# 📖 Book Recommender System - Complete Project Flow

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Configuration System](#configuration-system)
4. [Data Flow Pipeline](#data-flow-pipeline)
5. [Model Training Process](#model-training-process)
6. [Web Application Flow](#web-application-flow)
7. [Code Execution Flow](#code-execution-flow)

---

## Overview

This document explains the complete end-to-end flow of the Book Recommender System, from data ingestion to serving recommendations through a web interface.

**Project Type**: Machine Learning - Recommendation System  
**Approach**: Item-Based Collaborative Filtering  
**Algorithm**: K-Nearest Neighbors (KNN)  
**Framework**: Modular Pipeline Architecture

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CONFIGURATION LAYER                          │
│  config.yaml → ConfigurationManager → Pydantic Models          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ML PIPELINE (4 Stages)                       │
│                                                                 │
│  Stage 1: Data Ingestion                                       │
│  ├── Load BX-Books.csv                                         │
│  ├── Load BX-Users.csv                                         │
│  └── Load BX-Book-Ratings.csv                                  │
│                              ↓                                  │
│  Stage 2: Data Validation                                      │
│  ├── Check data integrity                                      │
│  ├── Validate schemas                                          │
│  └── Verify data quality                                       │
│                              ↓                                  │
│  Stage 3: Data Transformation                                  │
│  ├── Filter active users (>200 ratings)                        │
│  ├── Filter popular books (>50 ratings)                        │
│  └── Create user-book matrix (742 × 888)                       │
│                              ↓                                  │
│  Stage 4: Model Training                                       │
│  ├── Convert to sparse matrix                                  │
│  ├── Train KNN model (cosine similarity)                       │
│  └── Save artifacts (model, data, matrix)                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    WEB APPLICATION                              │
│  Load artifacts → Flask App → User Interface → Recommendations │
└─────────────────────────────────────────────────────────────────┘
```

---

## Configuration System

### 1. Configuration File (`config/config.yaml`)

```yaml
artifacts_root: artifacts

data_ingestion:
  root_dir: artifacts/data_ingestion
  books_file: notebooks/BX-Books.csv
  users_file: notebooks/BX-Users.csv
  ratings_file: notebooks/BX-Book-Ratings.csv

data_validation:
  root_dir: artifacts/data_validation
  
data_transformation:
  root_dir: artifacts/data_transformation
  min_user_ratings: 200      # Filter threshold for active users
  min_book_ratings: 50       # Filter threshold for popular books
  
model_trainer:
  root_dir: artifacts/model_trainer
  model_path: artifacts/model.pkl
  book_names_path: artifacts/book_name.pkl
  final_ratings_path: artifacts/final_ratings.pkl
  book_matrix_path: artifacts/book_matrix.pkl
  n_neighbors: 5             # Number of similar books to find
  algorithm: brute           # KNN algorithm (brute, ball_tree, kd_tree, auto)
```

### 2. Configuration Entities (`entity/config_entity.py`)

**Purpose**: Type-safe configuration using Pydantic models

```python
# DataIngestionConfig
- root_dir: Where to store ingestion artifacts
- books_file: Path to books CSV
- users_file: Path to users CSV
- ratings_file: Path to ratings CSV

# DataTransformationConfig
- min_user_ratings: int (validated > 0)
- min_book_ratings: int (validated > 0)

# ModelTrainerConfig
- n_neighbors: int (validated > 0)
- algorithm: Literal['auto', 'ball_tree', 'kd_tree', 'brute']
```

**Key Features**:
- Runtime validation using Pydantic
- Immutable configurations (frozen=True)
- Type safety with descriptive error messages

### 3. Configuration Manager (`config/configuration.py`)

**Flow**:
```
YAML File → Read YAML → Parse to Dict → Create Pydantic Models → Return Config Objects
```

**Example**:
```python
config_manager = ConfigurationManager()
data_ingestion_config = config_manager.get_data_ingestion_config()
# Returns: DataIngestionConfig with validated paths
```

---

## Data Flow Pipeline

### Stage 1: Data Ingestion 📥

**File**: `components/stage_00_data_ingestion.py`

**Purpose**: Load and preprocess raw CSV files

**Input**:
- `notebooks/BX-Books.csv` (271,360 books)
- `notebooks/BX-Users.csv` (278,858 users)
- `notebooks/BX-Book-Ratings.csv` (1,149,780 ratings)

**Process**:
```python
1. Load BX-Books.csv
   ├── Read with sep=';', encoding='latin-1'
   ├── Select columns: ISBN, Book-Title, Book-Author, Year-Of-Publication, Publisher, Image-URL-L
   └── Rename columns: Title, Author, Year, Image-URL

2. Load BX-Users.csv
   └── Read with sep=';', encoding='latin-1'

3. Load BX-Book-Ratings.csv
   └── Read with sep=';', encoding='latin-1'
```

**Output**:
- `books_df`: DataFrame with book metadata
- `users_df`: DataFrame with user information
- `ratings_df`: DataFrame with user-book ratings

**Key Points**:
- Uses `latin-1` encoding for special characters
- `on_bad_lines='skip'` to handle malformed rows
- `low_memory=False` for better dtype inference

---

### Stage 2: Data Validation ✅

**File**: `components/stage_01_data_validation.py`

**Purpose**: Ensure data quality and integrity

**Validation Checks**:

```python
1. Non-Empty DataFrames
   ├── books.empty → ValueError
   ├── users.empty → ValueError
   └── ratings.empty → ValueError

2. Schema Validation (Books)
   Required columns: ['ISBN', 'Title', 'Author', 'Year', 'Publisher', 'Image-URL']

3. Schema Validation (Users)
   Required columns: ['User-ID']

4. Schema Validation (Ratings)
   Required columns: ['User-ID', 'ISBN', 'Book-Rating']

5. Data Type & Range Validation
   ├── Book-Rating: 0-10 range (warning if violated)
   └── Year: 1800-2025 range (warning if violated)
```

**Output**:
- Returns `True` if all validations pass
- Raises `ValueError` with descriptive message if fails

**Why Important**:
- Catches data quality issues early
- Prevents downstream pipeline failures
- Provides clear error messages for debugging

---

### Stage 3: Data Transformation 🔄

**File**: `components/stage_02_data_transformation.py`

**Purpose**: Filter and transform data for collaborative filtering

**Process Flow**:

```python
1. Filter Active Users
   ├── Count ratings per user: ratings['User-ID'].value_counts()
   ├── Keep users with > 200 ratings
   ├── Result: 888 active users (from 278,858)
   └── Reasoning: Users with more ratings provide better signals

2. Merge Ratings with Books
   ├── pd.merge(ratings, books, on='ISBN')
   └── Enriches ratings with book metadata

3. Calculate Book Popularity
   ├── Group by 'Title', count ratings
   ├── Create 'Num_Ratings' column
   └── Merge back to main dataframe

4. Filter Popular Books
   ├── Keep books with ≥ 50 ratings
   ├── Result: 742 books (from 271,360)
   └── Reasoning: Books with more ratings = more reliable recommendations

5. Remove Duplicates
   └── drop_duplicates(['User-ID', 'Title'])

6. Create User-Book Matrix
   ├── Pivot table: Books as rows, Users as columns, Ratings as values
   ├── Shape: (742, 888)
   ├── Fill NaN with 0 (no interaction)
   └── This is the core matrix for collaborative filtering
```

**Output**:
- `final_ratings`: Filtered DataFrame (59,850 ratings)
- `user_book_matrix`: Pivot table (742 books × 888 users)

**Example Matrix Structure**:
```
                    User-ID
Title               11676  41385  97783  ...
1984                    8      0      0  ...
Animal Farm             0      9      0  ...
Harry Potter            0      0     10  ...
```

**Why These Filters**:
- **Active users (>200)**: Ensure users have enough history for patterns
- **Popular books (>50)**: Ensure books have enough ratings for reliable similarity
- **Result**: High-quality dense interactions for better recommendations

---

### Stage 4: Model Training 🤖

**File**: `components/stage_03_model_trainer.py`

**Purpose**: Train KNN model and save artifacts

**Training Process**:

```python
1. Convert to Sparse Matrix
   ├── user_book_matrix (742 × 888) → csr_matrix
   ├── Why sparse? Most cells are 0 (no rating)
   ├── Memory efficient: Stores only non-zero values
   └── Original size: ~5.2MB → Sparse: ~467KB

2. Initialize KNN Model
   ├── Algorithm: 'brute' (exhaustive search)
   ├── Metric: 'cosine' (measures similarity)
   └── N-neighbors: 5 (find 5 most similar books)

3. Train Model
   ├── model.fit(sparse_matrix)
   ├── Learns book-to-book similarity
   └── No gradient descent (it's instance-based learning)

4. Save Artifacts
   ├── model.pkl → Trained KNN model
   ├── book_name.pkl → Book titles index
   ├── final_ratings.pkl → Processed ratings data
   └── book_matrix.pkl → User-book interaction matrix
```

**Cosine Similarity Explained**:
```
         Book A ratings: [8, 0, 9, 0, 7]
         Book B ratings: [7, 0, 10, 0, 8]
         
Cosine Similarity = dot(A, B) / (||A|| × ||B||)
                  = High similarity (similar rating patterns)
```

**Output**:
- `artifacts/model.pkl`: Trained NearestNeighbors model
- `artifacts/book_name.pkl`: pandas Index of 742 book titles
- `artifacts/final_ratings.pkl`: DataFrame with 59,850 ratings
- `artifacts/book_matrix.pkl`: 742×888 interaction matrix

---

## Model Training Process

### Mathematical Foundation

**Problem**: Given a book, find similar books based on user rating patterns

**Approach**: Item-Based Collaborative Filtering

```
Users who rated Book A similarly to Book B
→ Book A and Book B are similar
→ Recommend Book B to users who liked Book A
```

**Algorithm Steps**:

1. **Represent books as vectors** (each user's rating is a dimension)
   ```
   Book "1984" = [8, 0, 9, 0, 7, 0, ..., 10]  (888 dimensions)
   ```

2. **Calculate similarity** using cosine distance
   ```
   Distance = 1 - cosine_similarity
   Lower distance = More similar
   ```

3. **Find K nearest neighbors** (K=5)
   ```
   For "1984":
   1. "Animal Farm" (distance: 0.234)
   2. "Brave New World" (distance: 0.298)
   3. "Fahrenheit 451" (distance: 0.312)
   ...
   ```

### Why KNN for Recommendations?

**Advantages**:
- ✅ No training phase (just stores data)
- ✅ Naturally handles sparse data
- ✅ Easy to update (add new books/ratings)
- ✅ Interpretable (distance = similarity)
- ✅ Works well for item-based filtering

**Limitations**:
- ⚠️ Computational cost for large datasets
- ⚠️ Cold start problem (new books with few ratings)
- ⚠️ Memory intensive (stores entire matrix)

---

## Web Application Flow

### Application Startup (`app.py`)

```python
1. Initialize Flask App
   └── app = Flask(__name__)

2. Load Artifacts (at startup)
   ├── model = pickle.load('model.pkl')           # KNN model
   ├── book_names = pickle.load('book_name.pkl')  # 742 book titles
   ├── final_ratings = pickle.load('final_ratings.pkl')
   └── book_matrix = pickle.load('book_matrix.pkl')

3. Start Server
   └── app.run(host='0.0.0.0', port=5000)
```

### User Request Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. User visits http://localhost:5000                       │
│     ↓                                                        │
│  2. GET / → index() function                                │
│     ├── Loads 742 book titles                               │
│     └── Renders index.html with dropdown                    │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  3. User selects "Harry Potter" and clicks Submit           │
│     ↓                                                        │
│  4. POST /recommend → recommend() function                  │
│     ├── Get selected book from form                         │
│     ├── Call recommend_books("Harry Potter", n=5)           │
│     └── Render recommend.html with results                  │
└─────────────────────────────────────────────────────────────┘
```

### Recommendation Function Flow

```python
def recommend_books(book_title, n_recommendations=5):
    
    # Step 1: Find book's position in matrix
    book_index = book_names.get_loc("Harry Potter")
    # Result: 250 (array index)
    
    # Step 2: Get book's rating vector
    book_vector = book_matrix.iloc[250, :]
    # Shape: (888,) - one rating per user
    
    # Step 3: Find K nearest neighbors
    distances, similar_indices = model.kneighbors(
        book_vector.reshape(1, -1),  # Reshape to (1, 888)
        n_neighbors=6                # +1 because first is the book itself
    )
    # distances: [0.0, 47.54, 49.06, 49.10, 50.23, 51.45]
    # similar_indices: [250, 189, 67, 402, 531, 98]
    
    # Step 4: Build recommendation list (skip first - it's the input book)
    recommendations = []
    for i in range(1, 6):
        idx = similar_indices[0][i]
        title = book_matrix.index[idx]
        distance = distances[0][i]
        image = final_ratings[final_ratings['Title'] == title]['Image-URL'].iloc[0]
        
        recommendations.append({
            'title': title,
            'distance': round(distance, 4),
            'image_url': image
        })
    
    return recommendations
    # [
    #   {'title': 'Chamber of Secrets', 'distance': 47.54, 'image_url': '...'},
    #   {'title': 'Prisoner of Azkaban', 'distance': 49.06, 'image_url': '...'},
    #   ...
    # ]
```

---

## Code Execution Flow

### Training Pipeline Execution

**Command**: `python main.py`

```
main.py
  ↓
1. Import logger (initializes logging system)
   ├── Creates logs/ directory
   ├── Creates timestamped log file
   └── Configures logging format
  ↓
2. Initialize TrainingPipeline()
   └── Creates ConfigurationManager instance
  ↓
3. pipeline.run_pipeline()
   ↓
   ├─→ run_data_ingestion()
   │    ├── Get config: get_data_ingestion_config()
   │    ├── Create DataIngestion(config)
   │    ├── Call load_data()
   │    └── Return: books, users, ratings DataFrames
   │
   ├─→ run_data_validation(books, users, ratings)
   │    ├── Get config: get_data_validation_config()
   │    ├── Create DataValidation(config)
   │    ├── Call validate_data()
   │    └── Return: True (or raise error)
   │
   ├─→ run_data_transformation(books, ratings)
   │    ├── Get config: get_data_transformation_config()
   │    ├── Create DataTransformation(config)
   │    ├── Call transform_data()
   │    └── Return: final_ratings, user_book_matrix
   │
   └─→ run_model_training(final_ratings, user_book_matrix)
        ├── Get config: get_model_trainer_config()
        ├── Create ModelTrainer(config)
        ├── Call train_model()
        ├── Save 4 artifacts to artifacts/ folder
        └── Return: trained model
  ↓
4. Log success message
5. Print completion message
```

**Duration**: ~30-60 seconds (depending on system)

**Artifacts Created**:
```
artifacts/
├── model.pkl           (~2.1 MB)
├── book_name.pkl       (~18 KB)
├── final_ratings.pkl   (~4.5 MB)
└── book_matrix.pkl     (~5.2 MB)
```

### Web Application Execution

**Command**: `python app.py`

```
app.py
  ↓
1. Import Flask and dependencies
2. Load artifacts (model, book_names, final_ratings, book_matrix)
3. Define routes (@app.route)
4. Start Flask server
   ├── Host: 0.0.0.0 (accessible from network)
   ├── Port: 5000
   └── Debug: True (auto-reload on code changes)
  ↓
Server Running ✓
  ↓
User Request → Flask handles routing → Return response
```

---

## Infrastructure Components

### 1. Logging System (`logger/log.py`)

**Purpose**: Track execution and debug issues

```python
# Configuration
LOG_FILE = "10_24_2025_14_30_45.log"  # Timestamped
logs_path = "logs/10_24_2025_14_30_45/"
format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"

# Log Levels
INFO    → Normal execution flow
WARNING → Potential issues (but continues)
ERROR   → Errors that stop execution
```

**Log Example**:
```
[ 2025-10-24 14:30:45 ] 28 stage_00_data_ingestion - INFO - Loading books dataset...
[ 2025-10-24 14:30:47 ] 35 stage_00_data_ingestion - INFO - Books dataset loaded: (271360, 6)
```

### 2. Exception Handling (`exception/exception_handler.py`)

**Purpose**: Provide detailed error information

```python
class CustomException:
    # Captures:
    # - File name where error occurred
    # - Line number
    # - Error message
    
    # Example output:
    # "Error occurred in python script name [stage_00_data_ingestion.py] 
    #  line number [28] error message [File not found: BX-Books.csv]"
```

### 3. Utility Functions (`utils/util.py`)

```python
read_yaml(path)              # Load and parse YAML files
create_directories(paths)     # Create directory structure
save_pickle(data, path)       # Serialize objects
load_pickle(path)             # Deserialize objects
```

---

## Key Design Decisions

### 1. **Why Modular Pipeline?**
- Easy to test individual stages
- Simple to modify/replace components
- Clear separation of concerns
- Reusable components

### 2. **Why Pydantic for Config?**
- Runtime validation (catch errors early)
- Type safety (IDE support)
- Clear error messages
- Self-documenting code

### 3. **Why Item-Based (not User-Based)?**
- Books are more stable than users
- Fewer items than users (742 vs millions)
- Easier to explain recommendations
- Better cold start handling for new users

### 4. **Why Pickle for Artifacts?**
- Fast serialization/deserialization
- Preserves exact Python objects
- Simple to use
- Industry standard for sklearn models

### 5. **Why Flask (not FastAPI/Django)?**
- Lightweight and simple
- Perfect for small applications
- Easy to deploy
- Minimal boilerplate

---

## Performance Metrics

### Dataset Statistics
```
Original Dataset:
├── Books: 271,360
├── Users: 278,858
└── Ratings: 1,149,780

After Filtering:
├── Books: 742 (popular books)
├── Users: 888 (active users)
└── Ratings: 59,850 (quality interactions)

Matrix Sparsity: 99.1% (59,850 / 658,896 possible interactions)
```

### Model Performance
```
Algorithm: K-Nearest Neighbors
Metric: Cosine Distance
K: 5 neighbors
Search: Brute force (exhaustive)

Average query time: ~20ms
Memory usage: ~12MB (sparse matrix)
```

---

## Troubleshooting Guide

### Common Issues

**1. FileNotFoundError: CSV files not found**
- Solution: Ensure CSV files are in `notebooks/` directory
- Check: `notebooks/BX-Books.csv`, `BX-Users.csv`, `BX-Book-Ratings.csv`

**2. InconsistentVersionWarning: sklearn version mismatch**
- Cause: Model trained on sklearn 1.3.2, running on different version
- Solution: `pip install scikit-learn==1.3.2` or retrain model

**3. MemoryError during transformation**
- Cause: Insufficient RAM for matrix operations
- Solution: Increase swap space or reduce matrix size (adjust filters)

**4. Book not found in dataset**
- Cause: Selected book filtered out during transformation
- Solution: Check if book has ≥50 ratings in original dataset

---

## Summary

### Complete Flow Recap

```
1. Configuration
   ↓
2. Data Ingestion (Load CSVs)
   ↓
3. Data Validation (Check quality)
   ↓
4. Data Transformation (Filter & create matrix)
   ↓
5. Model Training (KNN + save artifacts)
   ↓
6. Web Application (Flask + recommendations)
```

### Key Takeaways

✅ **Modular Design**: Each stage is independent and testable  
✅ **Type Safety**: Pydantic ensures configuration correctness  
✅ **Collaborative Filtering**: Leverages user behavior patterns  
✅ **Production Ready**: Logging, error handling, and clean code  
✅ **Scalable**: Easy to add new features or modify existing ones

---

**For more details, see**:
- `README.md` - Project overview and setup
- `config/config.yaml` - All configuration parameters
- Individual component files - Stage-specific implementation

**Questions?** Open an issue on GitHub: https://github.com/smt2208/Book_Recommender/issues
