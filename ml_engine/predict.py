"""Load an explicitly trained model when available; never invent predictions."""
from pathlib import Path
import joblib


class ModelUnavailableError(RuntimeError):
    pass


def load_model(path: str | Path):
    model_path = Path(path)
    if not model_path.is_file():
        raise ModelUnavailableError(f"No trained model found at {model_path}")
    return joblib.load(model_path)


def predict(features: dict[str, float], model_path: str | Path):
    model = load_model(model_path)
    return model.predict([list(features.values())])[0]
