from pathlib import Path
import joblib

MODEL_PATH = Path(__file__).resolve().parents[2] / "trained_models" / "packaging_rf.joblib"

_model = None


def load():
    global _model

    if not MODEL_PATH.exists():
        _model = None
        return None

    _model = joblib.load(MODEL_PATH)
    return _model


def get():
    global _model

    if _model is None:
        load()

    return _model
