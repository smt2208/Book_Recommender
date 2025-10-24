"""
Model Training Component
Trains K-Nearest Neighbors model for collaborative filtering and saves artifacts
"""

import logging
import pandas as pd
from typing import Tuple
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from entity.config_entity import ModelTrainerConfig
from utils.util import save_pickle

logger = logging.getLogger(__name__)


class ModelTrainer:
    """Trains and saves the recommendation model"""
    
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def train_model(self, final_ratings: pd.DataFrame, user_book_matrix: pd.DataFrame) -> NearestNeighbors:
        """
        Train KNN model for item-based collaborative filtering
        
        Args:
            final_ratings: Processed ratings DataFrame
            user_book_matrix: User-book interaction matrix
            
        Returns:
            Trained NearestNeighbors model
        """
        try:
            logger.info("Starting model training...")
            
            logger.info("Converting to sparse matrix...")
            sparse_user_book_matrix = csr_matrix(user_book_matrix.values)
            
            logger.info(f"Training KNN model with algorithm: {self.config.algorithm}")
            model = NearestNeighbors(algorithm=self.config.algorithm, metric='cosine')
            model.fit(sparse_user_book_matrix)
            
            logger.info("Model training completed!")
            
            logger.info("Saving model and artifacts...")
            save_pickle(model, self.config.model_path)
            save_pickle(user_book_matrix.index, self.config.book_names_path)
            save_pickle(final_ratings, self.config.final_ratings_path)
            save_pickle(user_book_matrix, self.config.book_matrix_path)
            
            logger.info("All artifacts saved successfully!")
            
            return model
            
        except Exception as e:
            logger.error(f"Error in model training: {e}")
            raise e
