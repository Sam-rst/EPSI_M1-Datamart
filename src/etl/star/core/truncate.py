"""Truncate star schema tables in reverse FK order."""

from sqlalchemy import text

from src.database.engine import engine
from src.etl.star.config.tables import STAR_TABLE_ORDER


def truncate_star_tables() -> list[str]:
    """Delete all rows from star tables (fact first, then dims). Returns truncated table names."""
    truncated = []
    with engine.connect() as conn:
        for table_name, _ in reversed(STAR_TABLE_ORDER):
            conn.execute(text(f"DELETE FROM {table_name}"))
            conn.commit()
            truncated.append(table_name)
    return truncated
