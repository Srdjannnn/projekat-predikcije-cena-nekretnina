from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import pandas as pd

from .data_validation import run_validation
from .features import prepare_features
from .utils import load_dataframe, save_dataframe

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

NUMERIC_COLUMNS = [
    "price",
    "area",
    "rooms",
    "floor",
    "total_floors",
    "building_year",
]
TEXT_COLUMNS = ["city", "municipality", "url"]
BINARY_COLUMNS = ["elevator", "terrace", "parking"]


def load_dataset(path: str | Path) -> pd.DataFrame:
    """Load a raw CSV dataset from disk."""
    df = load_dataframe(path)
    logger.info("Rows before preprocessing: %s", len(df))
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate listings, preferring URL-based deduplication when available."""
    before_count = len(df)
    subset = ["url"] if "url" in df.columns else None
    deduplicated = df.drop_duplicates(subset=subset).reset_index(drop=True)
    removed_count = before_count - len(deduplicated)
    logger.info("Removed duplicate rows: %s", removed_count)
    return deduplicated


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle non-critical missing values without imputing target-critical fields."""
    cleaned = df.copy()

    for column in TEXT_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].fillna("unknown")

    for column in BINARY_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].fillna(False)

    return cleaned


def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert known numeric columns to numeric dtype and normalize invalid infinities."""
    cleaned = df.copy()
    for column in NUMERIC_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    cleaned.replace([np.inf, -np.inf], np.nan, inplace=True)
    return cleaned


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Trim whitespace and normalize empty strings in known text columns."""
    cleaned = df.copy()
    for column in TEXT_COLUMNS:
        if column in cleaned.columns:
            cleaned[column] = (
                cleaned[column]
                .astype("string")
                .str.strip()
                .replace("", "unknown")
                .fillna("unknown")
            )
    return cleaned


def _iqr_bounds(series: pd.Series) -> tuple[float, float]:
    """Calculate lower and upper IQR bounds for a numeric series."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Remove price and area outliers using the IQR method."""
    cleaned = df.copy()
    before_count = len(cleaned)

    for column in ["price", "area"]:
        if column not in cleaned.columns or cleaned[column].dropna().empty:
            continue
        lower_bound, upper_bound = _iqr_bounds(cleaned[column])
        cleaned = cleaned[
            cleaned[column].between(lower_bound, upper_bound, inclusive="both")
        ]

    cleaned = cleaned.reset_index(drop=True)
    removed_count = before_count - len(cleaned)
    logger.info("Removed outlier rows: %s", removed_count)
    return cleaned


def save_processed_dataset(df: pd.DataFrame, path: str | Path) -> Path:
    """Save the processed model-ready dataset to disk."""
    output_path = save_dataframe(df, path)
    logger.info("Processed dataset saved to: %s", output_path)
    return output_path


def preprocess_data(input_path: str | Path, output_path: str | Path) -> pd.DataFrame:
    """Run validation, preprocessing, feature engineering, and save the final dataset."""
    df = load_dataset(input_path)
    df = run_validation(df)
    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = clean_numeric_columns(df)
    df = clean_text_columns(df)
    df = remove_outliers(df)
    df = prepare_features(df)
    save_processed_dataset(df, output_path)
    return df


if __name__ == "__main__":
    preprocess_data(
        input_path=Path("data/raw/dataset.csv"),
        output_path=Path("data/processed/processed_dataset.csv"),
    )
