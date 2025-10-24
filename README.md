# 📚 Book Recommender System

An end-to-end book recommendation system using collaborative filtering with K-Nearest Neighbors algorithm.

## 🎯 Project Overview

This project implements a book recommendation system based on collaborative filtering (item-based). The system analyzes user ratings to find similar books and provides personalized recommendations.

## 📁 Project Structure

```
Book_Recommender/
├── artifacts/              # Saved models and processed data
├── components/             # Pipeline components
│   ├── stage_00_data_ingestion.py
│   ├── stage_01_data_validation.py
│   ├── stage_02_data_transformation.py
│   └── stage_03_model_trainer.py
├── config/                 # Configuration files
│   ├── config.yaml
│   └── configuration.py
├── constant/               # Constants
├── entity/                 # Data entities
│   └── config_entity.py
├── exception/              # Custom exceptions
│   └── exception_handler.py
├── logger/                 # Logging setup
│   └── log.py
├── notebooks/              # Research notebooks and data
├── pipeline/               # Training pipeline
│   └── training_pipeline.py
├── templates/              # Flask HTML templates
│   ├── index.html
│   └── recommend.html
├── utils/                  # Utility functions
│   └── util.py
├── app.py                  # Flask web application
├── main.py                 # Training pipeline runner
└── requirements.txt        # Dependencies
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/smt2208/Book_Recommender.git
cd Book_Recommender
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

#### Option 1: Use Pre-trained Model (If artifacts exist)

If you already have the pickle files in the `artifacts` folder, directly run the Flask app:

```bash
python app.py
```

#### Option 2: Train from Scratch

1. Ensure the CSV data files are in the `notebooks` folder:
   - BX-Books.csv
   - BX-Users.csv
   - BX-Book-Ratings.csv

2. Run the training pipeline:
```bash
python main.py
```

3. Start the Flask application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## 🔧 How It Works

1. **Data Ingestion**: Loads books, users, and ratings datasets
2. **Data Validation**: Validates data integrity and required columns
3. **Data Transformation**: 
   - Filters active users (>200 ratings)
   - Filters popular books (>50 ratings)
   - Creates user-book interaction matrix
4. **Model Training**: 
   - Trains KNN model using collaborative filtering
   - Saves model and artifacts for deployment

## 📊 Model Details

- **Algorithm**: K-Nearest Neighbors (KNN)
- **Approach**: Item-based Collaborative Filtering
- **Similarity Metric**: Cosine Distance
- **Features**: User-Book rating matrix

## 🌐 Web Interface

The Flask web application provides:
- Book selection interface
- Visual recommendations with book covers
- Similarity scores for each recommendation

## 📦 Saved Artifacts

The training pipeline generates:
- `model.pkl` - Trained KNN model
- `book_name.pkl` - Book titles index
- `final_ratings.pkl` - Processed ratings dataframe
- `book_matrix.pkl` - User-book interaction matrix

## 🛠️ Technologies Used

- **Python** - Programming language
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning
- **SciPy** - Sparse matrix operations
- **Flask** - Web framework
- **HTML/CSS** - Frontend

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**smt2208**

---

⭐ If you find this project helpful, please give it a star!
