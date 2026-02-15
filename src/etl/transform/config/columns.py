"""Column mappings between raw CSVs and the 3NF model."""

# ---------------------------------------------------------------------------
# main.csv  →  Event / Stage / Match / Game
# ---------------------------------------------------------------------------

EVENT_COLUMNS = {
    "event_id": "event_id",
    "event": "event_name",
    "event_split": "event_split",
    "event_slug": "event_slug",
    "event_start_date": "event_start_date",
    "event_end_date": "event_end_date",
    "event_tier": "event_tier",
    "event_phase": "event_phase",
    "prize_money": "prize_money",
    "event_region": "region_id",
}

STAGE_COLUMNS = {
    "stage": "stage_name",
    "stage_step": "stage_step",
    "stage_start_date": "stage_start_date",
    "stage_end_date": "stage_end_date",
    "stage_is_lan": "is_lan",
    "stage_is_qualifier": "is_qualifier",
    "location_venue": "location_venue",
    "location_city": "location_city",
    "location_country": "location_country",
}

MATCH_COLUMNS = {
    "match_id": "match_id",
    "match_slug": "match_slug",
    "match_number": "match_number",
    "match_round": "match_round",
    "match_date": "match_date",
    "match_format": "match_format",
    "reverse_sweep_attempt": "reverse_sweep_attempt",
    "reverse_sweep": "reverse_sweep",
}

GAME_COLUMNS = {
    "game_id": "game_id",
    "match_id": "match_id",
    "map_id": "map_id",
    "game_number": "game_number",
    "game_date": "game_date",
    "game_duration": "game_duration",
    "overtime": "overtime",
    "ballchasing_id": "ballchasing_id",
}

# ---------------------------------------------------------------------------
# games_by_players.csv  →  GamePlayer metadata (non-stat columns)
# ---------------------------------------------------------------------------

GAME_PLAYER_META_COLUMNS = [
    "game_id",
    "player_id",
    "team_id",
    "car_id",
    "color",
    "winner",
    "platform",
    "platform_id",
    "steering_sensitivity",
    "camera_fov",
    "camera_height",
    "camera_pitch",
    "camera_distance",
    "camera_stiffness",
    "camera_swivel_speed",
    "camera_transition_speed",
]

# ---------------------------------------------------------------------------
# games_by_teams.csv  →  GameTeam metadata (non-stat columns)
# ---------------------------------------------------------------------------

GAME_TEAM_META_COLUMNS = [
    "game_id",
    "team_id",
    "color",
    "winner",
    "core_goals",
]

# ---------------------------------------------------------------------------
# Stat columns per category  (used for EAV unpivot)
# ---------------------------------------------------------------------------

PLAYER_STAT_COLUMNS: dict[str, list[str]] = {
    "CORE": [
        "core_shots",
        "core_goals",
        "core_saves",
        "core_assists",
        "core_score",
        "core_shooting_percentage",
    ],
    "BOOST": [
        "boost_bpm",
        "boost_bcpm",
        "boost_avg_amount",
        "boost_amount_collected",
        "boost_amount_stolen",
        "boost_amount_collected_big",
        "boost_amount_stolen_big",
        "boost_amount_collected_small",
        "boost_amount_stolen_small",
        "boost_count_collected_big",
        "boost_count_stolen_big",
        "boost_count_collected_small",
        "boost_count_stolen_small",
        "boost_amount_overfill",
        "boost_amount_overfill_stolen",
        "boost_amount_used_while_supersonic",
        "boost_time_zero_boost",
        "boost_percent_zero_boost",
        "boost_time_full_boost",
        "boost_percent_full_boost",
        "boost_time_boost_0_25",
        "boost_time_boost_25_50",
        "boost_time_boost_50_75",
        "boost_time_boost_75_100",
        "boost_percent_boost_0_25",
        "boost_percent_boost_25_50",
        "boost_percent_boost_50_75",
        "boost_percent_boost_75_100",
    ],
    "MOVEMENT": [
        "movement_avg_speed",
        "movement_total_distance",
        "movement_time_supersonic_speed",
        "movement_time_boost_speed",
        "movement_time_slow_speed",
        "movement_time_ground",
        "movement_time_low_air",
        "movement_time_high_air",
        "movement_time_powerslide",
        "movement_count_powerslide",
        "movement_avg_powerslide_duration",
        "movement_avg_speed_percentage",
        "movement_percent_slow_speed",
        "movement_percent_boost_speed",
        "movement_percent_supersonic_speed",
        "movement_percent_ground",
        "movement_percent_low_air",
        "movement_percent_high_air",
    ],
    "POSITIONING": [
        "positioning_avg_distance_to_ball",
        "positioning_avg_distance_to_ball_possession",
        "positioning_avg_distance_to_ball_no_possession",
        "positioning_avg_distance_to_mates",
        "positioning_time_defensive_third",
        "positioning_time_neutral_third",
        "positioning_time_offensive_third",
        "positioning_time_defensive_half",
        "positioning_time_offensive_half",
        "positioning_time_behind_ball",
        "positioning_time_in_front_ball",
        "positioning_time_most_back",
        "positioning_time_most_forward",
        "positioning_goals_against_while_last_defender",
        "positioning_time_closest_to_ball",
        "positioning_time_farthest_from_ball",
        "positioning_percent_defensive_third",
        "positioning_percent_offensive_third",
        "positioning_percent_neutral_third",
        "positioning_percent_defensive_half",
        "positioning_percent_offensive_half",
        "positioning_percent_behind_ball",
        "positioning_percent_in_front_ball",
        "positioning_percent_most_back",
        "positioning_percent_most_forward",
        "positioning_percent_closest_to_ball",
        "positioning_percent_farthest_from_ball",
    ],
    "DEMO": [
        "demo_inflicted",
        "demo_taken",
    ],
    "ADVANCED": [
        "advanced_goal_participation",
        "advanced_rating",
        "advanced_mvp",
    ],
}

TEAM_STAT_COLUMNS: dict[str, list[str]] = {
    "BALL": [
        "ball_possession_time",
        "ball_time_in_side",
    ],
    "CORE": [
        "core_shots",
        "core_goals",
        "core_saves",
        "core_assists",
        "core_score",
        "core_shooting_percentage",
    ],
    "BOOST": [
        "boost_bpm",
        "boost_bcpm",
        "boost_avg_amount",
        "boost_amount_collected",
        "boost_amount_stolen",
        "boost_amount_collected_big",
        "boost_amount_stolen_big",
        "boost_amount_collected_small",
        "boost_amount_stolen_small",
        "boost_count_collected_big",
        "boost_count_stolen_big",
        "boost_count_collected_small",
        "boost_count_stolen_small",
        "boost_amount_overfill",
        "boost_amount_overfill_stolen",
        "boost_amount_used_while_supersonic",
        "boost_time_zero_boost",
        "boost_time_full_boost",
        "boost_time_boost_0_25",
        "boost_time_boost_25_50",
        "boost_time_boost_50_75",
        "boost_time_boost_75_100",
    ],
    "MOVEMENT": [
        "movement_total_distance",
        "movement_time_supersonic_speed",
        "movement_time_boost_speed",
        "movement_time_slow_speed",
        "movement_time_ground",
        "movement_time_low_air",
        "movement_time_high_air",
        "movement_time_powerslide",
        "movement_count_powerslide",
    ],
    "POSITIONING": [
        "positioning_time_defensive_third",
        "positioning_time_neutral_third",
        "positioning_time_offensive_third",
        "positioning_time_defensive_half",
        "positioning_time_offensive_half",
        "positioning_time_behind_ball",
        "positioning_time_in_front_ball",
    ],
    "DEMO": [
        "demo_inflicted",
        "demo_taken",
    ],
}


def all_stat_columns() -> dict[str, str]:
    """Return {stat_name: category} for all unique stat names (player + team)."""
    result: dict[str, str] = {}
    for category, cols in PLAYER_STAT_COLUMNS.items():
        for col in cols:
            result[col] = category
    for category, cols in TEAM_STAT_COLUMNS.items():
        for col in cols:
            result.setdefault(col, category)
    return result
