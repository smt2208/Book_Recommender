import os
import yaml
import pickle
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def read_yaml(path_to_yaml: Path) -> dict:
    """Read yaml file and returns dictionary"""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return content
    except Exception as e:
        logger.error(f"Error reading yaml file: {e}")
        raise e


def create_directories(path_to_directories: list, verbose=True):
    """Create list of directories"""
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


def save_pickle(data, path: Path):
    """Save object as pickle file"""
    with open(path, 'wb') as f:
        pickle.dump(data, f)
    logger.info(f"Pickle file saved at: {path}")


def load_pickle(path: Path):
    """Load pickle file"""
    with open(path, 'rb') as f:
        data = pickle.load(f)
    logger.info(f"Pickle file loaded from: {path}")
    return data
