"""Star schema models: 6 dimensions + 1 fact table."""

from sqlalchemy import Boolean, Double, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base


# ---------------------------------------------------------------------------
# Dimensions
# ---------------------------------------------------------------------------


class DimDate(Base):
    __tablename__ = "dim_date"

    date_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    full_date: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    year: Mapped[int | None] = mapped_column(Integer)
    month: Mapped[int | None] = mapped_column(Integer)
    day: Mapped[int | None] = mapped_column(Integer)
    day_of_week: Mapped[int | None] = mapped_column(Integer)
    day_name: Mapped[str | None] = mapped_column(String)
    month_name: Mapped[str | None] = mapped_column(String)
    quarter: Mapped[int | None] = mapped_column(Integer)
    is_weekend: Mapped[bool | None] = mapped_column(Boolean)
    week_of_year: Mapped[int | None] = mapped_column(Integer)


class DimPlayer(Base):
    __tablename__ = "dim_player"

    player_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    player_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    player_tag: Mapped[str | None] = mapped_column(String)
    player_name: Mapped[str | None] = mapped_column(String)
    country_id: Mapped[str | None] = mapped_column(String)
    country_name: Mapped[str | None] = mapped_column(String)


class DimTeam(Base):
    __tablename__ = "dim_team"

    team_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    team_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    team_name: Mapped[str | None] = mapped_column(String)
    region_id: Mapped[str | None] = mapped_column(String)
    region_name: Mapped[str | None] = mapped_column(String)


class DimMap(Base):
    __tablename__ = "dim_map"

    map_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    map_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    map_name: Mapped[str | None] = mapped_column(String)


class DimCar(Base):
    __tablename__ = "dim_car"

    car_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    car_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    car_name: Mapped[str | None] = mapped_column(String)


class DimEvent(Base):
    __tablename__ = "dim_event"

    event_key: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    match_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    # Match attributes
    match_slug: Mapped[str | None] = mapped_column(String)
    match_number: Mapped[int | None] = mapped_column(Integer)
    match_round: Mapped[str | None] = mapped_column(String)
    match_date: Mapped[str | None] = mapped_column(String)
    match_format: Mapped[str | None] = mapped_column(String)
    reverse_sweep_attempt: Mapped[bool | None] = mapped_column(Boolean)
    reverse_sweep: Mapped[bool | None] = mapped_column(Boolean)
    # Stage attributes (denormalized)
    stage_id: Mapped[str | None] = mapped_column(String)
    stage_name: Mapped[str | None] = mapped_column(String)
    stage_step: Mapped[int | None] = mapped_column(Integer)
    is_lan: Mapped[bool | None] = mapped_column(Boolean)
    is_qualifier: Mapped[bool | None] = mapped_column(Boolean)
    location_venue: Mapped[str | None] = mapped_column(String)
    location_city: Mapped[str | None] = mapped_column(String)
    location_country: Mapped[str | None] = mapped_column(String)
    # Event attributes (denormalized)
    event_id: Mapped[str | None] = mapped_column(String)
    event_name: Mapped[str | None] = mapped_column(String)
    event_split: Mapped[str | None] = mapped_column(String)
    event_tier: Mapped[str | None] = mapped_column(String)
    event_phase: Mapped[str | None] = mapped_column(String)
    prize_money: Mapped[float | None] = mapped_column(Double)
    # Event region (denormalized)
    event_region_id: Mapped[str | None] = mapped_column(String)
    event_region_name: Mapped[str | None] = mapped_column(String)


# ---------------------------------------------------------------------------
# Fact table
# ---------------------------------------------------------------------------


class FactPlayerGame(Base):
    __tablename__ = "fact_player_game"

    # Composite PK
    game_id: Mapped[str] = mapped_column(String, primary_key=True)
    player_id: Mapped[str] = mapped_column(String, primary_key=True)

    # FK to dimensions
    player_key: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("dim_player.player_key")
    )
    team_key: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("dim_team.team_key")
    )
    map_key: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("dim_map.map_key")
    )
    car_key: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("dim_car.car_key")
    )
    date_key: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("dim_date.date_key")
    )
    event_key: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("dim_event.event_key")
    )

    # Degenerate dimensions
    match_id: Mapped[str | None] = mapped_column(String)

    # Game context
    game_number: Mapped[int | None] = mapped_column(Integer)
    game_duration: Mapped[float | None] = mapped_column(Double)
    overtime: Mapped[bool | None] = mapped_column(Boolean)
    winner: Mapped[bool | None] = mapped_column(Boolean)
    color: Mapped[str | None] = mapped_column(String)
    platform: Mapped[str | None] = mapped_column(String)

    # ── CORE (6) ──
    core_shots: Mapped[float | None] = mapped_column(Double)
    core_goals: Mapped[float | None] = mapped_column(Double)
    core_saves: Mapped[float | None] = mapped_column(Double)
    core_assists: Mapped[float | None] = mapped_column(Double)
    core_score: Mapped[float | None] = mapped_column(Double)
    core_shooting_percentage: Mapped[float | None] = mapped_column(Double)

    # ── BOOST (28) ──
    boost_bpm: Mapped[float | None] = mapped_column(Double)
    boost_bcpm: Mapped[float | None] = mapped_column(Double)
    boost_avg_amount: Mapped[float | None] = mapped_column(Double)
    boost_amount_collected: Mapped[float | None] = mapped_column(Double)
    boost_amount_stolen: Mapped[float | None] = mapped_column(Double)
    boost_amount_collected_big: Mapped[float | None] = mapped_column(Double)
    boost_amount_stolen_big: Mapped[float | None] = mapped_column(Double)
    boost_amount_collected_small: Mapped[float | None] = mapped_column(Double)
    boost_amount_stolen_small: Mapped[float | None] = mapped_column(Double)
    boost_count_collected_big: Mapped[float | None] = mapped_column(Double)
    boost_count_stolen_big: Mapped[float | None] = mapped_column(Double)
    boost_count_collected_small: Mapped[float | None] = mapped_column(Double)
    boost_count_stolen_small: Mapped[float | None] = mapped_column(Double)
    boost_amount_overfill: Mapped[float | None] = mapped_column(Double)
    boost_amount_overfill_stolen: Mapped[float | None] = mapped_column(Double)
    boost_amount_used_while_supersonic: Mapped[float | None] = mapped_column(Double)
    boost_time_zero_boost: Mapped[float | None] = mapped_column(Double)
    boost_percent_zero_boost: Mapped[float | None] = mapped_column(Double)
    boost_time_full_boost: Mapped[float | None] = mapped_column(Double)
    boost_percent_full_boost: Mapped[float | None] = mapped_column(Double)
    boost_time_boost_0_25: Mapped[float | None] = mapped_column(Double)
    boost_time_boost_25_50: Mapped[float | None] = mapped_column(Double)
    boost_time_boost_50_75: Mapped[float | None] = mapped_column(Double)
    boost_time_boost_75_100: Mapped[float | None] = mapped_column(Double)
    boost_percent_boost_0_25: Mapped[float | None] = mapped_column(Double)
    boost_percent_boost_25_50: Mapped[float | None] = mapped_column(Double)
    boost_percent_boost_50_75: Mapped[float | None] = mapped_column(Double)
    boost_percent_boost_75_100: Mapped[float | None] = mapped_column(Double)

    # ── MOVEMENT (18) ──
    movement_avg_speed: Mapped[float | None] = mapped_column(Double)
    movement_total_distance: Mapped[float | None] = mapped_column(Double)
    movement_time_supersonic_speed: Mapped[float | None] = mapped_column(Double)
    movement_time_boost_speed: Mapped[float | None] = mapped_column(Double)
    movement_time_slow_speed: Mapped[float | None] = mapped_column(Double)
    movement_time_ground: Mapped[float | None] = mapped_column(Double)
    movement_time_low_air: Mapped[float | None] = mapped_column(Double)
    movement_time_high_air: Mapped[float | None] = mapped_column(Double)
    movement_time_powerslide: Mapped[float | None] = mapped_column(Double)
    movement_count_powerslide: Mapped[float | None] = mapped_column(Double)
    movement_avg_powerslide_duration: Mapped[float | None] = mapped_column(Double)
    movement_avg_speed_percentage: Mapped[float | None] = mapped_column(Double)
    movement_percent_slow_speed: Mapped[float | None] = mapped_column(Double)
    movement_percent_boost_speed: Mapped[float | None] = mapped_column(Double)
    movement_percent_supersonic_speed: Mapped[float | None] = mapped_column(Double)
    movement_percent_ground: Mapped[float | None] = mapped_column(Double)
    movement_percent_low_air: Mapped[float | None] = mapped_column(Double)
    movement_percent_high_air: Mapped[float | None] = mapped_column(Double)

    # ── POSITIONING (27) ──
    positioning_avg_distance_to_ball: Mapped[float | None] = mapped_column(Double)
    positioning_avg_distance_to_ball_possession: Mapped[float | None] = mapped_column(Double)
    positioning_avg_distance_to_ball_no_possession: Mapped[float | None] = mapped_column(Double)
    positioning_avg_distance_to_mates: Mapped[float | None] = mapped_column(Double)
    positioning_time_defensive_third: Mapped[float | None] = mapped_column(Double)
    positioning_time_neutral_third: Mapped[float | None] = mapped_column(Double)
    positioning_time_offensive_third: Mapped[float | None] = mapped_column(Double)
    positioning_time_defensive_half: Mapped[float | None] = mapped_column(Double)
    positioning_time_offensive_half: Mapped[float | None] = mapped_column(Double)
    positioning_time_behind_ball: Mapped[float | None] = mapped_column(Double)
    positioning_time_in_front_ball: Mapped[float | None] = mapped_column(Double)
    positioning_time_most_back: Mapped[float | None] = mapped_column(Double)
    positioning_time_most_forward: Mapped[float | None] = mapped_column(Double)
    positioning_goals_against_while_last_defender: Mapped[float | None] = mapped_column(Double)
    positioning_time_closest_to_ball: Mapped[float | None] = mapped_column(Double)
    positioning_time_farthest_from_ball: Mapped[float | None] = mapped_column(Double)
    positioning_percent_defensive_third: Mapped[float | None] = mapped_column(Double)
    positioning_percent_offensive_third: Mapped[float | None] = mapped_column(Double)
    positioning_percent_neutral_third: Mapped[float | None] = mapped_column(Double)
    positioning_percent_defensive_half: Mapped[float | None] = mapped_column(Double)
    positioning_percent_offensive_half: Mapped[float | None] = mapped_column(Double)
    positioning_percent_behind_ball: Mapped[float | None] = mapped_column(Double)
    positioning_percent_in_front_ball: Mapped[float | None] = mapped_column(Double)
    positioning_percent_most_back: Mapped[float | None] = mapped_column(Double)
    positioning_percent_most_forward: Mapped[float | None] = mapped_column(Double)
    positioning_percent_closest_to_ball: Mapped[float | None] = mapped_column(Double)
    positioning_percent_farthest_from_ball: Mapped[float | None] = mapped_column(Double)

    # ── DEMO (2) ──
    demo_inflicted: Mapped[float | None] = mapped_column(Double)
    demo_taken: Mapped[float | None] = mapped_column(Double)

    # ── ADVANCED (3) ──
    advanced_goal_participation: Mapped[float | None] = mapped_column(Double)
    advanced_rating: Mapped[float | None] = mapped_column(Double)
    advanced_mvp: Mapped[float | None] = mapped_column(Double)
