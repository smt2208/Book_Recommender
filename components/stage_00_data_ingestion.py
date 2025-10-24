import os
import pandas as pd
import logging
from entity.config_entity import DataIngestionConfig

logger = logging.getLogger(__name__)


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def load_data(self):
        """Load all three datasets: books, users, and ratings"""
        try:
            logger.info("Loading books dataset...")
            self.books = pd.read_csv(
                self.config.books_file, 
                sep=';', 
                on_bad_lines='skip', 
                encoding='latin-1', 
                low_memory=False
            )
            
            # Select and rename columns
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
