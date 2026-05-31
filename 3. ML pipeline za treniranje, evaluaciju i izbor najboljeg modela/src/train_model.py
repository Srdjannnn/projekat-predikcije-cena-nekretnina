

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from .evaluate import evaluate_model
from .model_selection import compare_models
from .save_model import save_model

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
TARGET_COLUMN = "price"
DEFAULT_MODEL_PATH = Path("models/best_model.pkl")
DEFAULT_COMPARISON_PATH = Path("models/model_comparison.csv")
LEAKAGE_COLUMNS = ["price_per_m2"]


def train_linear_regression(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> LinearRegression:
    """Train a LinearRegression model."""
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def train_random_forest(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> RandomForestRegressor:
    """Train a RandomForestRegressor model with reproducible settings."""
    model = RandomForestRegressor(
        n_estimators=300,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        min_samples_leaf=2,
    )
    model.fit(X_train, y_train)
    return model


def train_gradient_boosting(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> GradientBoostingRegressor:
    """Train a GradientBoostingRegressor model with reproducible settings."""
    model = GradientBoostingRegressor(random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    return model


def train_all_models(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> dict[str, Any]:
    """Train all candidate models and return them by model name."""
    logger.info("Training LinearRegression")
    linear_regression = train_linear_regression(X_train, y_train)

    logger.info("Training RandomForestRegressor")
    random_forest = train_random_forest(X_train, y_train)

    logger.info("Training GradientBoostingRegressor")
    gradient_boosting = train_gradient_boosting(X_train, y_train)

    return {
        "LinearRegression": linear_regression,
        "RandomForestRegressor": random_forest,
        "GradientBoostingRegressor": gradient_boosting,
    }


def _load_training_data(data_path: str | Path) -> pd.DataFrame:
    """Load a processed CSV dataset for model training."""
    path = Path(data_path)
    if not path.exists():
        raise FileNotFoundError(f"Training dataset not found: {path}")
    return pd.read_csv(path)


def _split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Split a processed dataset into features X and target y."""
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' is missing")

    columns_to_drop = [TARGET_COLUMN] + [
        column for column in LEAKAGE_COLUMNS if column in df.columns
    ]
    X = df.drop(columns=columns_to_drop)
    y = df[TARGET_COLUMN]
    X = X.select_dtypes(include=["number", "bool"]).copy()
    X = X.fillna(X.median(numeric_only=True))
    return X, y


def run_training_pipeline(data_path: str | Path) -> dict[str, Any]:
    """Run train/test split, train models, evaluate them, and save the best model."""
    try:
        logger.info("Loading processed dataset from: %s", data_path)
        df = _load_training_data(data_path)
        logger.info("Dataset shape: %s rows, %s columns", len(df), len(df.columns))

        X, y = _split_features_target(df)
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=RANDOM_STATE,
        )
        logger.info("Train rows: %s | Test rows: %s", len(X_train), len(X_test))

        models = train_all_models(X_train, y_train)
        results: dict[str, dict[str, Any]] = {}

        for model_name, model in models.items():
            metrics = evaluate_model(model, X_test, y_test)
            results[model_name] = {"model": model, "metrics": metrics}
            logger.info("%s metrics: %s", model_name, metrics)

        best_model_name, best_model_object, comparison_table = compare_models(results)
        saved_path = save_model(best_model_object, DEFAULT_MODEL_PATH)
        DEFAULT_COMPARISON_PATH.parent.mkdir(parents=True, exist_ok=True)
        comparison_table.to_csv(DEFAULT_COMPARISON_PATH, index=False)
        logger.info("Best model: %s", best_model_name)
        logger.info("Best model saved to: %s", saved_path)
        logger.info("Model comparison saved to: %s", DEFAULT_COMPARISON_PATH)

        return {
            "best_model_name": best_model_name,
            "best_model": best_model_object,
            "comparison_table": comparison_table,
            "model_path": saved_path,
            "comparison_path": DEFAULT_COMPARISON_PATH,
        }
    except Exception:
        logger.exception("Training pipeline failed")
        raise


if __name__ == "__main__":
    pipeline_result = run_training_pipeline("data/processed/processed_dataset.csv")
    print(pipeline_result["comparison_table"].to_string(index=False))
    print(f"Best model: {pipeline_result['best_model_name']}")
