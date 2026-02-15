"""Orchestrate the full ETL pipeline: extract → transform → load."""

import time

from src.etl.extract.main import run as extract
from src.etl.transform.main import run as transform
from src.etl.load.main import run as load


def run() -> None:
    """Run the complete ETL pipeline end-to-end."""
    start = time.perf_counter()
    print("=" * 60)
    print("  PIPELINE ETL — Rocket League Esports")
    print("=" * 60)

    # 1. Extract
    print("\n[1/3] EXTRACT\n")
    extract()

    # 2. Transform
    print("\n[2/3] TRANSFORM\n")
    tables = transform()

    # 3. Load
    print("\n[3/3] LOAD\n")
    counts = load()

    # Summary
    elapsed = time.perf_counter() - start
    minutes, seconds = divmod(elapsed, 60)
    print("\n" + "=" * 60)
    print("  PIPELINE TERMINEE")
    print(f"  {len(counts)} tables | {sum(counts.values()):,} lignes")
    print(f"  Duree : {int(minutes)}m {seconds:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    run()
