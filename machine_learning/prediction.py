import numpy as np
import joblib
from pathlib import Path
from machine_learning.random_forest import RandomForestModel

class Prediction:

    def __init__(self, model_path: str = "machine_learning/models/ekg_model.pkl"):
        self.model = RandomForestModel()
        
        if not Path(model_path).exists():
            raise FileNotFoundError(f"Kein Modell gefunden unter: {model_path}")
        
        self.model.load(model_path)

    def predict(self, features: dict) -> dict:
        X = np.array([[
            features["heart_rate"],
            features["max_heart_rate"],
            features["hrv"],
            features["rr_mean"]
        ]])

        predicted_class = self.model.predict(X)
        confidence      = self.model.predict_proba(X)

        return {
            "predicted_class": predicted_class,
            "confidence":      round(confidence * 100, 1)
        }