import shutil
from pathlib import Path

from src.config import RAW_DIR


def copy_csvs_to_raw(source_dir: Path, raw_dir: Path = RAW_DIR) -> list[Path]:
    """Copy all CSVs from source_dir into raw_dir. Returns list of copied paths."""
    raw_dir.mkdir(parents=True, exist_ok=True)
    copied = []
    for csv_file in sorted(source_dir.rglob("*.csv")):
        dest = raw_dir / csv_file.name
        shutil.copy2(csv_file, dest)
        copied.append(dest)
    return copied
