
from __future__ import annotations

from typing import Any

import pandas as pd

RMSE_TIE_TOLERANCE = 0.01


def compare_models(
    results_dict: dict[str, dict[str, Any]],
) -> tuple[str, Any, pd.DataFrame]:
    """Compare models by lowest RMSE, using higher R2 as tie-breaker for close scores."""
    rows = []
    for model_name, result in results_dict.items():
        metrics = result["metrics"]
        rows.append(
            {
                "model": model_name,
                "mae": metrics["mae"],
                "rmse": metrics["rmse"],
                "r2": metrics["r2"],
            }
        )

    comparison_table = pd.DataFrame(rows).sort_values(
        by=["rmse", "r2"],
        ascending=[True, False],
    )
    best_row = comparison_table.iloc[0]
    best_rmse = float(best_row["rmse"])

    close_candidates = comparison_table[
        comparison_table["rmse"] <= best_rmse * (1 + RMSE_TIE_TOLERANCE)
    ].sort_values(by=["r2", "rmse"], ascending=[False, True])

    selected_name = str(close_candidates.iloc[0]["model"])
    selected_model = results_dict[selected_name]["model"]
    return selected_name, selected_model, comparison_table.reset_index(drop=True)

