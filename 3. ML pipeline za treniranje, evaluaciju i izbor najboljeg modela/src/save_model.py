
from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib


def save_model(model: Any, path: str | Path) -> Path:
    """Save a trained model to disk with joblib."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)
    return output_path


def load_model(path: str | Path) -> Any:
    """Load a trained model from disk with joblib."""
    return joblib.load(Path(path))

