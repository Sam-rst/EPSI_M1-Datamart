from pathlib import Path

from src.config import RAW_DIR
from src.etl.extract.config import MIN_CSV_COUNT
from src.etl.extract.core.copy import copy_csvs_to_raw
from src.etl.extract.core.download import download_dataset


def ensure_raw_csvs(raw_dir: Path = RAW_DIR) -> tuple[bool, list[Path]]:
    """Idempotent: download + copy only if CSVs are missing. Returns (skipped, csv_paths)."""
    existing = list(raw_dir.glob("*.csv"))
    if len(existing) >= MIN_CSV_COUNT:
        return True, sorted(existing)

    download_path = download_dataset()
    copied = copy_csvs_to_raw(download_path, raw_dir)
    return False, copied
