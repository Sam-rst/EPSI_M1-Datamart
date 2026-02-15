"""Insert processed CSVs into DuckDB via native read_csv (COPY)."""

from sqlalchemy import inspect, text

from src.config import PROCESSED_DIR
from src.database.engine import engine
from src.etl.load.config import TABLE_ORDER


def copy_table(table_name: str, model: type) -> int:
    """Load a CSV into DuckDB using native read_csv. Returns row count."""
    csv_path = PROCESSED_DIR / f"{table_name}.csv"
    # DuckDB needs forward slashes even on Windows.
    csv_str = str(csv_path).replace("\\", "/")

    # Get column names from ORM model to ensure correct mapping.
    mapper = inspect(model)
    columns = [col.key for col in mapper.columns]
    col_list = ", ".join(columns)

    with engine.connect() as conn:
        conn.execute(
            text(
                f"INSERT INTO {table_name} ({col_list}) "
                f"SELECT {col_list} FROM read_csv_auto('{csv_str}')"
            )
        )
        conn.commit()

        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.scalar()

    return count


def copy_all() -> dict[str, int]:
    """Copy all 14 tables in FK order via native read_csv. Returns {table_name: row_count}."""
    counts: dict[str, int] = {}

    for table_name, model in TABLE_ORDER:
        print(f"  {table_name}...", end=" ", flush=True)
        count = copy_table(table_name, model)
        counts[table_name] = count
        print(f"{count:,} lignes")

    return counts
