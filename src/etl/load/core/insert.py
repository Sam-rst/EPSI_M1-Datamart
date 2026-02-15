"""Insert processed CSVs into DuckDB via SQLAlchemy ORM bulk insert."""

import numpy as np
import pandas as pd
from sqlalchemy import Boolean, Double, Integer, inspect, insert
from sqlalchemy.orm import Session

from src.database.engine import SessionLocal
from src.etl.load.config import CHUNK_SIZE, LARGE_TABLES, TABLE_ORDER
from src.etl.load.utils import read_processed_csv


def _cast_dataframe(df: pd.DataFrame, model: type) -> pd.DataFrame:
    """Cast DataFrame columns to match ORM model types."""
    mapper = inspect(model)
    col_types = {col.key: col.type for col in mapper.columns}
    df = df.copy()

    for col_name, col_type in col_types.items():
        if col_name not in df.columns:
            continue
        if isinstance(col_type, Boolean):
            df[col_name] = df[col_name].map(
                {"True": True, "true": True, "1": True, "1.0": True,
                 "False": False, "false": False, "0": False, "0.0": False}
            )
        elif isinstance(col_type, Integer):
            df[col_name] = pd.to_numeric(df[col_name], errors="coerce").astype("Int64")
        elif isinstance(col_type, Double):
            df[col_name] = pd.to_numeric(df[col_name], errors="coerce")

    # Replace all NaN/NaT/None with None for DuckDB
    df = df.where(df.notna(), None)
    # Also replace numpy types that might slip through
    df = df.replace({np.nan: None})
    return df


def _df_to_records(df: pd.DataFrame) -> list[dict]:
    """Convert DataFrame to list of dicts with proper None handling."""
    records = df.to_dict(orient="records")
    # Final pass: convert any remaining numpy NaN to None
    for row in records:
        for k, v in row.items():
            if isinstance(v, float) and (v != v):  # NaN check without math import
                row[k] = None
            elif isinstance(v, np.integer):
                row[k] = int(v)
            elif isinstance(v, np.floating):
                row[k] = float(v) if v == v else None
            elif v is pd.NA or v is pd.NaT:
                row[k] = None
    return records


def insert_table(
    table_name: str,
    model: type,
    session: Session,
) -> int:
    """Read processed CSV and bulk-insert via ORM. Returns row count."""
    df = read_processed_csv(table_name)
    df = _cast_dataframe(df, model)

    if table_name in LARGE_TABLES:
        total = len(df)
        for i in range(0, total, CHUNK_SIZE):
            chunk_df = df.iloc[i : i + CHUNK_SIZE]
            records = _df_to_records(chunk_df)
            session.execute(insert(model), records)
            session.commit()
            print(f"    chunk {i + len(records):,}/{total:,}", flush=True)
        return total
    else:
        records = _df_to_records(df)
        if not records:
            return 0
        session.execute(insert(model), records)
        return len(records)


def insert_all(session: Session | None = None) -> dict[str, int]:
    """Insert all 14 tables in FK order. Returns {table_name: row_count}."""
    own_session = session is None
    if own_session:
        session = SessionLocal()

    counts: dict[str, int] = {}
    try:
        for table_name, model in TABLE_ORDER:
            print(f"  {table_name}...", end=" ", flush=True)
            count = insert_table(table_name, model, session)
            session.commit()
            counts[table_name] = count
            print(f"{count:,} lignes")
    except Exception:
        session.rollback()
        raise
    finally:
        if own_session:
            session.close()

    return counts
