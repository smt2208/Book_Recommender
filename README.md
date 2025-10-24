# 📚 Book Recommender System

An intelligent book recommendation system built with collaborative filtering using K-Nearest Neighbors algorithm. The system analyzes user-book interactions to provide personalized book recommendations through an intuitive web interface.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

This end-to-end machine learning project implements item-based collaborative filtering to recommend books based on user rating patterns. The system uses the Book-Crossing dataset and provides a Flask web application for easy interaction.

### Key Features

- ✅ **Collaborative Filtering**: Item-based recommendation using K-Nearest Neighbors
- ✅ **Robust Pipeline**: Modular ML pipeline with data validation and transformation
- ✅ **Web Interface**: Beautiful and responsive Flask application
- ✅ **Type Safety**: Pydantic models for configuration validation
- ✅ **Professional Logging**: Comprehensive logging system for debugging and monitoring
- ✅ **Scalable Architecture**: Modular design following software engineering best practices

## 🏗️ Project Architecture

```
Book_Recommender/
├── artifacts/              # Trained models and processed data
├── components/             # ML pipeline components
│   ├── stage_00_data_ingestion.py
│   ├── stage_01_data_validation.py
│   ├── stage_02_data_transformation.py
│   └── stage_03_model_trainer.py
├── config/                 # Configuration management
│   ├── config.yaml
│   └── configuration.py
├── constant/               # Project constants
├── entity/                 # Data models (Pydantic)
├── exception/              # Custom exception handling
├── logger/                 # Logging configuration
├── notebooks/              # Research notebooks and datasets
├── pipeline/               # Training pipeline orchestration
├── templates/              # Flask HTML templates
├── utils/                  # Utility functions
├── app.py                  # Flask web application
└── main.py                 # Training pipeline entry point
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/smt2208/Book_Recommender.git
cd Book_Recommender
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Usage

#### Option 1: Use Pre-trained Model

If you have the pre-trained model files in the `artifacts/` directory:

```bash
python app.py
```

Then open your browser and navigate to `http://localhost:5000`

#### Option 2: Train from Scratch

1. Ensure the CSV data files are in the `notebooks/` directory:
   - `BX-Books.csv`
   - `BX-Users.csv`
   - `BX-Book-Ratings.csv`

2. Run the training pipeline:
```bash
python main.py
```

3. Start the Flask application:
```bash
python app.py
```

## 📊 ML Pipeline Stages

### Stage 1: Data Ingestion
Loads and preprocesses the Book-Crossing dataset containing books, users, and ratings information.

### Stage 2: Data Validation
Validates data integrity, schema correctness, and data quality through comprehensive checks.

### Stage 3: Data Transformation
- Filters active users (>200 ratings)
- Filters popular books (>50 ratings)
- Creates user-book interaction matrix

### Stage 4: Model Training
- Trains K-Nearest Neighbors model using cosine similarity
- Saves model and artifacts for deployment

## � Configuration

All configuration parameters are managed through `config/config.yaml`:

```yaml
data_transformation:
  min_user_ratings: 200
  min_book_ratings: 50
  
model_trainer:
  n_neighbors: 5
  algorithm: brute
```

## 📈 Model Performance

- **Algorithm**: K-Nearest Neighbors (KNN)
- **Similarity Metric**: Cosine Distance
- **Dataset Size**: 742 books, 888 active users, 59,850 ratings
- **Matrix Shape**: 742 × 888 (sparse)

## 🌐 Web Interface

The Flask application provides:
- Intuitive book selection dropdown
- Visual recommendations with book covers
- Similarity scores for each recommendation
- Responsive design for all devices

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python** | Core programming language |
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computations |
| **Scikit-learn** | Machine learning algorithms |
| **SciPy** | Sparse matrix operations |
| **Flask** | Web framework |
| **Pydantic** | Data validation |
| **PyYAML** | Configuration management |

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Shyam Mohan Tripathi**
- GitHub: [@smt2208](https://github.com/smt2208)
- Email: rkknightx@gmail.com

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/smt2208/Book_Recommender/issues).

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!
