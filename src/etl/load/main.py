"""Orchestrate the full load: migrate → truncate → insert into DuckDB."""

from src.etl.load.core import apply_migrations, insert_all, truncate_all


def run() -> dict[str, int]:
    """Run the full load pipeline. Returns {table_name: row_count}."""
    print("=== Chargement en base DuckDB ===\n")

    # 1. Migrations
    print("--- Migrations Alembic ---")
    apply_migrations()
    print("  Schema a jour.\n")

    # 2. Truncate
    print("--- Truncate (reload idempotent) ---")
    truncated = truncate_all()
    print(f"  {len(truncated)} tables videes.\n")

    # 3. Insert
    print("--- Insertion via ORM ---")
    counts = insert_all()

    total = sum(counts.values())
    print(f"\n=== Chargement termine : {total:,} lignes dans {len(counts)} tables ===")
    return counts


if __name__ == "__main__":
    run()
