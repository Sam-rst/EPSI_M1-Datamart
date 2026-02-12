#!/usr/bin/env python3
"""
Run validation checks against the DuckDB database created in Atelier1/data/rl.duckdb
Outputs a JSON report of checks to Atelier1/notebooks/validation_report.json
"""
from pathlib import Path
import json
import duckdb

DB_PATH = Path('Atelier1') / 'data' / 'rl.duckdb'
OUT = Path('Atelier1') / 'notebooks' / 'validation_report.json'

checks = []

conn = duckdb.connect(database=str(DB_PATH), read_only=True)

# 1. Row counts per table
for tbl in ['games_by_players','games_by_teams','main','matches_by_players','matches_by_teams','players_db']:
    try:
        cnt = conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
    except Exception as e:
        cnt = None
    checks.append({'check':'row_count','table':tbl,'count':cnt})

# 2. Null count for key id columns
key_cols = {
    'games_by_players': ['game_id','player_id','team_id'],
    'matches_by_players': ['match_id','player_id','team_id'],
    'main': ['game_id','match_id'],
}
for tbl, cols in key_cols.items():
    for c in cols:
        try:
            nulls = conn.execute(f"SELECT SUM(CASE WHEN {c} IS NULL OR {c} = '' THEN 1 ELSE 0 END) FROM {tbl}").fetchone()[0]
        except Exception as e:
            nulls = None
        checks.append({'check':'null_count','table':tbl,'column':c,'nulls':nulls})

# 3. Referential sanity: players referenced exist in players_db
try:
    missing_players = conn.execute("SELECT COUNT(DISTINCT gp.player_id) FROM games_by_players gp LEFT JOIN players_db p ON gp.player_id = p.player_id WHERE p.player_id IS NULL").fetchone()[0]
except Exception as e:
    missing_players = None
checks.append({'check':'missing_players_in_players_db','missing_count':missing_players})

# 4. Simple distribution: distinct platforms
try:
    platforms = conn.execute("SELECT platform, COUNT(*) as c FROM games_by_players GROUP BY platform ORDER BY c DESC").fetchdf().to_dict(orient='records')
except Exception as e:
    platforms = str(e)
checks.append({'check':'platform_distribution','result':platforms})

with OUT.open('w', encoding='utf-8') as f:
    json.dump({'db':str(DB_PATH), 'checks':checks}, f, ensure_ascii=False, indent=2)

print('Validation report written to', OUT)
