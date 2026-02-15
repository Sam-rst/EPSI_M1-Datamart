"""Build EAV stat tables: StatType, Stat (wide-to-tall unpivot)."""

import uuid

import pandas as pd

from src.etl.transform.config.columns import (
    PLAYER_STAT_COLUMNS,
    TEAM_STAT_COLUMNS,
    all_stat_columns,
)


def build_stat_types() -> pd.DataFrame:
    """Build StatType dimension from column name conventions."""
    mapping = all_stat_columns()
    rows = [
        {"type_id": name, "stat_name": name, "category": category}
        for name, category in mapping.items()
    ]
    return pd.DataFrame(rows)


def _unpivot_stats(
    df: pd.DataFrame,
    id_col: str,
    entity_type: str,
    stat_columns: dict[str, list[str]],
) -> pd.DataFrame:
    """Unpivot stat columns from wide to tall EAV format."""
    all_cols = [col for cols in stat_columns.values() for col in cols]
    # Keep only rows that have at least the id and game_id
    keep_cols = ["game_id", id_col] + [c for c in all_cols if c in df.columns]
    df_sub = df[keep_cols].copy()

    melted = df_sub.melt(
        id_vars=["game_id", id_col],
        value_vars=[c for c in all_cols if c in df.columns],
        var_name="type_id",
        value_name="value",
    )

    # Drop rows where value is NaN
    melted = melted.dropna(subset=["value"])

    melted["stat_id"] = [str(uuid.uuid4()) for _ in range(len(melted))]
    melted["entity_id"] = melted[id_col]
    melted["entity_type"] = entity_type
    melted["value"] = pd.to_numeric(melted["value"], errors="coerce")
    melted = melted.dropna(subset=["value"])

    return melted[["stat_id", "entity_id", "entity_type", "game_id", "type_id", "value"]]


def build_player_stats(df_games_by_players: pd.DataFrame) -> pd.DataFrame:
    """Unpivot player-level stats from games_by_players.csv."""
    return _unpivot_stats(df_games_by_players, "player_id", "player", PLAYER_STAT_COLUMNS)


def build_team_stats(df_games_by_teams: pd.DataFrame) -> pd.DataFrame:
    """Unpivot team-level stats from games_by_teams.csv."""
    return _unpivot_stats(df_games_by_teams, "team_id", "team", TEAM_STAT_COLUMNS)


def build_stats(
    df_games_by_players: pd.DataFrame,
    df_games_by_teams: pd.DataFrame,
) -> pd.DataFrame:
    """Build full Stat table (player + team stats combined)."""
    player_stats = build_player_stats(df_games_by_players)
    team_stats = build_team_stats(df_games_by_teams)
    return pd.concat([player_stats, team_stats], ignore_index=True)
