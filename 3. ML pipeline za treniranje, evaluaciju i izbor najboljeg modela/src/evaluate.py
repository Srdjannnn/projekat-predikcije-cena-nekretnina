

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def calculate_mae(y_true: pd.Series, y_pred: np.ndarray) -> float:
    """Calculate mean absolute error."""
    return float(mean_absolute_error(y_true, y_pred))


def calculate_rmse(y_true: pd.Series, y_pred: np.ndarray) -> float:
    """Calculate root mean squared error."""
    mse = mean_squared_error(y_true, y_pred)
    return float(np.sqrt(mse))


def calculate_r2(y_true: pd.Series, y_pred: np.ndarray) -> float:
    """Calculate R-squared score."""
    return float(r2_score(y_true, y_pred))


def evaluate_model(
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, float]:
    """Evaluate a trained model and return MAE, RMSE, and R2 metrics."""
    predictions = model.predict(X_test)
    return {
        "mae": calculate_mae(y_test, predictions),
        "rmse": calculate_rmse(y_test, predictions),
        "r2": calculate_r2(y_test, predictions),
    }

