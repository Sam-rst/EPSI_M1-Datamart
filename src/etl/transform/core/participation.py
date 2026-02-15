"""Build participation tables: GamePlayer, GameTeam."""

import pandas as pd

from src.etl.transform.config.columns import (
    GAME_PLAYER_META_COLUMNS,
    GAME_TEAM_META_COLUMNS,
)
from src.etl.transform.utils import dedup


def build_game_players(df_games_by_players: pd.DataFrame) -> pd.DataFrame:
    """Build GamePlayer table from games_by_players.csv."""
    df = df_games_by_players[GAME_PLAYER_META_COLUMNS].copy()
    df["car_id"] = df["car_id"].astype(str).str.replace(r"\.0$", "", regex=True).replace("nan", None)
    df["winner"] = df["winner"].map({True: True, False: False, "True": True, "False": False})
    df = dedup(df, ["game_id", "player_id"])
    return df


def build_game_teams(df_games_by_teams: pd.DataFrame) -> pd.DataFrame:
    """Build GameTeam table from games_by_teams.csv."""
    df = df_games_by_teams[GAME_TEAM_META_COLUMNS].copy()
    df["winner"] = df["winner"].map({True: True, False: False, "True": True, "False": False})
    df["core_goals"] = pd.to_numeric(df["core_goals"], errors="coerce").astype("Int64")
    df = dedup(df, ["game_id", "team_id"])
    return df
