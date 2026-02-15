PRIMARY_KEYS: dict[str, list[str]] = {
    "main.csv": ["game_id"],
    "players_db.csv": ["player_id"],
    "games_by_players.csv": ["game_id", "player_id"],
    "games_by_teams.csv": ["game_id", "team_id"],
    "matches_by_players.csv": ["match_id", "player_id"],
    "matches_by_teams.csv": ["match_id", "team_id"],
}
