"""Star schema table order (dimensions first, then fact)."""

from src.database.models.star import (
    DimCar,
    DimDate,
    DimEvent,
    DimMap,
    DimPlayer,
    DimTeam,
    FactPlayerGame,
)

# Ordered: dimensions first (no FK between them), fact last.
STAR_TABLE_ORDER: list[tuple[str, type]] = [
    ("dim_date", DimDate),
    ("dim_player", DimPlayer),
    ("dim_team", DimTeam),
    ("dim_map", DimMap),
    ("dim_car", DimCar),
    ("dim_event", DimEvent),
    ("fact_player_game", FactPlayerGame),
]
