from src.config import RAW_DIR
from src.etl.extract.core import ensure_raw_csvs


def run() -> None:
    """Orchestrate raw CSV extraction: download from Kaggle or skip if present."""
    print("=== Extraction des donnees brutes ===\n")

    skipped, csv_paths = ensure_raw_csvs(RAW_DIR)

    if skipped:
        print(f"CSV deja presents ({len(csv_paths)} fichiers) — telechargement ignore.")
    else:
        print(f"Fichiers copies dans {RAW_DIR} :")
        for p in csv_paths:
            print(f"  -> {p.name}")

    print(f"\n{len(csv_paths)} fichiers CSV dans {RAW_DIR}")
    print("=== Extraction terminee ===")


if __name__ == "__main__":
    run()
