from pathlib import Path

import pandas as pd


def check_pk_duplicates(csv_path: Path, pk_columns: list[str]) -> int:
    """Return the number of duplicate rows on the given primary key columns."""
    df = pd.read_csv(csv_path)
    return int(df.duplicated(subset=pk_columns).sum())


def check_nulls(csv_path: Path) -> pd.Series:
    """Return percentage of nulls per column (only columns with nulls)."""
    df = pd.read_csv(csv_path)
    null_pct = df.isnull().mean() * 100
    return null_pct[null_pct > 0].sort_values(ascending=False)


def validate_all(
    raw_dir: Path, primary_keys: dict[str, list[str]]
) -> dict[str, dict]:
    """Run PK duplicate + null checks on all CSVs. Returns {filename: {duplicates, nulls}}."""
    results = {}
    for csv_path in sorted(raw_dir.glob("*.csv")):
        name = csv_path.name
        pk = primary_keys.get(name, [])
        nulls = check_nulls(csv_path)
        results[name] = {
            "duplicates": check_pk_duplicates(csv_path, pk) if pk else None,
            "pk_columns": pk,
            "nulls": nulls,
        }
    return results
