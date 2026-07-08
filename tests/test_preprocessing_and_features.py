from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
PREPROCESSING_DIR = REPO_ROOT / "2. Validacija podataka i preprocessing"
ML_SRC_DIR = REPO_ROOT / "3. ML pipeline za treniranje, evaluaciju i izbor najboljeg modela" / "src"


def load_module(module_name: str, package_name: str, package_dir: Path):
    package = types.ModuleType(package_name)
    package.__path__ = [str(package_dir)]
    sys.modules.setdefault(package_name, package)

    module_path = package_dir / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(f"{package_name}.{module_name}", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def preprocessing_modules():
    data_validation = load_module("data_validation", "preprocess_pkg", PREPROCESSING_DIR)
    features = load_module("features", "preprocess_pkg", PREPROCESSING_DIR)
    preprocessing = load_module("preprocessing", "preprocess_pkg", PREPROCESSING_DIR)
    return data_validation, features, preprocessing


def test_validate_required_columns_raises_when_columns_are_missing(preprocessing_modules):
    data_validation, _, _ = preprocessing_modules
    df = pd.DataFrame({"price": [100000], "area": [50]})

    with pytest.raises(ValueError, match="Missing required columns"):
        data_validation.validate_required_columns(df)


def test_run_validation_filters_invalid_rows_and_resets_index(preprocessing_modules):
    data_validation, _, _ = preprocessing_modules
    df = pd.DataFrame(
        {
            "price": [100000, 0, "bad", None],
            "area": [50, 40, 30, 20],
            "rooms": [2, 1, 3, 4],
            "city": ["Beograd", "Beograd", "Beograd", "Beograd"],
            "municipality": ["Savski venac", "Savski venac", "Savski venac", "Savski venac"],
            "floor": [2, 1, 3, 4],
            "total_floors": [4, 4, 4, 4],
            "building_year": [2005, 1995, 2010, 2020],
            "elevator": [False, True, False, True],
            "terrace": [False, False, True, False],
            "parking": [True, False, False, True],
            "url": ["a", "b", "c", "d"],
        }
    )

    validated = data_validation.run_validation(df)

    assert len(validated) == 1
    assert validated.iloc[0]["price"] == 100000
    assert validated.index.tolist() == [0]


def test_create_price_per_m2_divides_price_by_area(preprocessing_modules):
    _, features, _ = preprocessing_modules
    df = pd.DataFrame({"price": [100000, 50000], "area": [50, 0]})

    featured = features.create_price_per_m2(df)

    assert featured.loc[0, "price_per_m2"] == pytest.approx(2000.0)
    assert pd.isna(featured.loc[1, "price_per_m2"])


def test_create_building_age_and_binary_features_work(preprocessing_modules):
    _, features, _ = preprocessing_modules
    df = pd.DataFrame(
        {
            "building_year": [2020, 1990, 2100],
            "elevator": [True, "yes", None],
            "terrace": ["no", "1", "da"],
            "parking": ["0", "t", "false"],
        }
    )

    age_featured = features.create_building_age(df)
    binary_featured = features.create_binary_features(df)

    assert age_featured.loc[0, "building_age"] == pytest.approx(features.CURRENT_YEAR - 2020)
    assert age_featured.loc[1, "building_age"] == pytest.approx(features.CURRENT_YEAR - 1990)
    assert pd.isna(age_featured.loc[2, "building_age"])
    assert binary_featured["elevator"].tolist() == [1, 1, 0]
    assert binary_featured["terrace"].tolist() == [0, 1, 1]
    assert binary_featured["parking"].tolist() == [0, 1, 0]


def test_prepare_features_creates_engineered_columns_and_drops_url(preprocessing_modules):
    _, features, _ = preprocessing_modules
    df = pd.DataFrame(
        {
            "price": [100000],
            "area": [50],
            "rooms": [2],
            "building_year": [2010],
            "floor": [2],
            "total_floors": [4],
            "city": ["Beograd"],
            "municipality": ["Savski venac"],
            "elevator": [True],
            "terrace": [False],
            "parking": [True],
            "url": ["https://example.com"],
        }
    )

    featured = features.prepare_features(df)

    assert "url" not in featured.columns
    assert "price_per_m2" in featured.columns
    assert "building_age" in featured.columns
    assert "floor_ratio" in featured.columns
    assert "city_Beograd" in featured.columns
    assert "municipality_Savski venac" in featured.columns


def test_preprocess_data_applies_full_pipeline(preprocessing_modules, tmp_path):
    _, _, preprocessing = preprocessing_modules
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "processed.csv"

    pd.DataFrame(
        {
            "price": [100000, 0, 120000],
            "area": [50, 40, 60],
            "rooms": [2, 1, 3],
            "city": ["Beograd", "Beograd", "Beograd"],
            "municipality": ["Savski venac", "Savski venac", "Savski venac"],
            "floor": [2, 1, 3],
            "total_floors": [4, 4, 4],
            "building_year": [2005, 1995, 2010],
            "elevator": [False, True, False],
            "terrace": [False, False, True],
            "parking": [True, False, False],
            "url": ["a", "b", "c"],
        }
    ).to_csv(input_path, index=False)

    result = preprocessing.preprocess_data(input_path, output_path)

    assert output_path.exists()
    assert len(result) == 2
    assert "price_per_m2" in result.columns
