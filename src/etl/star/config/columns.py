"""Stat column names for the fact table pivot (sourced from transform config)."""

from src.etl.transform.config.columns import PLAYER_STAT_COLUMNS

# Flat list of all 84 player stat column names (used by the EAV pivot query).
FACT_STAT_COLUMNS: list[str] = [
    col
    for cols in PLAYER_STAT_COLUMNS.values()
    for col in cols
]
