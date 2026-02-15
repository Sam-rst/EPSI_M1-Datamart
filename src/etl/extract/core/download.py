from pathlib import Path

import kagglehub

from src.etl.extract.config import KAGGLE_DATASET


def download_dataset(dataset: str = KAGGLE_DATASET) -> Path:
    """Download dataset from Kaggle via kagglehub. Returns the download path."""
    return Path(kagglehub.dataset_download(dataset))
