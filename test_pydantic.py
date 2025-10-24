"""
Test Pydantic models validation
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

try:
    from entity.config_entity import (
        DataIngestionConfig, 
        DataValidationConfig, 
        DataTransformationConfig, 
        ModelTrainerConfig
    )
    
    print("✅ Pydantic models imported successfully!")
    
    # Test DataIngestionConfig validation
    try:
        config = DataIngestionConfig(
            root_dir=Path("test"),
            books_file=Path("books.csv"),
            users_file=Path("users.csv"),
            ratings_file=Path("ratings.csv")
        )
        print("✅ DataIngestionConfig validation passed")
    except Exception as e:
        print(f"❌ DataIngestionConfig validation failed: {e}")
    
    # Test ModelTrainerConfig validation with invalid values
    try:
        config = ModelTrainerConfig(
            root_dir=Path("test"),
            model_path=Path("model.pkl"),
            book_names_path=Path("names.pkl"),
            final_ratings_path=Path("ratings.pkl"),
            book_matrix_path=Path("matrix.pkl"),
            n_neighbors=-1,  # Invalid: should be positive
            algorithm="invalid_algorithm"  # Invalid: not in allowed values
        )
        print("❌ ModelTrainerConfig should have failed validation")
    except Exception as e:
        print(f"✅ ModelTrainerConfig validation correctly rejected invalid data: {e}")
    
    # Test ModelTrainerConfig validation with valid values
    try:
        config = ModelTrainerConfig(
            root_dir=Path("test"),
            model_path=Path("model.pkl"),
            book_names_path=Path("names.pkl"),
            final_ratings_path=Path("ratings.pkl"),
            book_matrix_path=Path("matrix.pkl"),
            n_neighbors=5,
            algorithm="brute"
        )
        print("✅ ModelTrainerConfig validation passed with valid data")
        print(f"   Algorithm: {config.algorithm} (type: {type(config.algorithm)})")
        print(f"   N-neighbors: {config.n_neighbors} (type: {type(config.n_neighbors)})")
    except Exception as e:
        print(f"❌ ModelTrainerConfig validation failed: {e}")

except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("Please install pydantic: pip install pydantic==2.5.0")