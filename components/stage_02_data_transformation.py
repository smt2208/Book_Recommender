import logging
import pandas as pd
from entity.config_entity import DataTransformationConfig

logger = logging.getLogger(__name__)


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def transform_data(self, books, ratings):
        """Transform and filter data for collaborative filtering"""
        try:
            logger.info("Starting data transformation...")
            
            # Filter users who have rated more than min_user_ratings books
            logger.info(f"Filtering users with more than {self.config.min_user_ratings} ratings...")
            user_rating_counts = ratings['User-ID'].value_counts() > self.config.min_user_ratings
            active_users = user_rating_counts[user_rating_counts == True].index
            filtered_ratings = ratings[ratings['User-ID'].isin(active_users)]
            logger.info(f"Active users: {len(active_users)}")
            
            # Merge ratings with books
            logger.info("Merging ratings with books data...")
            ratings_with_books = pd.merge(filtered_ratings, books, on='ISBN')
            
            # Count number of ratings per book
            book_rating_counts = ratings_with_books.groupby('Title')['Book-Rating'].count().reset_index()
            book_rating_counts.rename(columns={'Book-Rating': 'Num_Ratings'}, inplace=True)
            
            # Merge rating counts back
            ratings_with_books = pd.merge(ratings_with_books, book_rating_counts, on='Title')
            
            # Filter books with at least min_book_ratings ratings
            logger.info(f"Filtering books with at least {self.config.min_book_ratings} ratings...")
            final_ratings = ratings_with_books[ratings_with_books['Num_Ratings'] >= self.config.min_book_ratings]
            
            # Remove duplicates
            final_ratings.drop_duplicates(['User-ID', 'Title'], inplace=True)
            
            logger.info(f"Final dataset shape: {final_ratings.shape}")
            
            # Create user-book matrix
            logger.info("Creating user-book matrix...")
            user_book_matrix = final_ratings.pivot_table(
                columns='User-ID', 
                index='Title', 
                values='Book-Rating'
            )
            user_book_matrix.fillna(0, inplace=True)
            
            logger.info(f"User-book matrix shape: {user_book_matrix.shape}")
            logger.info("Data transformation completed!")
            
            return final_ratings, user_book_matrix
            
        except Exception as e:
            logger.error(f"Error in data transformation: {e}")
            raise e
