import pymysql
from datetime import date
from pathlib import Path


def get_connection():
    """
    Stellt eine Verbindung zur MySQL-Datenbank her.

    Returns:
        pymysql.Connection: Aktive Datenbankverbindung.
    """
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="abschlussproject_mci",
        port=3306
    )
    print("Verbindung erfolgreich!")
    return connection


def get_all_patients():
    """
    Gibt alle Patienten aus der Datenbank zurück.

    Returns:
        list[tuple]: Liste aller Patientendatensätze als Tuples.
                     Format: (id, Vorname, Nachname, Geburtsdatum, Gender)
    """
    conn = get_connection()

    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM patient"
        cursor.execute(sql)
        patients = cursor.fetchall()
        return patients

    finally:
        cursor.close()
        conn.close()


def create_patient(patient_dict):
    """
    Legt einen neuen Patienten in der Datenbank an.

    Args:
        patient_dict (dict): Dictionary mit Patientendaten.
            Erwartete Schlüssel:
                - vorname (str): Vorname des Patienten
                - nachname (str): Nachname des Patienten
                - geburtsdatum (str | date): Geburtsdatum im Format YYYY-MM-DD
                - gender (str): Geschlecht des Patienten

    Returns:
        None
    """
    conn = get_connection()

    try:
        cursor = conn.cursor()

        sql = """
            INSERT INTO patient (
                Vorname,
                Nachname,
                Geburtsdatum,
                Gender)
            VALUES
            (
                %(vorname)s,
                %(nachname)s,
                %(geburtsdatum)s,
                %(gender)s
            )
        """
        cursor.execute(sql, patient_dict)
        conn.commit()

    finally:
        cursor.close()
        conn.close()


def get_patient_by_id(id):
    """
    Gibt einen einzelnen Patienten anhand seiner ID zurück.

    Args:
        id (int): Die ID des gesuchten Patienten.

    Returns:
        tuple | None: Patientendatensatz als Tuple oder None wenn nicht gefunden.
                      Format: (id, Vorname, Nachname, Geburtsdatum, Gender)
    """
    conn = get_connection()

    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM patient WHERE id = %(id)s"
        cursor.execute(sql, {"id": id})
        patient = cursor.fetchone()
        return patient

    finally:
        cursor.close()
        conn.close()


def create_ekg_data(data_name, patient_id):
    """
    Legt einen neuen EKG-Datensatz in der Datenbank an und verknüpft
    ihn mit einem Patienten.

    Args:
        data_name (str): Dateipfad zur gespeicherten CSV-Datei.
        patient_id (int): ID des Patienten dem das EKG zugeordnet wird.

    Returns:
        None
    """
    conn = get_connection()
    recording_date = date.today()

    try:
        cursor = conn.cursor()

        sql = """
            INSERT INTO ekg_records (
                file_path,
                recording_date,
                patient_id
            )
            VALUES (
                %(data_name)s,
                %(recording_date)s,
                %(patient_id)s
            )
        """

        params = {
            "data_name": data_name,
            "recording_date": recording_date,
            "patient_id": patient_id
        }

        cursor.execute(sql, params)
        conn.commit()

    finally:
        cursor.close()
        conn.close()


def get_ekgs_by_patients(patient_id):
    """
    Gibt alle EKG-Datensätze eines bestimmten Patienten zurück.

    Args:
        patient_id (int): ID des Patienten.

    Returns:
        list[tuple]: Liste aller EKG-Datensätze des Patienten als Tuples.
                     Format: (idekg_records, file_path, recording_date, patient_id)
    """
    conn = get_connection()

    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM ekg_records WHERE patient_id = %(patient_id)s"
        cursor.execute(sql, {"patient_id": patient_id})
        ekg_data = cursor.fetchall()
        return ekg_data

    finally:
        cursor.close()
        conn.close()


def save_analysis_result(result_data: dict) -> int:
    """
    Speichert das Ergebnis einer EKG-Analyse in der Datenbank.

    Args:
        result_data (dict): Dictionary mit allen Analyseergebnissen.
            Erwartete Schlüssel:
                - ekg_id (int): ID des analysierten EKGs
                - heart_rate (float): Durchschnittliche Herzfrequenz in bpm
                - max_heart_rate (float): Maximale Herzfrequenz in bpm
                - rr_mean (float): Mittleres RR-Intervall in ms
                - rr_std (float): Standardabweichung der RR-Intervalle in ms
                - hrv (float): Herzratenvariabilität in ms
                - predicted_class (str): ML-Diagnoseklasse
                - confidence (float): Konfidenzwert des ML-Modells in %

    Returns:
        int: ID des neu erstellten Analysedatensatzes.
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO diagnosis_result
    (
        ekg_id,
        heart_rate,
        max_heart_rate,
        rr_mean,
        rr_std,
        hrv,
        predicted_class,
        confidence
    )
    VALUES
    (
        %(ekg_id)s,
        %(heart_rate)s,
        %(max_heart_rate)s,
        %(rr_mean)s,
        %(rr_std)s,
        %(hrv)s,
        %(predicted_class)s,
        %(confidence)s
    )
    """

    cursor.execute(sql, result_data)
    conn.commit()
    result_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return result_id


def get_results_by_ekg_id(ekg_data):
    """
    Gibt das Analyseergebnis für ein bestimmtes EKG zurück.

    Args:
        ekg_data (tuple): EKG-Datensatz Tuple aus der Datenbank.
                          Die ID wird aus Index [0] entnommen.

    Returns:
        tuple | None: Analyseergebnis als Tuple oder None wenn nicht gefunden.
    """
    conn = get_connection()
    ekg_id = ekg_data[0]

    try:
        cursor = conn.cursor()
        sql = "SELECT * FROM diagnosis_result WHERE ekg_id = %(ekg_id)s"
        cursor.execute(sql, {"ekg_id": ekg_id})
        diagnosis_result = cursor.fetchone()
        return diagnosis_result

    finally:
        cursor.close()
        conn.close()


def save_report(report_data: dict) -> int:
    """
    Speichert einen generierten PDF-Bericht in der Datenbank.

    Args:
        report_data (dict): Dictionary mit den Report-Daten.
            Erwartete Schlüssel:
                - ekg_id (int): ID des EKGs
                - diagnosis_id (int): ID der Diagnose
                - pdf_path (str): Pfad zur PDF-Datei

    Returns:
        int: ID des neu erstellten Report-Eintrags.
    """
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO reports (ekg_id, diagnosis_id, pdf_path)
        VALUES (%(ekg_id)s, %(diagnosis_id)s, %(pdf_path)s)
    """

    cursor.execute(sql, report_data)
    conn.commit()
    report_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return report_id



if __name__ == "__main__":
    patients = get_all_patients()
    print(patients)