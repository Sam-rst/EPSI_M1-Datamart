"""Functions to load raw CSVs into DataFrames."""

from pathlib import Path

import pandas as pd

from src.config import RAW_DIR


def load_main(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    return pd.read_csv(raw_dir / "main.csv", dtype=str)


def load_players_db(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    return pd.read_csv(raw_dir / "players_db.csv", dtype=str)


def load_games_by_players(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    return pd.read_csv(raw_dir / "games_by_players.csv", low_memory=False)


def load_games_by_teams(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    return pd.read_csv(raw_dir / "games_by_teams.csv", low_memory=False)
