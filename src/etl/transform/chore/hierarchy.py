"""Build hierarchy tables: Event, Stage, Match, Game (from main.csv)."""

import pandas as pd

from src.etl.transform.config.columns import (
    EVENT_COLUMNS,
    GAME_COLUMNS,
    MATCH_COLUMNS,
    STAGE_COLUMNS,
)
from src.etl.transform.utils import (
    cast_boolean,
    cast_integer,
    cast_numeric,
    dedup,
    rename_columns,
)


def build_events(df_main: pd.DataFrame) -> pd.DataFrame:
    """Extract unique events from main.csv."""
    df = rename_columns(df_main, EVENT_COLUMNS)
    df["region_id"] = df["region_id"].str.strip().str.upper()
    df = cast_numeric(df, ["prize_money"])
    df = dedup(df, ["event_id"])
    return df


def build_stages(df_main: pd.DataFrame) -> pd.DataFrame:
    """Extract unique stages from main.csv. Synthesizes stage_id."""
    # Build stage_id from event_id + stage_step (unique combo)
    df = df_main.copy()
    df["stage_id"] = df["event_id"].astype(str) + "_" + df["stage_step"].astype(str)
    df["event_id"] = df["event_id"]

    stage_cols = {"stage_id": "stage_id", "event_id": "event_id"}
    stage_cols.update(STAGE_COLUMNS)
    df = rename_columns(df, stage_cols)

    df = cast_boolean(df, ["is_lan", "is_qualifier"])
    df = cast_integer(df, ["stage_step"])
    df = dedup(df, ["stage_id"])
    return df


def build_matches(df_main: pd.DataFrame) -> pd.DataFrame:
    """Extract unique matches from main.csv. Links to stage_id."""
    df = df_main.copy()
    df["stage_id"] = df["event_id"].astype(str) + "_" + df["stage_step"].astype(str)

    match_cols = {**MATCH_COLUMNS, "stage_id": "stage_id"}
    df = rename_columns(df, match_cols)

    df = cast_boolean(df, ["reverse_sweep_attempt", "reverse_sweep"])
    df = cast_integer(df, ["match_number"])
    df = dedup(df, ["match_id"])
    return df


def build_games(df_main: pd.DataFrame) -> pd.DataFrame:
    """Extract unique games from main.csv."""
    df = rename_columns(df_main, GAME_COLUMNS)
    df = cast_boolean(df, ["overtime"])
    df = cast_numeric(df, ["game_duration"])
    df = cast_integer(df, ["game_number"])
    df = dedup(df, ["game_id"])
    return df
