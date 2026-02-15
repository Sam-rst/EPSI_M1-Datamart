"""Orchestrate the full transformation: raw CSVs → 14 normalized DataFrames."""

import pandas as pd

from src.etl.transform.core import (
    build_cars,
    build_countries,
    build_events,
    build_game_players,
    build_game_teams,
    build_games,
    build_maps,
    build_matches,
    build_players,
    build_regions,
    build_stages,
    build_stat_types,
    build_stats,
    build_teams,
    export_tables,
)
from src.etl.transform.config.loading import (
    load_games_by_players,
    load_games_by_teams,
    load_main,
    load_players_db,
)


def run() -> dict[str, pd.DataFrame]:
    """Run the full transform pipeline. Returns {table_name: DataFrame}."""
    print("=== Transformation des donnees brutes ===\n")

    # Load raw CSVs
    print("Chargement des CSV...")
    df_main = load_main()
    df_players_db = load_players_db()
    df_gbp = load_games_by_players()
    df_gbt = load_games_by_teams()
    print(f"  main: {len(df_main):,} | players_db: {len(df_players_db):,}")
    print(f"  games_by_players: {len(df_gbp):,} | games_by_teams: {len(df_gbt):,}")

    # 1. Referentials
    print("\n--- Referentiels ---")
    tables: dict[str, pd.DataFrame] = {}
    tables["country"] = build_countries(df_players_db)
    tables["region"] = build_regions(df_main, df_gbt)
    tables["map"] = build_maps(df_main)
    tables["car"] = build_cars(df_gbp)
    for name in ("country", "region", "map", "car"):
        print(f"  {name}: {len(tables[name])} lignes")

    # 2. Entities
    print("\n--- Entites ---")
    tables["player"] = build_players(df_players_db)
    tables["team"] = build_teams(df_gbt)
    for name in ("player", "team"):
        print(f"  {name}: {len(tables[name])} lignes")

    # 3. Hierarchy
    print("\n--- Hierarchie ---")
    tables["event"] = build_events(df_main)
    tables["stage"] = build_stages(df_main)
    tables["match"] = build_matches(df_main)
    tables["game"] = build_games(df_main)
    for name in ("event", "stage", "match", "game"):
        print(f"  {name}: {len(tables[name])} lignes")

    # 4. Participation
    print("\n--- Participation ---")
    tables["game_player"] = build_game_players(df_gbp)
    tables["game_team"] = build_game_teams(df_gbt)
    for name in ("game_player", "game_team"):
        print(f"  {name}: {len(tables[name]):,} lignes")

    # 5. Stats (EAV)
    print("\n--- Stats (EAV unpivot) ---")
    tables["stat_type"] = build_stat_types()
    print(f"  stat_type: {len(tables['stat_type'])} lignes")
    print("  Unpivot en cours (peut prendre quelques secondes)...")
    tables["stat"] = build_stats(df_gbp, df_gbt)
    print(f"  stat: {len(tables['stat']):,} lignes")

    # 6. Export to CSV
    print("\n--- Export CSV ---")
    written = export_tables(tables)
    for p in written:
        print(f"  -> {p.name}")

    total = sum(len(df) for df in tables.values())
    print(f"\n=== Transformation terminee : {len(tables)} tables, {total:,} lignes ===")
    return tables


if __name__ == "__main__":
    run()
