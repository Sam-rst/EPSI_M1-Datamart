"""Populate star schema dimensions from 3NF tables via SQL INSERT INTO ... SELECT."""

from sqlalchemy import text

from src.database.engine import engine


def _execute_and_count(insert_sql: str, table_name: str) -> int:
    """Execute an INSERT SQL and return the row count of the target table."""
    with engine.connect() as conn:
        conn.execute(text(insert_sql))
        conn.commit()
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        return result.scalar()


def populate_dim_date() -> int:
    """Populate dim_date from distinct game dates."""
    return _execute_and_count("""
        INSERT INTO dim_date (date_key, full_date, year, month, day,
                              day_of_week, day_name, month_name, quarter,
                              is_weekend, week_of_year)
        SELECT
            ROW_NUMBER() OVER (ORDER BY d) AS date_key,
            CAST(d AS VARCHAR) AS full_date,
            YEAR(d) AS year,
            MONTH(d) AS month,
            DAY(d) AS day,
            DAYOFWEEK(d) AS day_of_week,
            DAYNAME(d) AS day_name,
            MONTHNAME(d) AS month_name,
            QUARTER(d) AS quarter,
            DAYOFWEEK(d) IN (0, 6) AS is_weekend,
            WEEKOFYEAR(d) AS week_of_year
        FROM (
            SELECT DISTINCT CAST(game_date AS DATE) AS d
            FROM game
            WHERE TRY_CAST(game_date AS DATE) IS NOT NULL
        ) sub
    """, "dim_date")


def populate_dim_player() -> int:
    """Populate dim_player from player + country."""
    return _execute_and_count("""
        INSERT INTO dim_player (player_key, player_id, player_tag, player_name,
                                country_id, country_name)
        SELECT
            ROW_NUMBER() OVER (ORDER BY p.player_id) AS player_key,
            p.player_id, p.player_tag, p.player_name,
            p.country_id, COALESCE(c.country_name, c.country_id) AS country_name
        FROM player p
        LEFT JOIN country c ON p.country_id = c.country_id
    """, "dim_player")


def populate_dim_team() -> int:
    """Populate dim_team from team + region."""
    return _execute_and_count("""
        INSERT INTO dim_team (team_key, team_id, team_name, region_id, region_name)
        SELECT
            ROW_NUMBER() OVER (ORDER BY t.team_id) AS team_key,
            t.team_id, t.team_name, t.region_id, COALESCE(r.region_name, r.region_id) AS region_name
        FROM team t
        LEFT JOIN region r ON t.region_id = r.region_id
    """, "dim_team")


def populate_dim_map() -> int:
    """Populate dim_map from map."""
    return _execute_and_count("""
        INSERT INTO dim_map (map_key, map_id, map_name)
        SELECT
            ROW_NUMBER() OVER (ORDER BY map_id) AS map_key,
            map_id, map_name
        FROM map
    """, "dim_map")


def populate_dim_car() -> int:
    """Populate dim_car from car."""
    return _execute_and_count("""
        INSERT INTO dim_car (car_key, car_id, car_name)
        SELECT
            ROW_NUMBER() OVER (ORDER BY car_id) AS car_key,
            car_id, car_name
        FROM car
    """, "dim_car")


def populate_dim_event() -> int:
    """Populate dim_event from match + stage + event + region (denormalized)."""
    return _execute_and_count("""
        INSERT INTO dim_event (
            event_key, match_id,
            match_slug, match_number, match_round, match_date, match_format,
            reverse_sweep_attempt, reverse_sweep,
            stage_id, stage_name, stage_step, is_lan, is_qualifier,
            location_venue, location_city, location_country,
            event_id, event_name, event_split, event_tier, event_phase, prize_money,
            event_region_id, event_region_name
        )
        SELECT
            ROW_NUMBER() OVER (ORDER BY m.match_id) AS event_key,
            m.match_id,
            m.match_slug, m.match_number, m.match_round, m.match_date, m.match_format,
            m.reverse_sweep_attempt, m.reverse_sweep,
            s.stage_id, s.stage_name, s.stage_step, s.is_lan, s.is_qualifier,
            s.location_venue, s.location_city, s.location_country,
            e.event_id, e.event_name, e.event_split, e.event_tier, e.event_phase, e.prize_money,
            r.region_id, COALESCE(r.region_name, r.region_id) AS region_name
        FROM match m
        LEFT JOIN stage s ON m.stage_id = s.stage_id
        LEFT JOIN event e ON s.event_id = e.event_id
        LEFT JOIN region r ON e.region_id = r.region_id
    """, "dim_event")


def populate_dimensions() -> dict[str, int]:
    """Populate all 6 dimensions. Returns {table_name: row_count}."""
    counts = {}
    for name, func in [
        ("dim_date", populate_dim_date),
        ("dim_player", populate_dim_player),
        ("dim_team", populate_dim_team),
        ("dim_map", populate_dim_map),
        ("dim_car", populate_dim_car),
        ("dim_event", populate_dim_event),
    ]:
        count = func()
        counts[name] = count
        print(f"  {name:<20} {count:>8,} lignes")
    return counts
