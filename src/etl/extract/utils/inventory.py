from pathlib import Path

import pandas as pd


def inventory_csv(csv_path: Path) -> dict:
    """Return metadata for a single CSV: rows, columns, size_mb, column_names."""
    size_mb = csv_path.stat().st_size / (1024 * 1024)
    with open(csv_path, "r", encoding="utf-8") as fh:
        header = fh.readline().strip().split(",")
        n_lines = sum(1 for _ in fh)
    return {
        "fichier": csv_path.name,
        "lignes": n_lines,
        "colonnes": len(header),
        "taille_mb": round(size_mb, 2),
        "column_names": header,
    }


def inventory_all(raw_dir: Path) -> pd.DataFrame:
    """Return a DataFrame inventorying all CSVs in raw_dir."""
    csv_files = sorted(raw_dir.glob("*.csv"))
    rows = [inventory_csv(f) for f in csv_files]
    return pd.DataFrame(rows).drop(columns=["column_names"])
