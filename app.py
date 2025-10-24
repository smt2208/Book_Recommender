from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the saved model and data
model = pickle.load(open('artifacts/model.pkl', 'rb'))
book_names = pickle.load(open('artifacts/book_name.pkl', 'rb'))
final_ratings = pickle.load(open('artifacts/final_ratings.pkl', 'rb'))
book_matrix = pickle.load(open('artifacts/book_matrix.pkl', 'rb'))


def recommend_books(book_title, n_recommendations=5):
    """
    Recommend books based on a given book title using collaborative filtering
    
    Parameters:
    -----------
    book_title : str
        Title of the book to base recommendations on
    n_recommendations : int
        Number of book recommendations to return
    
    Returns:
    --------
    list of tuples: (title, distance, image_url)
    """
    try:
        # Find the book's position in the matrix
        book_index = book_names.get_loc(book_title)
        
        # Get similar books using KNN model
        distances, similar_indices = model.kneighbors(
            book_matrix.iloc[book_index, :].values.reshape(1, -1),
            n_neighbors=n_recommendations + 1
        )
        
        recommendations = []
        # Skip first one as it's the input book itself
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
    """Home page with book selection"""
    return render_template('index.html', book_list=list(book_names))


@app.route('/recommend', methods=['POST'])
def recommend():
    """Recommendation page"""
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
