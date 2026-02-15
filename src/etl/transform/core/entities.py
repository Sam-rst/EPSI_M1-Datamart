"""Build entity tables: Player, Team."""

import pandas as pd

from src.etl.transform.utils import dedup


def build_players(df_players_db: pd.DataFrame) -> pd.DataFrame:
    """Build Player table from players_db.csv."""
    df = df_players_db.copy()
    df = df.rename(columns={"player_country": "country_id"})
    df = dedup(df, ["player_id"])
    return df[["player_id", "player_tag", "player_name", "country_id"]]


def build_teams(df_games_by_teams: pd.DataFrame) -> pd.DataFrame:
    """Build Team table from games_by_teams.csv (deduplicated)."""
    df = df_games_by_teams[["team_id", "team_name", "team_region"]].copy()
    df = df.rename(columns={"team_region": "region_id"})
    df["region_id"] = df["region_id"].str.strip().str.upper()
    df = dedup(df, ["team_id"])
    return df[["team_id", "team_name", "region_id"]]
