#!/usr/bin/env python3
"""
Ingest all CSV files from data/raw/ into a DuckDB database file.
Creates `data/rl.duckdb` and a table per CSV (table name = filename without extension).
"""
from pathlib import Path
import sys

try:
    import duckdb
except Exception:
    print('❌ duckdb not installed. Run: pip install duckdb')
    sys.exit(1)

def safe_table_name(p: Path):
    return p.stem.replace('-', '_').replace(' ', '_')

def main():
    repo = Path.cwd()
    
    # Chercher les CSVs dans data/raw/
    data_dir = repo / 'data' / 'raw'
    
    # Fallback vers l'ancienne structure si nécessaire
    if not data_dir.exists():
        data_dir = repo / 'Atelier1' / 'Data'
        if not data_dir.exists():
            data_dir = repo / 'Atelier1' / 'data'
    
    if not data_dir.exists():
        print(f'❌ Dossier de données introuvable : {data_dir}')
        sys.exit(1)
    
    csvs = sorted(data_dir.glob('*.csv'))
    if not csvs:
        print(f'❌ Aucun fichier CSV trouvé dans {data_dir}')
        sys.exit(1)

    # Base de données dans data/
    db_path = repo / 'data' / 'rl.duckdb'
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    print('🚀 Ingestion des données dans DuckDB...')
    print(f'   Base de données : {db_path}')
    print(f'   Source : {data_dir}\n')
    
    conn = duckdb.connect(database=str(db_path))
    results = []
    total_rows = 0
    
    for p in csvs:
        tbl = safe_table_name(p)
        path_str = str(p).replace('\\', '/')
        try:
            conn.execute(f"CREATE OR REPLACE TABLE {tbl} AS SELECT * FROM read_csv_auto('{path_str}')")
            cnt = conn.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
            results.append({'table': tbl, 'rows': int(cnt), 'file': p.name})
            total_rows += cnt
            print(f'✓ Table {tbl:<25} créée : {cnt:>10,} lignes')
        except Exception as e:
            print(f'❌ Échec pour {p.name}: {e}')
            results.append({'table': tbl, 'error': str(e), 'file': p.name})

    conn.close()
    
    print('\n' + '=' * 60)
    print('✅ Ingestion terminée avec succès !')
    print(f'   Total : {total_rows:,} lignes importées')
    print(f'   Taille de la base : {db_path.stat().st_size / (1024*1024):.2f} MB')
    print(f'   Emplacement : {db_path}')
    print('=' * 60)

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()
