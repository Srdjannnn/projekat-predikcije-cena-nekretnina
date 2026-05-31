from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_processed_dataset(path: str | Path) -> pd.DataFrame:
    """Load the processed dataset used for charts and contextual information."""
    return pd.read_csv(Path(path))


def format_euro(value: float) -> str:
    """Format a numeric price as a Euro amount."""
    return f"{value:,.0f} \u20ac"


def get_feature_importance(model: object) -> pd.DataFrame:
    """Return feature importance table when the model exposes feature_importances_."""
    feature_names = list(getattr(model, "feature_names_in_", []))
    importances = getattr(model, "feature_importances_", None)
    if importances is None or not feature_names:
        return pd.DataFrame(columns=["feature", "importance"])

    table = pd.DataFrame(
        {"feature": feature_names, "importance": importances}
    ).sort_values("importance", ascending=False)
    return table.reset_index(drop=True)

