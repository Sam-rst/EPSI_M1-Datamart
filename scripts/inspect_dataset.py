#!/usr/bin/env python3
"""
Inspecte les CSV du dossier Atelier1/Data, calcule tailles et nombres de lignes
et produit un résumé JSON + exemples (5 lignes) pour chaque fichier.
Utilise DuckDB si disponible pour lire les gros fichiers.
"""
from pathlib import Path
import json
import sys

try:
    import duckdb
except Exception:
    duckdb = None

try:
    import pandas as pd
except Exception:
    pd = None

def count_rows_stream(p: Path):
    # streaming count (fast, memory-light)
    with p.open('r', encoding='utf-8', errors='ignore') as f:
        return sum(1 for _ in f) - 1

def main():
    repo_root = Path.cwd()
    # Support both 'data' and 'Data' directory names
    candidate1 = repo_root / 'Atelier1' / 'data'
    candidate2 = repo_root / 'Atelier1' / 'Data'
    if candidate1.exists():
        data_dir = candidate1
    else:
        data_dir = candidate2
    out_dir = repo_root / 'Atelier1' / 'notebooks'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_json = out_dir / 'step1_summary.json'

    if not data_dir.exists():
        print('Data dir not found:', data_dir)
        sys.exit(1)

    csv_files = sorted(data_dir.rglob('*.csv'))
    summary = {
        'data_dir': str(data_dir),
        'files': []
    }

    conn = None
    if duckdb:
        try:
            conn = duckdb.connect(database=':memory:')
        except Exception:
            conn = None

    for p in csv_files:
        info = {'name': p.name, 'path': str(p), 'size_mb': p.stat().st_size / 1e6}
        size_mb = info['size_mb']

        # Count rows: stream for small files, DuckDB for big when available
        rows = None
        count_error = None
        try:
            if size_mb <= 50:
                rows = count_rows_stream(p)
            else:
                if conn is not None:
                    path_str = str(p).replace('\\', '/')
                    try:
                        rows = int(conn.execute(f"SELECT COUNT(*) FROM read_csv_auto('{path_str}')").fetchone()[0])
                    except Exception as e:
                        count_error = str(e)
                else:
                    count_error = 'duckdb not available; skip count for large file'
        except Exception as e:
            count_error = str(e)

        info['rows'] = rows
        if count_error:
            info['count_error'] = count_error

        # Sample: try DuckDB first (if available), else pandas (if available), else csv.reader
        sample = None
        columns = None
        sample_error = None
        try:
            if conn is not None:
                path_str = str(p).replace('\\', '/')
                df = conn.execute(f"SELECT * FROM read_csv_auto('{path_str}') LIMIT 5").fetchdf()
                columns = list(df.columns)
                sample = df.to_dict(orient='records')
            elif pd is not None:
                df = pd.read_csv(p, nrows=5)
                columns = list(df.columns)
                sample = df.to_dict(orient='records')
            else:
                import csv
                with p.open('r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.reader(f)
                    rows = []
                    for i, r in enumerate(reader):
                        rows.append(r)
                        if i >= 4:
                            break
                    sample = rows
        except Exception as e:
            sample_error = str(e)

        if columns:
            info['columns'] = columns
        if sample is not None:
            # Ensure values are JSON-serializable (convert numpy/pandas types)
            def make_serializable(v):
                try:
                    import pandas as _pd
                    import numpy as _np
                except Exception:
                    _pd = None
                    _np = None
                # pandas types
                try:
                    if _pd is not None and isinstance(v, (_pd.Timestamp, _pd.Timedelta)):
                        return str(v)
                except Exception:
                    pass
                # numpy scalar
                try:
                    if _np is not None and isinstance(v, _np.generic):
                        return v.item()
                except Exception:
                    pass
                # fallback for other non-serializable objects
                try:
                    json.dumps(v)
                    return v
                except Exception:
                    return str(v)

            if isinstance(sample, list) and sample and isinstance(sample[0], dict):
                serial = []
                for row in sample:
                    serial.append({k: make_serializable(v) for k, v in row.items()})
                info['sample'] = serial
            else:
                # sample as raw rows (list of lists)
                info['sample'] = [[make_serializable(x) for x in r] for r in sample]
        if sample_error:
            info['sample_error'] = sample_error

        summary['files'].append(info)

    # Write summary JSON
    with out_json.open('w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print('Wrote summary to', out_json)
    print('Files inspected:', len(summary['files']))

if __name__ == '__main__':
    main()
