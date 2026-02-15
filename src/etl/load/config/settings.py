"""Load method configuration from environment."""

import os

from dotenv import load_dotenv

load_dotenv()

LOAD_METHOD: str = os.getenv("LOAD_METHOD", "orm")
