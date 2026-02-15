"""Truncate all tables in reverse FK order for idempotent reload."""

from sqlalchemy.orm import Session

from src.database.engine import SessionLocal
from src.etl.load.config import TABLE_ORDER


def truncate_all(session: Session | None = None) -> list[str]:
    """Delete all rows from every table (reverse FK order). Returns truncated table names."""
    own_session = session is None
    if own_session:
        session = SessionLocal()

    truncated = []
    try:
        for table_name, model in reversed(TABLE_ORDER):
            session.query(model).delete()
            session.commit()
            truncated.append(table_name)
    except Exception:
        session.rollback()
        raise
    finally:
        if own_session:
            session.close()

    return truncated
