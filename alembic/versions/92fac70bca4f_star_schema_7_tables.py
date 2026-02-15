"""star schema 7 tables

Revision ID: 92fac70bca4f
Revises: 6f3da4bd7748
Create Date: 2026-02-15 19:10:10.035546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92fac70bca4f'
down_revision: Union[str, Sequence[str], None] = '6f3da4bd7748'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Dimensions ──

    op.create_table(
        "dim_date",
        sa.Column("date_key", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("full_date", sa.String(), unique=True, nullable=False),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("month", sa.Integer(), nullable=True),
        sa.Column("day", sa.Integer(), nullable=True),
        sa.Column("day_of_week", sa.Integer(), nullable=True),
        sa.Column("day_name", sa.String(), nullable=True),
        sa.Column("month_name", sa.String(), nullable=True),
        sa.Column("quarter", sa.Integer(), nullable=True),
        sa.Column("is_weekend", sa.Boolean(), nullable=True),
        sa.Column("week_of_year", sa.Integer(), nullable=True),
    )

    op.create_table(
        "dim_player",
        sa.Column("player_key", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("player_id", sa.String(), unique=True, nullable=False),
        sa.Column("player_tag", sa.String(), nullable=True),
        sa.Column("player_name", sa.String(), nullable=True),
        sa.Column("country_id", sa.String(), nullable=True),
        sa.Column("country_name", sa.String(), nullable=True),
    )

    op.create_table(
        "dim_team",
        sa.Column("team_key", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("team_id", sa.String(), unique=True, nullable=False),
        sa.Column("team_name", sa.String(), nullable=True),
        sa.Column("region_id", sa.String(), nullable=True),
        sa.Column("region_name", sa.String(), nullable=True),
    )

    op.create_table(
        "dim_map",
        sa.Column("map_key", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("map_id", sa.String(), unique=True, nullable=False),
        sa.Column("map_name", sa.String(), nullable=True),
    )

    op.create_table(
        "dim_car",
        sa.Column("car_key", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("car_id", sa.String(), unique=True, nullable=False),
        sa.Column("car_name", sa.String(), nullable=True),
    )

    op.create_table(
        "dim_event",
        sa.Column("event_key", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("match_id", sa.String(), unique=True, nullable=False),
        # Match attributes
        sa.Column("match_slug", sa.String(), nullable=True),
        sa.Column("match_number", sa.Integer(), nullable=True),
        sa.Column("match_round", sa.String(), nullable=True),
        sa.Column("match_date", sa.String(), nullable=True),
        sa.Column("match_format", sa.String(), nullable=True),
        sa.Column("reverse_sweep_attempt", sa.Boolean(), nullable=True),
        sa.Column("reverse_sweep", sa.Boolean(), nullable=True),
        # Stage (denormalized)
        sa.Column("stage_id", sa.String(), nullable=True),
        sa.Column("stage_name", sa.String(), nullable=True),
        sa.Column("stage_step", sa.Integer(), nullable=True),
        sa.Column("is_lan", sa.Boolean(), nullable=True),
        sa.Column("is_qualifier", sa.Boolean(), nullable=True),
        sa.Column("location_venue", sa.String(), nullable=True),
        sa.Column("location_city", sa.String(), nullable=True),
        sa.Column("location_country", sa.String(), nullable=True),
        # Event (denormalized)
        sa.Column("event_id", sa.String(), nullable=True),
        sa.Column("event_name", sa.String(), nullable=True),
        sa.Column("event_split", sa.String(), nullable=True),
        sa.Column("event_tier", sa.String(), nullable=True),
        sa.Column("event_phase", sa.String(), nullable=True),
        sa.Column("prize_money", sa.Double(), nullable=True),
        # Event region (denormalized)
        sa.Column("event_region_id", sa.String(), nullable=True),
        sa.Column("event_region_name", sa.String(), nullable=True),
    )

    # ── Fact table ──

    op.create_table(
        "fact_player_game",
        # Composite PK
        sa.Column("game_id", sa.String(), primary_key=True),
        sa.Column("player_id", sa.String(), primary_key=True),
        # FK to dimensions
        sa.Column("player_key", sa.Integer(), sa.ForeignKey("dim_player.player_key"), nullable=True),
        sa.Column("team_key", sa.Integer(), sa.ForeignKey("dim_team.team_key"), nullable=True),
        sa.Column("map_key", sa.Integer(), sa.ForeignKey("dim_map.map_key"), nullable=True),
        sa.Column("car_key", sa.Integer(), sa.ForeignKey("dim_car.car_key"), nullable=True),
        sa.Column("date_key", sa.Integer(), sa.ForeignKey("dim_date.date_key"), nullable=True),
        sa.Column("event_key", sa.Integer(), sa.ForeignKey("dim_event.event_key"), nullable=True),
        # Degenerate dimensions
        sa.Column("match_id", sa.String(), nullable=True),
        # Game context
        sa.Column("game_number", sa.Integer(), nullable=True),
        sa.Column("game_duration", sa.Double(), nullable=True),
        sa.Column("overtime", sa.Boolean(), nullable=True),
        sa.Column("winner", sa.Boolean(), nullable=True),
        sa.Column("color", sa.String(), nullable=True),
        sa.Column("platform", sa.String(), nullable=True),
        # ── CORE (6) ──
        sa.Column("core_shots", sa.Double(), nullable=True),
        sa.Column("core_goals", sa.Double(), nullable=True),
        sa.Column("core_saves", sa.Double(), nullable=True),
        sa.Column("core_assists", sa.Double(), nullable=True),
        sa.Column("core_score", sa.Double(), nullable=True),
        sa.Column("core_shooting_percentage", sa.Double(), nullable=True),
        # ── BOOST (28) ──
        sa.Column("boost_bpm", sa.Double(), nullable=True),
        sa.Column("boost_bcpm", sa.Double(), nullable=True),
        sa.Column("boost_avg_amount", sa.Double(), nullable=True),
        sa.Column("boost_amount_collected", sa.Double(), nullable=True),
        sa.Column("boost_amount_stolen", sa.Double(), nullable=True),
        sa.Column("boost_amount_collected_big", sa.Double(), nullable=True),
        sa.Column("boost_amount_stolen_big", sa.Double(), nullable=True),
        sa.Column("boost_amount_collected_small", sa.Double(), nullable=True),
        sa.Column("boost_amount_stolen_small", sa.Double(), nullable=True),
        sa.Column("boost_count_collected_big", sa.Double(), nullable=True),
        sa.Column("boost_count_stolen_big", sa.Double(), nullable=True),
        sa.Column("boost_count_collected_small", sa.Double(), nullable=True),
        sa.Column("boost_count_stolen_small", sa.Double(), nullable=True),
        sa.Column("boost_amount_overfill", sa.Double(), nullable=True),
        sa.Column("boost_amount_overfill_stolen", sa.Double(), nullable=True),
        sa.Column("boost_amount_used_while_supersonic", sa.Double(), nullable=True),
        sa.Column("boost_time_zero_boost", sa.Double(), nullable=True),
        sa.Column("boost_percent_zero_boost", sa.Double(), nullable=True),
        sa.Column("boost_time_full_boost", sa.Double(), nullable=True),
        sa.Column("boost_percent_full_boost", sa.Double(), nullable=True),
        sa.Column("boost_time_boost_0_25", sa.Double(), nullable=True),
        sa.Column("boost_time_boost_25_50", sa.Double(), nullable=True),
        sa.Column("boost_time_boost_50_75", sa.Double(), nullable=True),
        sa.Column("boost_time_boost_75_100", sa.Double(), nullable=True),
        sa.Column("boost_percent_boost_0_25", sa.Double(), nullable=True),
        sa.Column("boost_percent_boost_25_50", sa.Double(), nullable=True),
        sa.Column("boost_percent_boost_50_75", sa.Double(), nullable=True),
        sa.Column("boost_percent_boost_75_100", sa.Double(), nullable=True),
        # ── MOVEMENT (18) ──
        sa.Column("movement_avg_speed", sa.Double(), nullable=True),
        sa.Column("movement_total_distance", sa.Double(), nullable=True),
        sa.Column("movement_time_supersonic_speed", sa.Double(), nullable=True),
        sa.Column("movement_time_boost_speed", sa.Double(), nullable=True),
        sa.Column("movement_time_slow_speed", sa.Double(), nullable=True),
        sa.Column("movement_time_ground", sa.Double(), nullable=True),
        sa.Column("movement_time_low_air", sa.Double(), nullable=True),
        sa.Column("movement_time_high_air", sa.Double(), nullable=True),
        sa.Column("movement_time_powerslide", sa.Double(), nullable=True),
        sa.Column("movement_count_powerslide", sa.Double(), nullable=True),
        sa.Column("movement_avg_powerslide_duration", sa.Double(), nullable=True),
        sa.Column("movement_avg_speed_percentage", sa.Double(), nullable=True),
        sa.Column("movement_percent_slow_speed", sa.Double(), nullable=True),
        sa.Column("movement_percent_boost_speed", sa.Double(), nullable=True),
        sa.Column("movement_percent_supersonic_speed", sa.Double(), nullable=True),
        sa.Column("movement_percent_ground", sa.Double(), nullable=True),
        sa.Column("movement_percent_low_air", sa.Double(), nullable=True),
        sa.Column("movement_percent_high_air", sa.Double(), nullable=True),
        # ── POSITIONING (27) ──
        sa.Column("positioning_avg_distance_to_ball", sa.Double(), nullable=True),
        sa.Column("positioning_avg_distance_to_ball_possession", sa.Double(), nullable=True),
        sa.Column("positioning_avg_distance_to_ball_no_possession", sa.Double(), nullable=True),
        sa.Column("positioning_avg_distance_to_mates", sa.Double(), nullable=True),
        sa.Column("positioning_time_defensive_third", sa.Double(), nullable=True),
        sa.Column("positioning_time_neutral_third", sa.Double(), nullable=True),
        sa.Column("positioning_time_offensive_third", sa.Double(), nullable=True),
        sa.Column("positioning_time_defensive_half", sa.Double(), nullable=True),
        sa.Column("positioning_time_offensive_half", sa.Double(), nullable=True),
        sa.Column("positioning_time_behind_ball", sa.Double(), nullable=True),
        sa.Column("positioning_time_in_front_ball", sa.Double(), nullable=True),
        sa.Column("positioning_time_most_back", sa.Double(), nullable=True),
        sa.Column("positioning_time_most_forward", sa.Double(), nullable=True),
        sa.Column("positioning_goals_against_while_last_defender", sa.Double(), nullable=True),
        sa.Column("positioning_time_closest_to_ball", sa.Double(), nullable=True),
        sa.Column("positioning_time_farthest_from_ball", sa.Double(), nullable=True),
        sa.Column("positioning_percent_defensive_third", sa.Double(), nullable=True),
        sa.Column("positioning_percent_offensive_third", sa.Double(), nullable=True),
        sa.Column("positioning_percent_neutral_third", sa.Double(), nullable=True),
        sa.Column("positioning_percent_defensive_half", sa.Double(), nullable=True),
        sa.Column("positioning_percent_offensive_half", sa.Double(), nullable=True),
        sa.Column("positioning_percent_behind_ball", sa.Double(), nullable=True),
        sa.Column("positioning_percent_in_front_ball", sa.Double(), nullable=True),
        sa.Column("positioning_percent_most_back", sa.Double(), nullable=True),
        sa.Column("positioning_percent_most_forward", sa.Double(), nullable=True),
        sa.Column("positioning_percent_closest_to_ball", sa.Double(), nullable=True),
        sa.Column("positioning_percent_farthest_from_ball", sa.Double(), nullable=True),
        # ── DEMO (2) ──
        sa.Column("demo_inflicted", sa.Double(), nullable=True),
        sa.Column("demo_taken", sa.Double(), nullable=True),
        # ── ADVANCED (3) ──
        sa.Column("advanced_goal_participation", sa.Double(), nullable=True),
        sa.Column("advanced_rating", sa.Double(), nullable=True),
        sa.Column("advanced_mvp", sa.Double(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("fact_player_game")
    op.drop_table("dim_event")
    op.drop_table("dim_car")
    op.drop_table("dim_map")
    op.drop_table("dim_team")
    op.drop_table("dim_player")
    op.drop_table("dim_date")
