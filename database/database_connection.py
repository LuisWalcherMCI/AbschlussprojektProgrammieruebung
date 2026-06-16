import pymysql
from datetime import date
from pathlib import Path

def get_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="chrirolu1",
        database="abschlussprojektmci",
        port=3306
    )
    print("Verbindung erfolgreich!")

    return connection

def get_all_patients():
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
        cursor.execute(sql,patient_dict)
        conn.commit()
    

    finally:
        cursor.close()
        conn.close()

def get_patient_by_id(id):
    conn = get_connection()

    try:
        cursor = conn.cursor()
        sql = """
            SELECT * FROM patient WHERE id = %(id)s
            """
        cursor.execute(sql, {"id": id})
        patient = cursor.fetchone()

        return patient
    finally:
        cursor.close()
        conn.close()

def create_ekg_data(data_name, patient_id):

    conn = get_connection()
    recording_date = date.today()

    try:
        cursor = conn.cursor()

        print("ICH BIN IN DER NEUEN VERSION")
        print("data_name:", data_name)
        print("patient_id:", patient_id)
        print("recording_date:", recording_date)

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

        print("SQL:", sql)
        print("PARAMS:", params)

        cursor.execute(sql, params)

        conn.commit()

    finally:
        cursor.close()
        conn.close()

def get_ekgs_by_patients(patient_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        sql = """
            SELECT * FROM ekg_records WHERE patient_id = %(patient_id)s
            """
        cursor.execute(sql, {"patient_id": patient_id})
        ekg_data = cursor.fetchall()

        return ekg_data
    finally:
        cursor.close()
        conn.close()


def save_analysis_result(result_data: dict) -> int:

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO analysis_results
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
    conn = get_connection()
    ekg_id = ekg_data[0]
    try:
        cursor = conn.cursor()
        sql = """
            SELECT * FROM diagnosis_result WHERE ekg_id = %(ekg_data)s
            """
        cursor.execute(sql, {"ekg_data": ekg_data})
        diagnosis_result = cursor.fetchone()

        return diagnosis_result
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    patients = get_all_patients()
    print(patients)
    dict_patient = {
        "vorname": "Steve",
        "nachname": "Mayr",
        "geburtsdatum": "1230-12-04",
        "gender": "male"
    }
    #create_patient(dict_patient)
    patients = get_all_patients()
    print(patients)
    print(get_ekgs_by_patients(1))