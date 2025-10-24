"""
Data Validation Component
Validates data integrity, schema, and quality of loaded datasets
"""

import logging
import pandas as pd
from entity.config_entity import DataValidationConfig
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class DataValidation:
    """Performs comprehensive validation checks on loaded datasets"""
    
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_data(self, books: pd.DataFrame, users: pd.DataFrame, ratings: pd.DataFrame) -> bool:
        """
        Validate the loaded datasets for completeness and correctness
        
        Args:
            books: Books DataFrame
            users: Users DataFrame  
            ratings: Ratings DataFrame
            
        Returns:
            bool: True if validation passes
        """
        try:
            logger.info("Starting data validation...")
            
            self._validate_non_empty_dataframes(books, users, ratings)
            self._validate_books_schema(books)
            self._validate_users_schema(users)
            self._validate_ratings_schema(ratings)
            self._validate_data_types_and_ranges(books, users, ratings)
            
            logger.info("Data validation successful!")
            return True
            
        except (ValidationError, ValueError, AssertionError) as e:
            logger.error(f"Data validation failed: {e}")
            raise e

    def _validate_non_empty_dataframes(self, books: pd.DataFrame, users: pd.DataFrame, ratings: pd.DataFrame):
        """Check if dataframes are not empty"""
        if books.empty:
            raise ValueError("Books dataset is empty")
        if users.empty:
            raise ValueError("Users dataset is empty") 
        if ratings.empty:
            raise ValueError("Ratings dataset is empty")

    def _validate_books_schema(self, books: pd.DataFrame):
        """Validate books dataframe schema"""
        required_books_cols = ['ISBN', 'Title', 'Author', 'Year', 'Publisher', 'Image-URL']
        missing_cols = [col for col in required_books_cols if col not in books.columns]
        if missing_cols:
            raise ValueError(f"Books dataset missing required columns: {missing_cols}")

    def _validate_users_schema(self, users: pd.DataFrame):
        """Validate users dataframe schema"""
        required_users_cols = ['User-ID']
        missing_cols = [col for col in required_users_cols if col not in users.columns]
        if missing_cols:
            raise ValueError(f"Users dataset missing required columns: {missing_cols}")

    def _validate_ratings_schema(self, ratings: pd.DataFrame):
        """Validate ratings dataframe schema"""
        required_ratings_cols = ['User-ID', 'ISBN', 'Book-Rating']
        missing_cols = [col for col in required_ratings_cols if col not in ratings.columns]
        if missing_cols:
            raise ValueError(f"Ratings dataset missing required columns: {missing_cols}")

    def _validate_data_types_and_ranges(self, books: pd.DataFrame, users: pd.DataFrame, ratings: pd.DataFrame):
        """Validate data types and value ranges"""
        # Validate ratings are in acceptable range (0-10)
        if 'Book-Rating' in ratings.columns:
            invalid_ratings = ratings['Book-Rating'][(ratings['Book-Rating'] < 0) | (ratings['Book-Rating'] > 10)]
            if len(invalid_ratings) > 0:
                logger.warning(f"Found {len(invalid_ratings)} ratings outside 0-10 range")
        
        # Validate year is reasonable
        if 'Year' in books.columns:
            current_year = 2025
            invalid_years = books['Year'][(books['Year'] < 1800) | (books['Year'] > current_year)]
            if len(invalid_years) > 0:
                logger.warning(f"Found {len(invalid_years)} books with unrealistic publication years")
