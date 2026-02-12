# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Data engineering project in 3 workshops: raw Rocket League esports data (from octane.gg) → normalized relational model → star schema → BI dashboard. The README references Valorant but the actual dataset is Rocket League.

Pipeline: `CSV (data/raw/) → Relational 3NF (DuckDB) → Star schema (fact_ + dim_) → Notebook/Web dashboard`

## Commands

```bash
# Setup
uv sync                    # Install dependencies (uses uv package manager)

# Run notebooks
jupyter notebook           # Or open .ipynb files in VS Code

# Database
# DuckDB database file: data/valorant.db (gitignored)
# Python: import duckdb; con = duckdb.connect('data/valorant.db')
```

## Stack

- **Python 3.13** with uv for dependency management
- **DuckDB** for storage and querying (in-process, no server)
- **pandas / matplotlib / seaborn** for data manipulation and visualization
- **Jupyter notebooks** for orchestration and presentation
- No backend server - everything runs client-side or in notebooks

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

## SQL & Data Conventions

- Scripts must be idempotent: `CREATE TABLE IF NOT EXISTS`, `INSERT OR IGNORE`
- All table/column names in `snake_case`
- Fact tables prefixed `fact_`, dimensions prefixed `dim_`
- Surrogate keys: `id INTEGER PRIMARY KEY AUTOINCREMENT`
- SQL scripts go in `sql/`, Python scripts in `scripts/`
- Database dialect: DuckDB SQL

## Relational Model (Workshop 1)

Entities: Player, Team, Match, Map, Score, Stat, StatType, StatMapping. Normalized to 3NF. StatMapping uses a polymorphic `entity_id` to link stats to players, teams, or matches.

## Star Schema (Workshop 2)

- **Fact table**: `fact_match_stats` (granularity: one row per player per match)
- **Dimensions**: `dim_player`, `dim_team`, `dim_map`, `dim_time`, `dim_character`
- Measures: score, duration, goals, saves, assists, shots, win (boolean), boost stats, etc.

## KPIs (Workshop 3)

Must implement at least 5 KPIs:
- 2+ simple aggregations (win rate, average duration, active players)
- 2+ cross-measures with charts (score by map/character, winrate over time)
- 2 interactive filters + CSV export

## Agents

Four specialized agents in `.claude/agents/`:
- `@dm`: `data-modeler.md` — DDL, ERD, schema design (3NF + star)
- `@de`: `etl-engineer.md` — Data loading, transformation, integrity checks
- `@da`: `bi-visualization.md` — KPIs, charts, filters, CSV export
- `@rv`: `quality-reviewer.md` — Checklists per workshop, code quality review
