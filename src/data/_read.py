import pandas as pd
from pathlib import Path


def read_metadata() -> pd.DataFrame:
    DATA_DIR = Path.cwd().parent.resolve() / "./data/final/public"
    assert DATA_DIR.exists()

    return pd.read_csv(DATA_DIR / "metadata.csv", parse_dates=['date'])
