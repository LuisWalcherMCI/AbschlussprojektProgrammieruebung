import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from machine_learning.base_model import BaseModel


class RandomForestModel(BaseModel):
    """
    Konkrete Implementierung eines Random Forest Klassifikators
    für die EKG-Diagnose.

    Erbt von BaseModel und implementiert alle abstrakten Methoden.
    Ein Random Forest besteht aus vielen Entscheidungsbäumen die
    unabhängig voneinander abstimmen — die Mehrheitsmeinung gewinnt.

    Der Algorithmus kann jederzeit durch eine andere BaseModel-Implementierung
    ersetzt werden (z.B. XGBoostModel, CNNModel) ohne den Rest der
    Anwendung zu ändern.

    Beispiel:
        model = RandomForestModel(n_estimators=100)
        model.train(X_train, y_train)
        model.save("models/ekg_model.pkl")

        model.load("models/ekg_model.pkl")
        label = model.predict(X_test)
        confidence = model.predict_proba(X_test)
    """

    def __init__(self, n_estimators: int = 100):
        """
        Initialisiert den Random Forest Klassifikator.

        Args:
            n_estimators (int): Anzahl der Entscheidungsbäume im Forest.
                                Mehr Bäume = genauer aber langsamer.
                                Standard: 100
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=42
        )

    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Trainiert den Random Forest mit den gegebenen Trainingsdaten.

        Args:
            X (np.ndarray): Feature-Matrix der Form (n_samples, n_features).
                            Spalten: [heart_rate, max_heart_rate, hrv, rr_mean]
            y (np.ndarray): Label-Vektor der Form (n_samples,).
                            z.B. ["Normal", "Tachykardie", "Bradykardie", ...]

        Returns:
            None
        """
        self.model.fit(X, y)

    def predict(self, X: np.ndarray) -> str:
        """
        Sagt die Diagnoseklasse für einen EKG-Datensatz vorher.

        Args:
            X (np.ndarray): Feature-Matrix der Form (1, n_features).

        Returns:
            str: Vorhergesagte Diagnoseklasse,
                 z.B. "Normal", "Tachykardie", "Bradykardie",
                 "Arrhythmie" oder "Verrauscht".
        """
        return self.model.predict(X)[0]

    def predict_proba(self, X: np.ndarray) -> float:
        """
        Gibt die Konfidenz der Vorhersage zurück.

        Berechnet die Wahrscheinlichkeiten für alle Klassen und
        gibt den höchsten Wert zurück — das ist die Konfidenz
        für die vorhergesagte Klasse.

        Args:
            X (np.ndarray): Feature-Matrix der Form (1, n_features).

        Returns:
            float: Konfidenzwert zwischen 0.0 und 1.0.
                   z.B. 0.96 bedeutet 96% Sicherheit.
        """
        proba = self.model.predict_proba(X)
        return float(np.max(proba[0]))

    def save(self, path: str) -> None:
        """
        Speichert das trainierte Modell als .pkl Datei mit joblib.

        Das gespeicherte Modell kann später mit load() wieder geladen
        werden ohne neu trainieren zu müssen.

        Args:
            path (str): Dateipfad zum Speichern,
                        z.B. "machine_learning/models/ekg_model.pkl".

        Returns:
            None
        """
        joblib.dump(self.model, path)

    def load(self, path: str) -> None:
        """
        Lädt ein bereits trainiertes Modell aus einer .pkl Datei.

        Args:
            path (str): Dateipfad zum gespeicherten Modell,
                        z.B. "machine_learning/models/ekg_model.pkl".

        Returns:
            None
        """
        self.model = joblib.load(path)