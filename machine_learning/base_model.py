from abc import ABC, abstractmethod
import numpy as np


class BaseModel(ABC):
    """
    Abstrakte Basisklasse für alle Machine Learning Modelle.

    Definiert eine einheitliche Schnittstelle die von allen konkreten
    ML-Modellen implementiert werden muss. Dadurch kann der Algorithmus
    ausgetauscht werden ohne den Rest der Anwendung zu ändern.

    Beispiel:
        class RandomForestModel(BaseModel):
            def train(self, X, y): ...
            def predict(self, X): ...
            ...

        class XGBoostModel(BaseModel):
            def train(self, X, y): ...
            def predict(self, X): ...
            ...
    """

    @abstractmethod
    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Trainiert das Modell mit den gegebenen Trainingsdaten.

        Args:
            X (np.ndarray): Feature-Matrix der Form (n_samples, n_features).
                            Jede Zeile entspricht einem EKG-Datensatz,
                            jede Spalte einem Feature (HR, HRV, RR, ...).
            y (np.ndarray): Label-Vektor der Form (n_samples,).
                            Enthält die Diagnoseklassen als Strings
                            z.B. ["Normal", "Tachykardie", ...].

        Returns:
            None
        """
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> str:
        """
        Sagt die Diagnoseklasse für einen neuen EKG-Datensatz vorher.

        Args:
            X (np.ndarray): Feature-Matrix der Form (1, n_features).
                            Enthält die Features eines einzelnen EKGs.

        Returns:
            str: Vorhergesagte Diagnoseklasse,
                 z.B. "Normal", "Tachykardie", "Bradykardie",
                 "Arrhythmie" oder "Verrauscht".
        """
        pass

    @abstractmethod
    def predict_proba(self, X: np.ndarray) -> float:
        """
        Gibt die Konfidenz der Vorhersage als Wahrscheinlichkeit zurück.

        Args:
            X (np.ndarray): Feature-Matrix der Form (1, n_features).
                            Enthält die Features eines einzelnen EKGs.

        Returns:
            float: Konfidenzwert zwischen 0.0 und 1.0.
                   z.B. 0.96 bedeutet 96% Sicherheit für die Vorhersage.
        """
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """
        Speichert das trainierte Modell als Datei.

        Args:
            path (str): Dateipfad zum Speichern des Modells,
                        z.B. "machine_learning/models/ekg_model.pkl".

        Returns:
            None
        """
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        """
        Lädt ein bereits trainiertes Modell aus einer Datei.

        Args:
            path (str): Dateipfad zum gespeicherten Modell,
                        z.B. "machine_learning/models/ekg_model.pkl".

        Returns:
            None
        """
        pass