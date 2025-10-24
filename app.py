"""
Book Recommender Flask Web Application
Uses collaborative filtering to recommend similar books based on user ratings
"""

from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load pre-trained model and preprocessed data
model = pickle.load(open('artifacts/model.pkl', 'rb'))
book_names = pickle.load(open('artifacts/book_name.pkl', 'rb'))
final_ratings = pickle.load(open('artifacts/final_ratings.pkl', 'rb'))
book_matrix = pickle.load(open('artifacts/book_matrix.pkl', 'rb'))


def recommend_books(book_title, n_recommendations=5):
    """
    Generate book recommendations using K-Nearest Neighbors collaborative filtering
    
    Args:
        book_title (str): Title of the book to base recommendations on
        n_recommendations (int): Number of recommendations to return (default: 5)
    
    Returns:
        list: List of dictionaries containing recommended books with title, distance, and image URL
        None: If book is not found in the dataset
    """
    try:
        book_index = book_names.get_loc(book_title)
        
        distances, similar_indices = model.kneighbors(
            book_matrix.iloc[book_index, :].values.reshape(1, -1),
            n_neighbors=n_recommendations + 1
        )
        
        recommendations = []
        for i in range(1, len(similar_indices.flatten())):
            idx = similar_indices.flatten()[i]
            recommended_title = book_matrix.index[idx]
            similarity_distance = distances.flatten()[i]
            book_image_url = final_ratings[final_ratings['Title'] == recommended_title]['Image-URL'].iloc[0]
            
            recommendations.append({
                'title': recommended_title,
                'distance': round(similarity_distance, 4),
                'image_url': book_image_url
            })
        
        return recommendations
    
    except (IndexError, KeyError):
        return None


@app.route('/')
def index():
    """Render home page with book selection dropdown"""
    return render_template('index.html', book_list=list(book_names))


@app.route('/recommend', methods=['POST'])
def recommend():
    """Process book selection and display recommendations"""
    selected_book = request.form.get('book')
    
    if not selected_book:
        return render_template('index.html', book_list=list(book_names), error="Please select a book")
    
    recommendations = recommend_books(selected_book, n_recommendations=5)
    
    if recommendations is None:
        return render_template('index.html', book_list=list(book_names), 
                             error=f"Book '{selected_book}' not found in the dataset")
    
    return render_template('recommend.html', book_name=selected_book, recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
