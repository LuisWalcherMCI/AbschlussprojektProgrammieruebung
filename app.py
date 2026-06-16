import streamlit as st
import pandas as pd
from database.database_connection import *
from pathlib import Path


def main():

    st.set_page_config(
        page_title="EKG ML Analyzer",
        layout="wide"
    )

    st.title("EKG ML Analyzer")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Patients",
            "New Analysis",
            "Reports"
        ]
    )

    if menu == "Dashboard":
        dashboard_page()

    elif menu == "Patients":
        patients_page()

    elif menu == "New Analysis":
        analysis_page()

    elif menu == "Reports":
        reports_page()


# ------------------------------------------------------
# Dashboard
# ------------------------------------------------------

def get_all_names(persons):
    person_names = []
    for i in persons:
        person_names.append(i[1]+" "+i[2])
    return person_names

def read_csv(data):
    df = pd.read_csv(data, sep=',',header =0)    
    return df

def dashboard_page():

    st.header("Dashboard")
    persons = get_all_patients()
    col1, col2 = st.columns(2)
    with col1:
        selected_patient = st.selectbox(
            "Patienten",
            options=persons,
            format_func=lambda p: f"{p[1]} {p[2]}"
            )
        patient_id = selected_patient[0]
        ekgs = get_ekgs_by_patients(patient_id)
        
        selected_ekg = st.selectbox(
            "EKG-Daten",
            options=ekgs,
            format_func=lambda p: f"{p[0]}"
        )

    with col2:
        st.subheader("EKG-Daten hinaufladen")
        uploaded_file = st.file_uploader(
            "Upload ECG file",
            type=["csv"])

        if uploaded_file is not None:

            upload_dir = Path("data/")
            upload_dir.mkdir(parents=True, exist_ok=True)

            file_path = upload_dir / uploaded_file.name

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"Datei gespeichert: {file_path}")
            print(file_path)
            create_ekg_data(file_path,patient_id)

# ------------------------------------------------------
# Patienten
# ------------------------------------------------------

def patients_page():

    st.header("Patients")

    # Patient anlegen
    # --------------------------------------------------
    # Neuer Patient
    # --------------------------------------------------

    st.subheader("Neuen Patienten anlegen")

    first_name = st.text_input(
        "First Name"
    )

    last_name = st.text_input(
        "Last Name"
    )

    birth_date = st.date_input(
        "Date of Birth"
    )

    sex = st.selectbox(
        "Gender",
        [
            "Male",
            "Female",
            "Diverse"
        ]
    )

    if st.button("Create Patient"):

        patient_data = {

            "vorname": first_name,

            "nachname": last_name,

            "geburtsdatum": birth_date,

            "gender": sex

        }

        create_patient(patient_data)

        st.success("Patient erfolgreich angelegt")



# ------------------------------------------------------
# Neue Analyse
# ------------------------------------------------------

def analysis_page():

    st.header("New ECG Analysis")

    # Patient auswählen

    # CSV hochladen

    # CSV speichern

    # create_ekg_record()

    # EKG analysieren

    # Machine Learning

    # save_analysis_result()

    # PDF erzeugen

    # save_report()


# ------------------------------------------------------
# Reports
# ------------------------------------------------------

def reports_page():

    st.header("Reports")

    # Patient auswählen

    # Berichte anzeigen

    # PDF herunterladen


# ------------------------------------------------------

if __name__ == "__main__":
    main()