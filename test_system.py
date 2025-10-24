"""
Test script to verify the recommendation system works with saved artifacts
"""
import pickle
import os

def test_recommendation_system():
    """Test if the recommendation system works properly"""
    
    # Check if artifacts exist
    artifacts_path = 'artifacts'
    required_files = ['model.pkl', 'book_name.pkl', 'final_ratings.pkl', 'book_matrix.pkl']
    
    print("🔍 Checking for artifacts...")
    for file in required_files:
        file_path = os.path.join(artifacts_path, file)
        if os.path.exists(file_path):
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")
            print(f"\n⚠️ Please run 'python main.py' to train the model first.")
            return
    
    print("\n📦 Loading artifacts...")
    try:
        model = pickle.load(open('artifacts/model.pkl', 'rb'))
        book_names = pickle.load(open('artifacts/book_name.pkl', 'rb'))
        final_ratings = pickle.load(open('artifacts/final_ratings.pkl', 'rb'))
        book_matrix = pickle.load(open('artifacts/book_matrix.pkl', 'rb'))
        print("✅ All artifacts loaded successfully!")
        
        print(f"\n📊 Dataset Statistics:")
        print(f"   Total books in system: {len(book_names)}")
        print(f"   Total ratings: {len(final_ratings)}")
        print(f"   Matrix shape: {book_matrix.shape}")
        
        # Test recommendation
        print("\n🧪 Testing recommendation system...")
        test_book = book_names[0]  # Get first book
        print(f"   Input book: {test_book}")
        
        book_index = book_names.get_loc(test_book)
        distances, similar_indices = model.kneighbors(
            book_matrix.iloc[book_index, :].values.reshape(1, -1),
            n_neighbors=4
        )
        
        print(f"\n   Top 3 Recommendations:")
        for i in range(1, len(similar_indices.flatten())):
            idx = similar_indices.flatten()[i]
            recommended_title = book_matrix.index[idx]
            similarity_distance = distances.flatten()[i]
            print(f"   {i}. {recommended_title}")
            print(f"      Distance: {similarity_distance:.4f}")
        
        print("\n✅ Recommendation system working perfectly!")
        print("\n🚀 You can now run 'python app.py' to start the web application.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"Please ensure all artifacts are properly generated.")

if __name__ == "__main__":
    test_recommendation_system()
