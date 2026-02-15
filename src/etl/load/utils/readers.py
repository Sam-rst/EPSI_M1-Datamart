"""Read processed CSVs into DataFrames with correct dtypes."""

from pathlib import Path

import pandas as pd

from src.config import PROCESSED_DIR


def read_processed_csv(
    table_name: str, processed_dir: Path = PROCESSED_DIR
) -> pd.DataFrame:
    """Read a processed CSV with all columns as strings to preserve IDs."""
    path = processed_dir / f"{table_name}.csv"
    df = pd.read_csv(path, dtype=str, keep_default_na=True, low_memory=False)
    return df
