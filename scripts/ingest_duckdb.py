#!/usr/bin/env python3
"""
Ingest all CSV files found under Atelier1/data into a DuckDB database file.
Creates `Atelier1/data/rl.duckdb` and a table per CSV (table name = filename without extension).
"""
from pathlib import Path
import sys

try:
    import duckdb
except Exception:
    print('duckdb not installed')
    sys.exit(1)

def safe_table_name(p: Path):
    return p.stem.replace('-', '_').replace(' ', '_')

def main():
    repo = Path.cwd()
    data_dir = repo / 'Atelier1' / 'data'
    if not data_dir.exists():
        data_dir = repo / 'Atelier1' / 'Data'
    csvs = sorted(data_dir.rglob('*.csv'))
    if not csvs:
        print('No CSVs found under', data_dir)
        sys.exit(1)

    db_path = data_dir / 'rl.duckdb'
    conn = duckdb.connect(database=str(db_path))
    results = []
    for p in csvs:
        tbl = safe_table_name(p)
        path_str = str(p).replace('\\', '/')
        print('Ingesting', p.name, '-> table', tbl)
        try:
            conn.execute(f"CREATE OR REPLACE TABLE {tbl} AS SELECT * FROM read_csv_auto('{path_str}')")
            cnt = conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            results.append({'table': tbl, 'rows': int(cnt), 'file': str(p)})
            print(' -> rows:', cnt)
        except Exception as e:
            print('Failed to ingest', p.name, e)
            results.append({'table': tbl, 'error': str(e), 'file': str(p)})

    print('\nIngestion complete. DB at', db_path)
    for r in results:
        print(r)

if __name__ == '__main__':
    main()
