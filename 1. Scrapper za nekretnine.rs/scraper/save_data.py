from pathlib import Path
from typing import Iterable

import pandas as pd

from .config import OUTPUT_FILE
from .models import PropertyListing


CSV_COLUMNS = [
    "price",
    "area",
    "rooms",
    "city",
    "municipality",
    "floor",
    "total_floors",
    "building_year",
    "elevator",
    "terrace",
    "parking",
    "url",
]


def save_to_csv(
    listings: Iterable[PropertyListing],
    output_file: str | Path = OUTPUT_FILE,
) -> Path:
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    for listing in listings:
        row = listing.to_dict()
        rows.append({column: row.get(column) for column in CSV_COLUMNS})

    dataframe = pd.DataFrame(rows, columns=CSV_COLUMNS)
    dataframe.drop_duplicates(subset=["url"], inplace=True)
    dataframe.to_csv(output_path, index=False, encoding="utf-8")
    return output_path


def load_csv(input_file: str | Path = OUTPUT_FILE) -> pd.DataFrame:
    input_path = Path(input_file)
    if not input_path.exists():
        return pd.DataFrame(columns=CSV_COLUMNS)
    return pd.read_csv(input_path)

