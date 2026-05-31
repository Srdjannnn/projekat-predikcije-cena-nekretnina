from __future__ import annotations

from pathlib import Path

import pandas as pd


def save_dataframe(df: pd.DataFrame, path: str | Path) -> Path:
    """Save a DataFrame as a UTF-8 CSV file and create parent folders if needed."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")
    return output_path


def load_dataframe(path: str | Path) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(Path(path))


def print_dataset_info(df: pd.DataFrame) -> None:
    """Print shape, columns, missing values, and dtypes for quick inspection."""
    print(f"Shape: {df.shape}")
    print("Columns:")
    print(", ".join(df.columns))
    print("\nMissing values:")
    print(df.isna().sum().to_string())
    print("\nDtypes:")
    print(df.dtypes.to_string())


def generate_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Generate summary statistics for numeric columns in a DataFrame."""
    return df.describe(include="all").transpose()

