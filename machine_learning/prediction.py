import numpy as np
import joblib
from pathlib import Path
from machine_learning.random_forest import RandomForestModel


class Prediction:
    """
    Klasse zur Vorhersage von EKG-Diagnosen mithilfe eines
    trainierten Machine Learning Modells.

    Lädt ein gespeichertes Modell beim Start und stellt eine
    einfache Schnittstelle für Vorhersagen bereit. Wird direkt
    von der Streamlit-App im Dashboard aufgerufen.

    Beispiel:
        predictor = Prediction()
        result = predictor.predict(features)
        # result = {"predicted_class": "Normal", "confidence": 96.0}
    """

    def __init__(self, model_path: str = "machine_learning/models/ekg_model.pkl"):
        """
        Initialisiert die Prediction-Klasse und lädt das trainierte Modell.

        Args:
            model_path (str): Pfad zur gespeicherten Modelldatei (.pkl).
                              Standard: "machine_learning/models/ekg_model.pkl"

        Raises:
            FileNotFoundError: Wenn keine Modelldatei unter dem angegebenen
                               Pfad gefunden wird. In diesem Fall muss zuerst
                               der ModelTrainer ausgeführt werden.
        """
        self.model = RandomForestModel()

        if not Path(model_path).exists():
            raise FileNotFoundError(f"Kein Modell gefunden unter: {model_path}")

        self.model.load(model_path)

    def predict(self, features: dict) -> dict:
        """
        Sagt die Diagnoseklasse und Konfidenz für ein EKG vorher.

        Wandelt das Feature-Dictionary in eine NumPy-Matrix um und
        gibt die Vorhersage des geladenen Modells zurück.

        Args:
            features (dict): Dictionary mit den berechneten EKG-Features.
                Erwartete Schlüssel:
                    - heart_rate (float): Durchschnittliche Herzfrequenz in bpm
                    - max_heart_rate (float): Maximale Herzfrequenz in bpm
                    - hrv (float): Herzratenvariabilität in ms
                    - rr_mean (float): Mittleres RR-Intervall in ms

        Returns:
            dict: Dictionary mit Vorhersageergebnis:
                - predicted_class (str): Vorhergesagte Diagnoseklasse,
                  z.B. "Normal", "Tachykardie", "Bradykardie",
                  "Arrhythmie" oder "Verrauscht"
                - confidence (float): Konfidenzwert in Prozent (0.0 - 100.0),
                  z.B. 96.0 bedeutet 96% Sicherheit
        """
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