from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
ML_SRC_DIR = REPO_ROOT / "3. ML pipeline za treniranje, evaluaciju i izbor najboljeg modela" / "src"


@pytest.fixture(scope="module")
def evaluation_module():
    module_name = "evaluate"
    package_name = "ml_pipeline"
    package = types.ModuleType(package_name)
    package.__path__ = [str(ML_SRC_DIR)]
    sys.modules.setdefault(package_name, package)

    module_path = ML_SRC_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(f"{package_name}.{module_name}", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_calculate_metrics_return_expected_values(evaluation_module):
    y_true = pd.Series([1.0, 2.0, 3.0])
    y_pred = np.array([1.0, 2.0, 4.0])

    metrics = {
        "mae": evaluation_module.calculate_mae(y_true, y_pred),
        "rmse": evaluation_module.calculate_rmse(y_true, y_pred),
        "r2": evaluation_module.calculate_r2(y_true, y_pred),
    }

    assert metrics["mae"] == pytest.approx(0.3333333333)
    assert metrics["rmse"] == pytest.approx(0.5773502692)
    assert metrics["r2"] == pytest.approx(0.5)


def test_evaluate_model_returns_metric_dict(evaluation_module):
    class DummyModel:
        def predict(self, X):
            return np.array([1.0, 2.0, 3.0])

    X_test = pd.DataFrame({"feature": [1, 2, 3]})
    y_test = pd.Series([1.0, 2.0, 3.0])

    metrics = evaluation_module.evaluate_model(DummyModel(), X_test, y_test)

    assert set(metrics) == {"mae", "rmse", "r2"}
    assert metrics["mae"] == pytest.approx(0.0)
    assert metrics["rmse"] == pytest.approx(0.0)
    assert metrics["r2"] == pytest.approx(1.0)
