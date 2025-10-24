"""
Data Ingestion Component
Loads and preprocesses the Book-Crossing dataset (Books, Users, Ratings)
"""

import pandas as pd
import logging
from typing import Tuple
from entity.config_entity import DataIngestionConfig

logger = logging.getLogger(__name__)


class DataIngestion:
    """Handles loading and initial preprocessing of raw data files"""
    
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Load all three datasets from CSV files
        
        Returns:
            Tuple of (books_df, users_df, ratings_df)
        """
        try:
            logger.info("Loading books dataset...")
            self.books = pd.read_csv(
                self.config.books_file, 
                sep=';', 
                on_bad_lines='skip', 
                encoding='latin-1', 
                low_memory=False
            )
            
            self.books = self.books[['ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 'Publisher', 'Image-URL-L']]
            self.books.rename(columns={
                'Book-Title': 'Title',
                'Book-Author': 'Author',
                'Year-Of-Publication': 'Year',
                'Image-URL-L': 'Image-URL'
            }, inplace=True)
            
            logger.info(f"Books dataset loaded: {self.books.shape}")
            
            logger.info("Loading users dataset...")
            self.users = pd.read_csv(
                self.config.users_file, 
                sep=';', 
                on_bad_lines='skip', 
                encoding='latin-1', 
                low_memory=False
            )
            logger.info(f"Users dataset loaded: {self.users.shape}")
            
            logger.info("Loading ratings dataset...")
            self.ratings = pd.read_csv(
                self.config.ratings_file, 
                sep=';', 
                on_bad_lines='skip', 
                encoding='latin-1', 
                low_memory=False
            )
            logger.info(f"Ratings dataset loaded: {self.ratings.shape}")
            
            return self.books, self.users, self.ratings
            
        except Exception as e:
            logger.error(f"Error in data ingestion: {e}")
            raise e
