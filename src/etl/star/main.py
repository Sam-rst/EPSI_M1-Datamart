"""Orchestrate star schema ETL: migrate -> truncate -> dimensions -> fact."""

import time

from src.etl.load.core import apply_migrations
from src.etl.star.core import (
    populate_dimensions,
    populate_fact_player_game,
    truncate_star_tables,
)


def run() -> dict[str, int]:
    """Run the full star schema pipeline. Returns {table_name: row_count}."""
    start = time.perf_counter()
    print("=" * 60)
    print("  STAR SCHEMA — Rocket League Esports")
    print("=" * 60)

    # 1. Migrations
    print("\n[1/4] Migrations Alembic")
    apply_migrations()
    print("  Schema a jour.\n")

    # 2. Truncate star tables
    print("[2/4] Truncate star tables")
    truncated = truncate_star_tables()
    print(f"  {len(truncated)} tables videes.\n")

    # 3. Populate dimensions
    print("[3/4] Peuplement des dimensions")
    counts = populate_dimensions()
    print()

    # 4. Populate fact table
    print("[4/4] Peuplement de la table de faits")
    fact_count = populate_fact_player_game()
    counts["fact_player_game"] = fact_count
    print(f"  fact_player_game   {fact_count:>8,} lignes\n")

    # Summary
    elapsed = time.perf_counter() - start
    total = sum(counts.values())
    print("=" * 60)
    print(f"  STAR SCHEMA TERMINE")
    print(f"  {len(counts)} tables | {total:,} lignes")
    print(f"  Duree : {elapsed:.1f}s")
    print("=" * 60)

    return counts


if __name__ == "__main__":
    run()
