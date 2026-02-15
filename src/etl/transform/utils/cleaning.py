"""Pure functions for deduplication and type casting."""

import pandas as pd


def dedup(df: pd.DataFrame, subset: list[str]) -> pd.DataFrame:
    """Drop duplicate rows on the given columns, keeping first occurrence."""
    return df.drop_duplicates(subset=subset, keep="first").reset_index(drop=True)


def cast_boolean(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Cast string columns ('True'/'False'/NaN) to nullable boolean."""
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = df[col].map({"True": True, "true": True, "False": False, "false": False})
    return df


def cast_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Cast string columns to numeric (float), coercing errors to NaN."""
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def cast_integer(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Cast columns to nullable integer."""
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    return df
