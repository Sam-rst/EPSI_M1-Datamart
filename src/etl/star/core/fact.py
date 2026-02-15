"""Populate fact_player_game via EAV pivot from 3NF tables."""

from sqlalchemy import text

from src.database.engine import engine
from src.etl.star.config.columns import FACT_STAT_COLUMNS
from src.etl.star.utils.sql import build_pivot_expressions


def populate_fact_player_game() -> int:
    """Pivot EAV stats into columnar fact table. Returns row count."""
    pivot_exprs = build_pivot_expressions(FACT_STAT_COLUMNS)
    stat_col_names = ", ".join(FACT_STAT_COLUMNS)

    sql = text(f"""
        INSERT INTO fact_player_game (
            game_id, player_id,
            player_key, team_key, map_key, car_key, date_key, event_key,
            match_id, game_number, game_duration, overtime, winner, color, platform,
            {stat_col_names}
        )
        SELECT
            gp.game_id, gp.player_id,
            dp.player_key, dt.team_key, dm.map_key, dc.car_key, dd.date_key, de.event_key,
            g.match_id, g.game_number, g.game_duration, g.overtime,
            gp.winner, gp.color, gp.platform,
            {pivot_exprs}
        FROM game_player gp
        JOIN game g ON gp.game_id = g.game_id
        LEFT JOIN stat s
            ON s.entity_id = gp.player_id
            AND s.game_id = gp.game_id
            AND s.entity_type = 'player'
        LEFT JOIN stat_type st ON s.type_id = st.type_id
        JOIN dim_player dp ON gp.player_id = dp.player_id
        LEFT JOIN dim_team dt ON gp.team_id = dt.team_id
        LEFT JOIN dim_map dm ON g.map_id = dm.map_id
        LEFT JOIN dim_car dc ON gp.car_id = dc.car_id
        LEFT JOIN dim_date dd ON CAST(g.game_date AS DATE)::VARCHAR = dd.full_date
        LEFT JOIN dim_event de ON g.match_id = de.match_id
        GROUP BY
            gp.game_id, gp.player_id,
            dp.player_key, dt.team_key, dm.map_key, dc.car_key, dd.date_key, de.event_key,
            g.match_id, g.game_number, g.game_duration, g.overtime,
            gp.winner, gp.color, gp.platform
    """)

    with engine.connect() as conn:
        conn.execute(sql)
        conn.commit()
        result = conn.execute(text("SELECT COUNT(*) FROM fact_player_game"))
        return result.scalar()
