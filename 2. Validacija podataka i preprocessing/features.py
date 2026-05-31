

from __future__ import annotations

import logging
from datetime import date

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

CURRENT_YEAR = date.today().year
BINARY_COLUMNS = ["elevator", "terrace", "parking"]
CATEGORICAL_COLUMNS = ["city", "municipality"]
IDENTIFIER_COLUMNS = ["url"]


def create_price_per_m2(df: pd.DataFrame) -> pd.DataFrame:
    """Create price_per_m2 as price divided by area."""
    featured = df.copy()
    featured["price_per_m2"] = np.where(
        featured["area"] > 0,
        featured["price"] / featured["area"],
        np.nan,
    )
    return featured


def create_building_age(df: pd.DataFrame) -> pd.DataFrame:
    """Create building_age as current year minus building_year, preserving NaN years."""
    featured = df.copy()
    building_year = pd.to_numeric(featured.get("building_year"), errors="coerce")
    featured["building_age"] = np.where(
        building_year.notna(),
        CURRENT_YEAR - building_year,
        np.nan,
    )
    featured.loc[featured["building_age"] < 0, "building_age"] = np.nan
    return featured


def create_floor_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """Create floor_ratio as floor divided by total_floors when both values are valid."""
    featured = df.copy()
    floor = pd.to_numeric(featured.get("floor"), errors="coerce")
    total_floors = pd.to_numeric(featured.get("total_floors"), errors="coerce")
    featured["floor_ratio"] = np.where(
        total_floors > 0,
        floor / total_floors,
        np.nan,
    )
    return featured


def create_binary_features(df: pd.DataFrame) -> pd.DataFrame:
    """Convert boolean amenity columns to integer 0/1 features."""
    featured = df.copy()
    truthy_values = {"true", "1", "yes", "da", "y", "t"}

    for column in BINARY_COLUMNS:
        if column in featured.columns:
            featured[column] = (
                featured[column]
                .fillna(False)
                .map(lambda value: str(value).strip().lower() in truthy_values)
                .astype(int)
            )
    return featured


def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """One-hot encode city and municipality columns using pandas get_dummies."""
    featured = df.copy()
    available_columns = [
        column for column in CATEGORICAL_COLUMNS if column in featured.columns
    ]
    if not available_columns:
        return featured

    featured[available_columns] = featured[available_columns].fillna("unknown")
    return pd.get_dummies(
        featured,
        columns=available_columns,
        prefix=available_columns,
        dummy_na=False,
        dtype=int,
    )


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Run the full feature engineering pipeline and return a model-ready DataFrame."""
    featured = create_price_per_m2(df)
    featured = create_building_age(featured)
    featured = create_floor_ratio(featured)
    featured = create_binary_features(featured)
    featured = encode_categorical_features(featured)
    featured = featured.drop(
        columns=[column for column in IDENTIFIER_COLUMNS if column in featured.columns]
    )
    logger.info("Columns after feature engineering: %s", len(featured.columns))
    return featured
