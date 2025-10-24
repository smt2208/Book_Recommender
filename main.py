"""
Main entry point for training the Book Recommender model
Executes the complete ML pipeline from data ingestion to model training
"""

from logger import log
from pipeline.training_pipeline import TrainingPipeline
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info("Starting Book Recommender Training Pipeline")
        pipeline = TrainingPipeline()
        pipeline.run_pipeline()
        logger.info("Training Pipeline completed successfully!")
        print("\n✅ Training completed! Run 'python app.py' to start the Flask application.")
    except Exception as e:
        logger.error(f"Training pipeline failed: {e}")
        print(f"\n❌ Error: {e}")
        raise e
