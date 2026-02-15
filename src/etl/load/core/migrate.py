"""Apply Alembic migrations to create/update the schema."""

import subprocess
import sys

from src.config import ROOT_DIR


def apply_migrations() -> None:
    """Run alembic upgrade head to ensure schema is up to date."""
    subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=ROOT_DIR,
        check=True,
    )
