import streamlit as st
import pandas as pd
from database.database_connection import *
from ekg_processing.ekg import EKGdata
from pathlib import Path
from machine_learning.prediction import Prediction


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

def dashboard_page():

    st.header("Dashboard")

    persons = get_all_patients()

    if not persons:
        st.warning("Keine Patienten vorhanden. Bitte zuerst einen Patienten anlegen.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Patient Information")
        selected_patient = st.selectbox(
            "Select Patient",
            options=persons,
            format_func=lambda p: f"{p[1]} {p[2]}"
        )
        patient_id = selected_patient[0]

        st.markdown(f"**Name:** {selected_patient[1]} {selected_patient[2]}")
        st.markdown(f"**Date of Birth:** {selected_patient[3]}")
        st.markdown(f"**Gender:** {selected_patient[4]}")

    with col2:
        st.subheader("ECG File Upload")
        uploaded_file = st.file_uploader(
            "Upload ECG file (.csv)",
            type=["csv"]
        )

        if uploaded_file is not None:
            upload_dir = Path("data/")
            upload_dir.mkdir(parents=True, exist_ok=True)
            file_path = upload_dir / uploaded_file.name

            if not st.session_state.get(f"uploaded_{uploaded_file.name}"):
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                create_ekg_data(str(file_path), patient_id)
                st.session_state[f"uploaded_{uploaded_file.name}"] = True
                st.success(f"Datei gespeichert: {file_path}")

    # EKG auswählen
    st.divider()
    ekgs = get_ekgs_by_patients(patient_id)

    if not ekgs:
        st.info("Noch keine EKG-Daten für diesen Patienten vorhanden.")
        return

    selected_ekg = st.selectbox(
        "EKG-Aufnahme auswählen",
        options=ekgs,
        format_func=lambda e: f"EKG {e[0]} — {e[3]}"
    )

    # EKG laden und analysieren
    try:
        ekg = EKGdata(selected_ekg[1])  # [1] = file_path
    except Exception as ex:
        st.error(f"Fehler beim Laden der EKG-Datei: {ex}")
        return

    # Plot
    st.subheader("ECG Visualization — Lead II")
    fig = ekg.plot_time_series()
    st.plotly_chart(fig, use_container_width=True)

    # Feature Cards
    st.subheader("Analysis Results")
    features = ekg.get_all_features()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Heart Rate",     f"{features['heart_rate']} bpm")
    c2.metric("Max Heart Rate", f"{features['max_heart_rate']} bpm")
    c3.metric("RR Interval",    f"{features['rr_mean']} ms")
    c4.metric("HRV",            f"{features['hrv']} ms")

# ML Diagnose
    st.subheader("Machine Learning Diagnosis")

    try:
        prediction = Prediction()
        result = prediction.predict(features)

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.markdown("**Predicted Diagnosis**")
            st.markdown(f"### {result['predicted_class']}")

        with col_b:
            st.markdown("**Confidence Score**")
            st.markdown(f"### {result['confidence']} %")
            st.progress(result['confidence'] / 100)

        with col_c:
            st.markdown("**Risk Level**")
            if result['predicted_class'] == "Normal":
                st.success("🟢 Low — Status: Normal")
            elif result['predicted_class'] in ["Tachykardie", "Bradykardie"]:
                st.warning("🟡 Medium")
            else:
                st.error("🔴 High")

        # Automatisch speichern - aber nur einmal pro EKG
        ekg_key = f"saved_ekg_{selected_ekg[0]}"
        if not st.session_state.get(ekg_key):
            result_data = {
                "ekg_id":          selected_ekg[0],
                "heart_rate":      features["heart_rate"],
                "max_heart_rate":  features["max_heart_rate"],
                "rr_mean":         features["rr_mean"],
                "rr_std":          features["hrv"],
                "hrv":             features["hrv"],
                "predicted_class": result["predicted_class"],
                "confidence":      result["confidence"]
            }
            result_id = save_analysis_result(result_data)
            st.session_state[ekg_key] = result_id
            st.success(f"Analyse automatisch gespeichert!")

        st.session_state["result_id"] = st.session_state.get(ekg_key)

    except FileNotFoundError as e:
        st.error(f"Modell nicht gefunden: {e}")
    except Exception as e:
        st.error(f"Fehler bei der Diagnose: {e}")
# ------------------------------------------------------
# Patienten
# ------------------------------------------------------

def patients_page():

    st.header("Patients")
    st.subheader("Neuen Patienten anlegen")

    first_name = st.text_input("First Name")
    last_name  = st.text_input("Last Name")
    birth_date = st.date_input("Date of Birth")
    sex        = st.selectbox("Gender", ["Male", "Female", "Diverse"])

    if st.button("Create Patient"):
        patient_data = {
            "vorname":      first_name,
            "nachname":     last_name,
            "geburtsdatum": birth_date,
            "gender":       sex
        }
        create_patient(patient_data)
        st.success("Patient erfolgreich angelegt!")


# ------------------------------------------------------
# Neue Analyse
# ------------------------------------------------------

def analysis_page():

    st.header("New ECG Analysis")
    st.info("Wird noch implementiert.")


# ------------------------------------------------------
# Reports
# ------------------------------------------------------

def reports_page():

    st.header("Reports")
    st.info("Wird noch implementiert.")


# ------------------------------------------------------

if __name__ == "__main__":
    main()