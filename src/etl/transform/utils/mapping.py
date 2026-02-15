"""Pure functions for column renaming and FK resolution."""

import pandas as pd


def rename_columns(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    """Select and rename columns according to mapping {csv_col: model_col}."""
    available = {k: v for k, v in mapping.items() if k in df.columns}
    return df[list(available.keys())].rename(columns=available)


def safe_str_id(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Ensure ID columns are strings (not float from NaN coercion)."""
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype(str).replace("nan", None).replace("None", None)
    return df
