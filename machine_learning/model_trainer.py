import numpy as np
from pathlib import Path
from ekg_processing.ekg import EKGdata
from machine_learning.random_forest import RandomForestModel

class ModelTrainer:

    def __init__(self, model=None):
        """
        Hier kannst du beliebiges Modell übergeben
        Standard ist RandomForest
        """
        if model is None:
            self.model = RandomForestModel(n_estimators=100)
        else:
            self.model = model  # z.B. später XGBoostModel()

    def load_training_data(self, data_dir: str):
        """
        Liest alle CSV Dateien aus dem data/ Ordner
        und extrahiert Features + Labels

        Dateiname bestimmt das Label:
        patient_001_normal.csv      → "Normal"
        patient_002_tachycardia.csv → "Tachykardie"
        """
        X = []  # Features
        y = []  # Labels

        data_path = Path(data_dir)

        for csv_file in data_path.glob("*.csv"):

            # Label aus Dateiname extrahieren
            label = self._extract_label(csv_file.name)
            if label is None:
                continue

            # EKG laden und Features berechnen
            try:
                ekg = EKGdata(str(csv_file))
                features = ekg.get_all_features()

                # Features als Liste
                feature_vector = [
                    features["heart_rate"],
                    features["max_heart_rate"],
                    features["hrv"],
                    features["rr_mean"]
                ]

                X.append(feature_vector)
                y.append(label)

                print(f"✅ {csv_file.name} → {label} {feature_vector}")

            except Exception as e:
                print(f"❌ Fehler bei {csv_file.name}: {e}")

        return np.array(X), np.array(y)

    def _extract_label(self, filename: str) -> str:
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
        Kompletter Trainingsprozess:
        1. Daten laden
        2. Modell trainieren
        3. Modell speichern
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