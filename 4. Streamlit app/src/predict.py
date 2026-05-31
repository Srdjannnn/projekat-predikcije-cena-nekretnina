from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from .input_schema import PropertyInput

CURRENT_YEAR = date.today().year
DEFAULT_MODEL_PATH = Path("models/best_model.pkl")


def load_model(path: str | Path = DEFAULT_MODEL_PATH) -> Any:
    """Load a trained model from disk."""
    return joblib.load(Path(path))


def _feature_columns(model: Any) -> list[str]:
    """Read expected feature columns from a fitted scikit-learn model."""
    feature_names = list(getattr(model, "feature_names_in_", []))
    if not feature_names:
        raise ValueError("Model does not expose feature_names_in_; cannot align input.")
    return feature_names


def prepare_input_dataframe(user_input: PropertyInput | dict[str, Any]) -> pd.DataFrame:
    """Transform user input into base engineered features before final model alignment."""
    if isinstance(user_input, dict):
        user_input = PropertyInput(**user_input)

    total_floors = max(int(user_input.total_floors), 1)
    floor = int(user_input.floor)
    building_year = int(user_input.building_year)

    return pd.DataFrame(
        [
            {
                "area": float(user_input.area),
                "rooms": int(user_input.rooms),
                "floor": floor,
                "total_floors": total_floors,
                "building_year": building_year,
                "elevator": int(user_input.elevator),
                "terrace": int(user_input.terrace),
                "parking": int(user_input.parking),
                "building_age": np.nan
                if building_year <= 0
                else max(CURRENT_YEAR - building_year, 0),
                "floor_ratio": floor / total_floors,
                f"city_{user_input.city}": 1,
                f"municipality_{user_input.municipality}": 1,
            }
        ]
    )


def _align_to_model_features(df: pd.DataFrame, model: Any) -> pd.DataFrame:
    """Align a single-row feature DataFrame to the exact columns expected by the model."""
    feature_columns = _feature_columns(model)
    aligned = pd.DataFrame(0.0, index=df.index, columns=feature_columns)

    for column in df.columns:
        if column in aligned.columns:
            aligned[column] = df[column]

    return aligned.astype(float)


def predict_price(
    input_data: PropertyInput | dict[str, Any],
    model_path: str | Path = DEFAULT_MODEL_PATH,
) -> float:
    """Load the trained model, prepare input features, and return a price prediction."""
    model = load_model(model_path)
    base_features = prepare_input_dataframe(input_data)
    model_features = _align_to_model_features(base_features, model)
    prediction = model.predict(model_features)[0]
    return float(max(prediction, 0.0))

