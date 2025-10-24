from pathlib import Path
from entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)
from constant import CONFIG_FILE_PATH
from utils.util import read_yaml, create_directories


class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)
        create_directories([self.config['artifacts_root']])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config['data_ingestion']
        create_directories([config['root_dir']])
        
        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config['root_dir']),
            books_file=Path(config['books_file']),
            users_file=Path(config['users_file']),
            ratings_file=Path(config['ratings_file'])
        )
        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config['data_validation']
        create_directories([config['root_dir']])
        
        data_validation_config = DataValidationConfig(
            root_dir=Path(config['root_dir'])
        )
        return data_validation_config

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config['data_transformation']
        create_directories([config['root_dir']])
        
        data_transformation_config = DataTransformationConfig(
            root_dir=Path(config['root_dir']),
            min_user_ratings=config['min_user_ratings'],
            min_book_ratings=config['min_book_ratings']
        )
        return data_transformation_config

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config['model_trainer']
        create_directories([config['root_dir']])
        
        model_trainer_config = ModelTrainerConfig(
            root_dir=Path(config['root_dir']),
            model_path=Path(config['model_path']),
            book_names_path=Path(config['book_names_path']),
            final_ratings_path=Path(config['final_ratings_path']),
            book_matrix_path=Path(config['book_matrix_path']),
            n_neighbors=config['n_neighbors'],
            algorithm=config['algorithm']
        )
        return model_trainer_config
