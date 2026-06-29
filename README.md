# EKG ML Analyzer

Dieses Repository beinhaltet den Code für das Abschlussprojekt: Eine Streamlit-Webanwendung für Kardiologen zur Verwaltung von Patienten und automatisierten Analyse von EKG-Daten mithilfe von Machine Learning.

---

## Repository herunterladen

Zuerst das Repository klonen:

```bash
git clone https://github.com/<Luis-Walcher>/AbschlussprojektProgrammieruebung.git
```

Dann in den Projektordner wechseln:

```bash
cd AbschlussprojektProgrammieruebung
```

---

## Voraussetzungen

Benötigt:

- Python 3.11+
- PDM
- MySQL Server 8.0+
- MySQL Workbench (empfohlen)
- Git

### PDM installieren

```bash
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
```

---

## Virtuelle Umgebung aktivieren (optional)

```bash
pdm venv activate
```

Windows (PowerShell):

```powershell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned)
& .venv\Scripts\Activate.ps1
```

---

## Pakete installieren

```bash
pdm install
```

Falls die Pakete manuell installiert werden müssen:

```bash
pdm add streamlit pymysql pandas numpy scipy scikit-learn plotly reportlab joblib kaleido
```

### Einzelne Pakete installieren

```bash
pdm add paketname
```

Beispiele:

```bash
pdm add streamlit
pdm add scikit-learn
pdm add reportlab
```

---

## Datenbank einrichten

In MySQL Workbench eine neue Datenbank anlegen und folgende SQL-Befehle ausführen:

```sql
CREATE DATABASE abschlussproject_mci;
USE abschlussproject_mci;

CREATE TABLE patient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Vorname VARCHAR(45),
    Nachname VARCHAR(45),
    Geburtsdatum DATE,
    Gender VARCHAR(45)
);

CREATE TABLE ekg_records (
    idekg_records INT AUTO_INCREMENT PRIMARY KEY,
    file_path VARCHAR(255),
    sampling_rate INT,
    recording_date TIMESTAMP,
    patient_id INT,
    FOREIGN KEY (patient_id) REFERENCES patient(id)
);

CREATE TABLE diagnosis_result (
    iddiagnosis_result INT AUTO_INCREMENT PRIMARY KEY,
    ekg_id INT,
    heart_rate DOUBLE,
    max_heart_rate INT,
    rr_mean DOUBLE,
    rr_std DOUBLE,
    hrv DOUBLE,
    predicted_class VARCHAR(45),
    confidence DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ekg_id) REFERENCES ekg_records(idekg_records)
);

CREATE TABLE reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    result_id INT,
    pdf_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (result_id) REFERENCES diagnosis_result(iddiagnosis_result)
);
```

### Datenbankverbindung konfigurieren

In `database/database_connection.py` die Zugangsdaten anpassen:

```python
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="dein_passwort",
    database="abschlussproject_mci",
    port=3306
)
```

---

## ML-Modell trainieren

Vor dem ersten Start muss das Machine Learning Modell trainiert werden.

EKG-Trainingsdaten (CSV-Dateien) in den `data/` Ordner legen. Die Dateinamen müssen das Label enthalten:

```
data/
    patient_001_normal.csv
    patient_002_tachycardia.csv
    patient_003_bradycardia.csv
    patient_004_arrhythmia.csv
    patient_005_noisy.csv
```

Dann das Modell trainieren:

```bash
pdm run python -m machine_learning.model_trainer
```

Das trainierte Modell wird unter `machine_learning/models/ekg_model.pkl` gespeichert.

---

## Streamlit App starten

```bash
pdm run streamlit run app.py
```

Die App öffnet sich automatisch im Browser unter `http://localhost:8501`.

---

## Über diese App

Diese Anwendung wurde mit **Streamlit** entwickelt und bietet folgende Hauptfunktionen:

1. **Patientenverwaltung:** Patienten können angelegt und ausgewählt werden.
2. **EKG Upload:** CSV-Dateien können hochgeladen und einem Patienten zugeordnet werden.
3. **Automatische Analyse:** Das EKG-Signal wird verarbeitet, R-Peaks werden erkannt und Features wie Herzfrequenz, HRV und RR-Intervall werden berechnet.
4. **Machine Learning Diagnose:** Ein trainiertes Random Forest Modell klassifiziert das EKG automatisch (Normal, Tachykardie, Bradykardie, Arrhythmie, Verrauscht) und gibt einen Konfidenzwert aus.
5. **PDF-Report:** Ein professioneller Bericht mit EKG-Visualisierung, Analyseergebnissen und ML-Diagnose kann generiert und heruntergeladen werden.



