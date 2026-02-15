"""Export transformed DataFrames to CSV files in data/processed/."""

from pathlib import Path

import pandas as pd

from src.config import PROCESSED_DIR


def export_tables(
    tables: dict[str, pd.DataFrame],
    output_dir: Path = PROCESSED_DIR,
) -> list[Path]:
    """Write each DataFrame as a CSV in output_dir. Returns list of written paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name, df in tables.items():
        path = output_dir / f"{name}.csv"
        df.to_csv(path, index=False)
        written.append(path)
    return written
