import logging
from config.configuration import ConfigurationManager
from components.stage_00_data_ingestion import DataIngestion
from components.stage_01_data_validation import DataValidation
from components.stage_02_data_transformation import DataTransformation
from components.stage_03_model_trainer import ModelTrainer

logger = logging.getLogger(__name__)


class TrainingPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()

    def run_data_ingestion(self):
        """Run data ingestion stage"""
        try:
            logger.info("=" * 50)
            logger.info("STAGE 1: Data Ingestion Started")
            config = self.config_manager.get_data_ingestion_config()
            data_ingestion = DataIngestion(config)
            books, users, ratings = data_ingestion.load_data()
            logger.info("STAGE 1: Data Ingestion Completed")
            logger.info("=" * 50)
            return books, users, ratings
        except Exception as e:
            logger.error(f"Error in data ingestion stage: {e}")
            raise e

    def run_data_validation(self, books, users, ratings):
        """Run data validation stage"""
        try:
            logger.info("=" * 50)
            logger.info("STAGE 2: Data Validation Started")
            config = self.config_manager.get_data_validation_config()
            data_validation = DataValidation(config)
            data_validation.validate_data(books, users, ratings)
            logger.info("STAGE 2: Data Validation Completed")
            logger.info("=" * 50)
        except Exception as e:
            logger.error(f"Error in data validation stage: {e}")
            raise e

    def run_data_transformation(self, books, ratings):
        """Run data transformation stage"""
        try:
            logger.info("=" * 50)
            logger.info("STAGE 3: Data Transformation Started")
            config = self.config_manager.get_data_transformation_config()
            data_transformation = DataTransformation(config)
            final_ratings, user_book_matrix = data_transformation.transform_data(books, ratings)
            logger.info("STAGE 3: Data Transformation Completed")
            logger.info("=" * 50)
            return final_ratings, user_book_matrix
        except Exception as e:
            logger.error(f"Error in data transformation stage: {e}")
            raise e

    def run_model_training(self, final_ratings, user_book_matrix):
        """Run model training stage"""
        try:
            logger.info("=" * 50)
            logger.info("STAGE 4: Model Training Started")
            config = self.config_manager.get_model_trainer_config()
            model_trainer = ModelTrainer(config)
            model = model_trainer.train_model(final_ratings, user_book_matrix)
            logger.info("STAGE 4: Model Training Completed")
            logger.info("=" * 50)
            return model
        except Exception as e:
            logger.error(f"Error in model training stage: {e}")
            raise e

    def run_pipeline(self):
        """Run the complete training pipeline"""
        try:
            # Stage 1: Data Ingestion
            books, users, ratings = self.run_data_ingestion()
            
            # Stage 2: Data Validation
            self.run_data_validation(books, users, ratings)
            
            # Stage 3: Data Transformation
            final_ratings, user_book_matrix = self.run_data_transformation(books, ratings)
            
            # Stage 4: Model Training
            model = self.run_model_training(final_ratings, user_book_matrix)
            
            logger.info("=" * 50)
            logger.info("Training Pipeline Completed Successfully!")
            logger.info("=" * 50)
            
        except Exception as e:
            logger.error(f"Training pipeline failed: {e}")
            raise e


if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()
