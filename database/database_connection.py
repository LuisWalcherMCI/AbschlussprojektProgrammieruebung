import pymysql
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
if __name__ == "__main__":
    patients = get_all_patients()
    print(patients)
    dict_patient = {
        "vorname": "Steve",
        "nachname": "Mayr",
        "geburtsdatum": "1230-12-04",
        "gender": "male"
    }
    create_patient(dict_patient)
    patients = get_all_patients()
    print(patients)