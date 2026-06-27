import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from machine_learning.base_model import BaseModel

class RandomForestModel(BaseModel):

    def __init__(self, n_estimators: int = 100):
        """
        n_estimators = Anzahl der Bäume im Forest
        je mehr Bäume, desto genauer aber langsamer
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=42  # damit die Ergebnisse reproduzierbar sind
        )

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        X = Features (heart_rate, hrv, rr_mean, ...)
        y = Labels (Normal, Tachykardie, ...)
        """
        self.model.fit(X, y)

    def predict(self, X: np.ndarray) -> str:
        """
        Gibt die vorhergesagte Klasse zurück
        z.B. "Normal" oder "Tachykardie"
        """
        return self.model.predict(X)[0]

    def predict_proba(self, X: np.ndarray) -> float:
        """
        Gibt die Konfidenz zurück
        z.B. 0.96 = 96% sicher
        """
        proba = self.model.predict_proba(X)
        return float(np.max(proba))

    def save(self, path: str) -> None:
        """
        Speichert das trainierte Modell als Datei
        damit man es nicht jedes Mal neu trainieren muss
        """
        joblib.dump(self.model, path)

    def load(self, path: str) -> None:
        """
        Lädt ein bereits trainiertes Modell aus einer Datei
        """
        self.model = joblib.load(path)