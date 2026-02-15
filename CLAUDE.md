# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Data engineering project in 3 workshops: raw Rocket League esports data (Kaggle/octane.gg) -> normalized relational model (3NF) -> star schema -> BI dashboard.

Pipeline: `CSV (data/raw/) -> SQLAlchemy ORM + Alembic -> DuckDB (3NF) -> Star schema (fact_ + dim_) -> Notebook dashboard`

## Commands

```bash
# Setup
uv sync                          # Install dependencies (uses uv package manager)
cp .env.example .env             # Configure environment (LOAD_METHOD=orm|copy)

# Full ETL pipeline (CLI)
uv run python -m src.etl                 # Run entire pipeline (extract -> transform -> load)
uv run python -m src.etl.extract         # Download Kaggle CSVs -> data/raw/
uv run python -m src.etl.transform       # Normalize to 14 tables -> data/processed/
uv run python -m src.etl.load            # Load into DuckDB -> data/rl.duckdb
uv run python -m src.etl.star            # Build star schema (6 dims + 1 fact)

# Migrations
uv run alembic upgrade head      # Apply all migrations
uv run alembic history           # View migration history
uv run alembic revision -m "msg" # Create new migration (manual, autogenerate not supported with DuckDB)
uv run alembic downgrade -1      # Rollback last migration

# Run notebooks
jupyter notebook                 # Or open .ipynb files in VS Code

# Database
# DuckDB database file: data/rl.duckdb (gitignored)
# Python: from src.database import engine, SessionLocal
```

## Stack

- **Python 3.13** with uv for dependency management
- **SQLAlchemy 2.0** ORM (DeclarativeBase, mapped_column) for models
- **Alembic** for database migrations (manual revisions, autogenerate incompatible with DuckDB)
- **DuckDB** for storage and querying (in-process, no server, via duckdb-engine)
- **pandas / matplotlib / seaborn** for data manipulation and visualization
- **python-dotenv** for environment configuration (`.env`)
- **Jupyter notebooks** for orchestration and presentation
- No backend server - everything runs client-side or in notebooks

## Project Structure

```
src/
├── config.py                  # ROOT_DIR, DATA_DIR, RAW_DIR, PROCESSED_DIR, DB_PATH, DATABASE_URL + load_dotenv()
├── database/
│   ├── engine.py              # SQLAlchemy engine + SessionLocal
│   └── models/
│       ├── base.py            # DeclarativeBase
│       ├── referentials.py    # Country, Region, Map, Car
│       ├── entities.py        # Player, Team
│       ├── hierarchy.py       # Event, Stage, Match, Game
│       ├── participation.py   # GamePlayer, GameTeam
│       ├── stats.py           # StatType, Stat (polymorphic EAV)
│       └── star.py            # DimDate, DimPlayer, DimTeam, DimMap, DimCar, DimEvent, FactPlayerGame
└── etl/
    ├── main.py                # Full pipeline orchestrator (extract -> transform -> load)
    ├── extract/               # Kaggle download + validation
    │   ├── core/              # download, copy, ensure (idempotent)
    │   ├── config/            # datasets, primary keys
    │   └── utils/             # inventory, validation
    ├── transform/             # Raw CSVs -> 14 normalized DataFrames
    │   ├── core/              # referentials, entities, hierarchy, participation, stats, export
    │   ├── config/            # column mappings (89+ stat definitions), CSV loaders
    │   └── utils/             # cleaning (dedup, cast), mapping
    ├── load/                  # Processed CSVs -> DuckDB (ORM or native COPY)
    │   ├── core/              # migrate (alembic), truncate, insert (ORM), copy (native DuckDB)
    │   ├── config/            # table order (FK-aware), chunk size, settings (LOAD_METHOD from .env)
    │   └── utils/             # CSV readers
    └── star/                  # Star schema (3NF -> star)
        ├── core/              # dimensions, fact (EAV pivot), truncate
        ├── config/            # stat columns, table order
        └── utils/             # SQL pivot helper
alembic/
├── env.py                     # Imports Base.metadata, registers DuckDB dialect
└── versions/                  # Migration files (2: initial 14 tables + star schema 7 tables)
notebooks/
├── 01_raw_extraction.ipynb    # Extract: Kaggle download + validation
├── 02_transform.ipynb         # Transform: normalize to 14 3NF tables
├── 03_load.ipynb              # Load: insert into DuckDB + SQL verification
├── 04_star_schema.ipynb       # Star: 3NF -> star schema + verification + BI queries
└── 05_dashboard.ipynb         # Dashboard BI: 7 KPIs + ipywidgets filters + CSV export
data/
├── raw/                       # 6 raw CSVs from Kaggle (gitignored)
├── processed/                 # 14 normalized CSVs (gitignored)
├── exports/                   # CSV exports from dashboard (gitignored)
└── rl.duckdb                  # DuckDB database (gitignored)
docs/
├── ateliers/                  # Atelier PDFs + RESUME.md per workshop
└── database/schemas/
    ├── ERD/                   # 3NF schema (schema_3nf.mmd, .dbml, .png, .svg)
    └── star/                  # Star schema (schema_star.mmd, .dbml, .png)
```

## Data Files (data/raw/)

| File | Rows | Description |
|------|------|-------------|
| `main.csv` | ~18.7k | Game-level data: events, stages, matches, maps, durations |
| `games_by_players.csv` | ~106k | Per-player per-game stats (shots, goals, saves, boost, movement, positioning, demos) |
| `games_by_teams.csv` | ~35.5k | Per-team per-game aggregated stats |
| `matches_by_players.csv` | ~26k | Per-player per-match aggregated stats |
| `matches_by_teams.csv` | ~10.5k | Per-team per-match aggregated stats |
| `players_db.csv` | ~1.2k | Player registry (id, tag, name, country) |

Key join columns: `game_id`, `match_id`, `player_id`, `team_id`. Colors are `blue`/`orange`.

## Conventions

- All table/column names in `snake_case`
- SQLAlchemy models in `src/database/models/`, grouped by domain
- Migrations in `alembic/versions/` (manual, not autogenerated)
- Fact tables prefixed `fact_`, dimensions prefixed `dim_` (Atelier 2)
- ETL modules follow `core/` (business logic), `config/` (constants), `utils/` (helpers) pattern
- Each ETL stage has a `main.py` orchestrator and a `__main__.py` CLI entry point
- Database dialect: DuckDB SQL
- Database file: `data/rl.duckdb` (gitignored)
- Raw data: `data/raw/` (gitignored)
- Processed data: `data/processed/` (gitignored, 14 CSVs output by transform)
- Environment config: `.env` (gitignored), `.env.example` (committed)
- Load method: `LOAD_METHOD=orm` (ORM bulk insert) or `LOAD_METHOD=copy` (DuckDB native read_csv, ~20x faster)

## Relational Model (Workshop 1) — 14 Tables

5 groups:
- **Referentials**: Country, Region, Map, Car
- **Entities**: Player (FK country), Team (FK region)
- **Hierarchy**: Event > Stage > Match > Game (FK chain)
- **Participation**: GamePlayer (composite PK game+player, FK team+car), GameTeam (composite PK game+team)
- **Stats (EAV)**: StatType (name, category), Stat (entity_id + entity_type polymorphic, FK game + type)

Stat uses polymorphic `entity_id` + `entity_type` (player/team) to link stats at game-level only. Match-level stats are derived via Game.match_id aggregation.

## Star Schema (Workshop 2) — 7 Tables

6 dimensions + 1 fact table. Grain: 1 player x 1 game (~106k rows).

- **DimDate**: date_key PK, full_date, year/month/day, day_of_week, day_name, quarter, is_weekend
- **DimPlayer**: player_key PK, player_id, player_tag, player_name, country_id/name (denorm)
- **DimTeam**: team_key PK, team_id, team_name, region_id/name (denorm)
- **DimMap**: map_key PK, map_id, map_name
- **DimCar**: car_key PK, car_id, car_name
- **DimEvent**: event_key PK, match_id + match/stage/event attrs denormalized (25 cols)
- **FactPlayerGame**: (game_id, player_id) composite PK, 6 FK dims, game context, 84 stat measures

Surrogate keys generated via `ROW_NUMBER()`. Stats pivoted from EAV via `MAX(CASE WHEN)`.
CLI: `uv run python -m src.etl.star`

## KPIs (Workshop 3) — 7 indicators in `05_dashboard.ipynb`

Simple aggregations (3): overtime rate, avg score per player, total games count.
Cross-measures with charts (4): win rate by car (barh), avg score by event tier (bar), games per month (line), goals by map x color (heatmap).
Interactive filters (2): event_tier + event_region_name dropdowns (ipywidgets).
CSV export: button → `data/exports/dashboard_export.csv`.

## Agents

Four specialized agents in `.claude/agents/`:
- `@dm`: `data-modeler.md` — DDL, ERD, schema design (3NF + star)
- `@de`: `etl-engineer.md` — Data loading, transformation, integrity checks
- `@da`: `bi-visualization.md` — KPIs, charts, filters, CSV export
- `@rv`: `quality-reviewer.md` — Checklists per workshop, code quality review
