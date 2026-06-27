from abc import ABC, abstractmethod
import numpy as np

class BaseModel(ABC):

    @abstractmethod
    def train(self, X: np.ndarray, y: np.ndarray) -> None:
        """Modell trainieren"""
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> str:
        """Klasse vorhersagen"""
        pass

    @abstractmethod
    def predict_proba(self, X: np.ndarray) -> float:
        """Konfidenz/Wahrscheinlichkeit vorhersagen"""
        pass

    @abstractmethod
    def save(self, path: str) -> None:
        """Modell speichern"""
        pass

    @abstractmethod
    def load(self, path: str) -> None:
        """Modell laden"""
        pass