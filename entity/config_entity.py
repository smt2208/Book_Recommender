from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class DataIngestionConfig(BaseModel):
    model_config = ConfigDict(frozen=True, protected_namespaces=())
    
    root_dir: Path
    books_file: Path
    users_file: Path
    ratings_file: Path


class DataValidationConfig(BaseModel):
    model_config = ConfigDict(frozen=True, protected_namespaces=())
    
    root_dir: Path


class DataTransformationConfig(BaseModel):
    model_config = ConfigDict(frozen=True, protected_namespaces=())
    
    root_dir: Path
    min_user_ratings: int = Field(gt=0, description="Minimum user ratings must be positive")
    min_book_ratings: int = Field(gt=0, description="Minimum book ratings must be positive")


class ModelTrainerConfig(BaseModel):
    model_config = ConfigDict(frozen=True, protected_namespaces=())
    
    root_dir: Path
    model_path: Path
    book_names_path: Path
    final_ratings_path: Path
    book_matrix_path: Path
    n_neighbors: int = Field(gt=0, description="Number of neighbors must be positive")
    algorithm: Literal['auto', 'ball_tree', 'kd_tree', 'brute'] = Field(default='brute', description="KNN algorithm type")
