"""Table insertion order respecting FK constraints, and Model mapping."""

from src.database.models import (
    Car,
    Country,
    Event,
    Game,
    GamePlayer,
    GameTeam,
    Map,
    Match,
    Player,
    Region,
    Stage,
    Stat,
    StatType,
    Team,
)

# Ordered by FK dependencies: parents first, children last.
TABLE_ORDER: list[tuple[str, type]] = [
    ("country", Country),
    ("region", Region),
    ("map", Map),
    ("car", Car),
    ("player", Player),
    ("team", Team),
    ("event", Event),
    ("stage", Stage),
    ("match", Match),
    ("game", Game),
    ("game_player", GamePlayer),
    ("game_team", GameTeam),
    ("stat_type", StatType),
    ("stat", Stat),
]

# Large tables that need chunked insertion.
CHUNK_SIZE = 100_000
LARGE_TABLES = {"stat"}
