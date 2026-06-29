import numpy as np
from pathlib import Path
from ekg_processing.ekg import EKGdata
from machine_learning.random_forest import RandomForestModel


class ModelTrainer:
    """
    Klasse zur Steuerung des kompletten ML-Trainingsprozesses.

    Lädt EKG-Trainingsdaten aus einem Ordner, extrahiert Features,
    trainiert ein ML-Modell und speichert es als Datei.

    Das verwendete Modell kann flexibel ausgetauscht werden — standard
    ist RandomForest, aber jedes Modell das von BaseModel erbt kann
    übergeben werden.
    """

    def __init__(self, model=None):
        """
        Initialisiert den ModelTrainer mit einem ML-Modell.

        Args:
            model (BaseModel | None): Ein ML-Modell das von BaseModel erbt.
                                      Wenn None wird RandomForestModel
                                      mit 100 Bäumen verwendet.

        Beispiel:
            trainer = ModelTrainer()                        # RandomForest
            trainer = ModelTrainer(model=XGBoostModel())   # XGBoost
        """
        if model is None:
            self.model = RandomForestModel(n_estimators=100)
        else:
            self.model = model

    def load_training_data(self, data_dir: str):
        """
        Lädt alle CSV-Dateien aus einem Ordner und extrahiert
        Features und Labels für das Training.

        Das Label wird automatisch aus dem Dateinamen gelesen:
            patient_001_normal.csv      → "Normal"
            patient_002_tachycardia.csv → "Tachykardie"
            patient_003_bradycardia.csv → "Bradykardie"
            patient_004_arrhythmia.csv  → "Arrhythmie"
            patient_005_noisy.csv       → "Verrauscht"

        Args:
            data_dir (str): Pfad zum Ordner mit den CSV-Trainingsdaten.

        Returns:
            tuple[np.ndarray, np.ndarray]:
                - X: Feature-Matrix der Form (n_samples, 4)
                     mit den Spalten [heart_rate, max_heart_rate, hrv, rr_mean]
                - y: Label-Vektor der Form (n_samples,)
                     mit den Diagnoseklassen als Strings
        """
        X = []
        y = []

        data_path = Path(data_dir)

        for csv_file in data_path.glob("*.csv"):

            label = self._extract_label(csv_file.name)
            if label is None:
                continue

            try:
                ekg = EKGdata(str(csv_file))
                features = ekg.get_all_features()

                feature_vector = [
                    features["heart_rate"],
                    features["max_heart_rate"],
                    features["hrv"],
                    features["rr_mean"]
                ]

                X.append(feature_vector)
                y.append(label)

                print(f"{csv_file.name} → {label} {feature_vector}")

            except Exception as e:
                print(f"Fehler bei {csv_file.name}: {e}")

        return np.array(X), np.array(y)

    def _extract_label(self, filename: str) -> str | None:
        """
        Liest das Diagnoselabel aus dem Dateinamen einer CSV-Datei.

        Unterstützte Schlüsselwörter im Dateinamen:
            - "normal"      → "Normal"
            - "tachycardia" → "Tachykardie"
            - "bradycardia" → "Bradykardie"
            - "arrhythmia"  → "Arrhythmie"
            - "noisy"       → "Verrauscht"

        Args:
            filename (str): Dateiname der CSV-Datei.

        Returns:
            str | None: Diagnoseklasse als String oder None wenn kein
                        bekanntes Schlüsselwort im Dateinamen gefunden wurde.
        """
        filename = filename.lower()

        if "normal" in filename:
            return "Normal"
        elif "tachycardia" in filename:
            return "Tachykardie"
        elif "bradycardia" in filename:
            return "Bradykardie"
        elif "arrhythmia" in filename:
            return "Arrhythmie"
        elif "noisy" in filename:
            return "Verrauscht"
        else:
            return None

    def train(self, data_dir: str, save_path: str) -> None:
        """
        Führt den kompletten Trainingsprozess durch.

        Schritte:
            1. Trainingsdaten aus CSV-Dateien laden
            2. Features extrahieren
            3. Modell trainieren
            4. Modell als Datei speichern

        Args:
            data_dir (str): Pfad zum Ordner mit den CSV-Trainingsdaten.
            save_path (str): Pfad zum Speichern des trainierten Modells,
                             z.B. "machine_learning/models/ekg_model.pkl".

        Returns:
            None
        """
        print("Lade Trainingsdaten...")
        X, y = self.load_training_data(data_dir)

        if len(X) == 0:
            print("Keine Trainingsdaten gefunden!")
            return

        print(f"{len(X)} EKGs geladen")
        print(f"Klassen: {set(y)}")

        print("Trainiere Modell...")
        self.model.train(X, y)

        print(f"Speichere Modell: {save_path}")
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        self.model.save(save_path)

        print("Training abgeschlossen!")


if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.train(
        data_dir="data/",
        save_path="machine_learning/models/ekg_model.pkl"
    )