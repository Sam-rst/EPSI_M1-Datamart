"""Build referential tables: Country, Region, Map, Car."""

import pandas as pd

from src.etl.transform.utils import dedup


def build_countries(df_players: pd.DataFrame) -> pd.DataFrame:
    """Extract unique countries from players_db."""
    df = df_players[["player_country"]].dropna(subset=["player_country"]).copy()
    df = df.rename(columns={"player_country": "country_id"})
    df = dedup(df, ["country_id"])
    df["country_name"] = df["country_id"]
    return df[["country_id", "country_name"]]


def build_regions(
    df_main: pd.DataFrame, df_games_by_teams: pd.DataFrame
) -> pd.DataFrame:
    """Extract unique regions from main.csv (event_region) and games_by_teams (team_region)."""
    regions_event = df_main[["event_region"]].dropna().rename(
        columns={"event_region": "region_id"}
    )
    regions_team = df_games_by_teams[["team_region"]].dropna().rename(
        columns={"team_region": "region_id"}
    )
    df = pd.concat([regions_event, regions_team], ignore_index=True)
    # Normalize: strip + uppercase
    df["region_id"] = df["region_id"].str.strip().str.upper()
    df = dedup(df, ["region_id"])
    df["region_name"] = df["region_id"]
    return df[["region_id", "region_name"]]


def build_maps(df_main: pd.DataFrame) -> pd.DataFrame:
    """Extract unique maps from main.csv."""
    df = df_main[["map_id", "map_name"]].dropna(subset=["map_id"]).copy()
    return dedup(df, ["map_id"])[["map_id", "map_name"]]


def build_cars(df_games_by_players: pd.DataFrame) -> pd.DataFrame:
    """Extract unique cars from games_by_players.csv."""
    df = df_games_by_players[["car_id", "car_name"]].dropna(subset=["car_id"]).copy()
    df["car_id"] = df["car_id"].astype(str).str.replace(r"\.0$", "", regex=True)
    return dedup(df, ["car_id"])[["car_id", "car_name"]]
