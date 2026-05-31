

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = [
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

CRITICAL_COLUMNS = ["price", "area", "rooms"]


def validate_required_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Validate that all columns needed by the preprocessing pipeline exist."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    return df.copy()


def _validate_positive_numeric(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Coerce a column to numeric values and keep only positive non-null rows."""
    validated = df.copy()
    before_count = len(validated)
    validated[column] = pd.to_numeric(validated[column], errors="coerce")
    validated = validated[validated[column].notna() & (validated[column] > 0)]
    removed_count = before_count - len(validated)
    if removed_count:
        logger.info("Removed %s rows with invalid %s", removed_count, column)
    return validated


def validate_price(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows where price is missing, non-numeric, or less than or equal to zero."""
    return _validate_positive_numeric(df, "price")


def validate_area(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows where area is missing, non-numeric, or less than or equal to zero."""
    return _validate_positive_numeric(df, "area")


def validate_rooms(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows where rooms is missing, non-numeric, or less than or equal to zero."""
    return _validate_positive_numeric(df, "rooms")


def run_validation(df: pd.DataFrame) -> pd.DataFrame:
    """Run all validation rules and return a filtered DataFrame."""
    logger.info("Rows before validation: %s", len(df))
    validated = validate_required_columns(df)
    validated = validated.dropna(subset=CRITICAL_COLUMNS)
    validated = validate_price(validated)
    validated = validate_area(validated)
    validated = validate_rooms(validated)
    validated = validated.reset_index(drop=True)
    logger.info("Rows after validation: %s", len(validated))
    return validated

