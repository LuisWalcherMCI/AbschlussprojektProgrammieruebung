import pandas as pd
import plotly.graph_objects as go
from scipy.signal import find_peaks


class EKGdata:
    """
    Klasse zur Verarbeitung und Analyse von EKG-Daten aus CSV-Dateien.

    Lädt ein EKG-Signal, erkennt automatisch R-Peaks und berechnet
    klinisch relevante Features wie Herzfrequenz, HRV und RR-Intervalle.

    Attributes:
        file_path (str): Pfad zur CSV-Datei.
        df (pd.DataFrame): DataFrame mit Spalten 'time', 'voltage' und 'is_peak'.
    """

    def __init__(self, file_path: str):
        """
        Initialisiert das EKGdata-Objekt, lädt die CSV-Datei und
        erkennt automatisch R-Peaks im Signal.

        Args:
            file_path (str): Pfad zur EKG-CSV-Datei.
                             Erwartet zwei Spalten: 'time' (s) und 'voltage' (mV).
        """
        self.file_path = file_path
        self.df = pd.read_csv(file_path, sep=',', header=0)
        self.df.columns = ['time', 'voltage']

        peaks_idx, _ = find_peaks(self.df['voltage'], height=0.5, distance=150)
        self.df['is_peak'] = False
        self.df.loc[peaks_idx, 'is_peak'] = True

    def plot_time_series(self) -> go.Figure:
        """
        Erstellt einen interaktiven Plotly-Graphen des EKG-Signals
        mit markierten R-Peaks.

        Returns:
            go.Figure: Plotly Figure mit EKG-Signal (blau) und
                       R-Peak Markierungen (rote Punkte).
        """
        peaks = self.df[self.df['is_peak']]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df['time'],
            y=self.df['voltage'],
            mode='lines',
            name='Signal',
            line=dict(color='#1a56db', width=1.5)
        ))
        fig.add_trace(go.Scatter(
            x=peaks['time'],
            y=peaks['voltage'],
            mode='markers',
            name='R-Peak',
            marker=dict(color='red', size=8)
        ))
        fig.update_layout(
            title='ECG Visualization — Lead II',
            xaxis_title='Time (s)',
            yaxis_title='Voltage (mV)',
            legend=dict(orientation='h', x=1, xanchor='right', y=1.1)
        )
        return fig

    def calculate_avg_hr(self) -> float:
        """
        Berechnet die durchschnittliche Herzfrequenz in bpm.

        Die Herzfrequenz wird aus der Anzahl der R-Peaks und der
        Gesamtaufnahmedauer berechnet:
        HR = Anzahl Peaks / Zeit in Minuten

        Returns:
            float: Durchschnittliche Herzfrequenz in bpm.
                   Gibt 0.0 zurück wenn weniger als 2 Peaks erkannt wurden.
        """
        peaks = self.df[self.df['is_peak']]
        if len(peaks) < 2:
            return 0.0
        dt_s = peaks['time'].iloc[-1] - peaks['time'].iloc[0]
        dt_min = dt_s / 60
        return len(peaks) / dt_min

    def calculate_max_hr(self) -> float:
        """
        Berechnet die maximale Herzfrequenz in bpm.

        Die maximale HR entspricht dem kürzesten RR-Intervall:
        Max HR = 60 / minimales RR-Intervall (in Sekunden)

        Returns:
            float: Maximale Herzfrequenz in bpm.
                   Gibt 0.0 zurück wenn weniger als 2 Peaks erkannt wurden.
        """
        peaks = self.df[self.df['is_peak']]
        if len(peaks) < 2:
            return 0.0
        rr = peaks['time'].diff().dropna()
        min_rr = rr.min()
        return 60 / min_rr if min_rr > 0 else 0.0

    def calculate_hrv(self) -> float:
        """
        Berechnet die Herzratenvariabilität (HRV) in Millisekunden.

        Die HRV wird als Standardabweichung der RR-Intervalle berechnet
        (SDNN-Methode). Eine höhere HRV deutet auf ein gesünderes Herz hin.

        Returns:
            float: HRV als Standardabweichung der RR-Intervalle in ms.
                   Gibt 0.0 zurück wenn weniger als 2 Peaks erkannt wurden.
        """
        peaks = self.df[self.df['is_peak']]
        if len(peaks) < 2:
            return 0.0
        rr = peaks['time'].diff().dropna() * 1000
        return float(rr.std())

    def calculate_rr_mean(self) -> float:
        """
        Berechnet das mittlere RR-Intervall in Millisekunden.

        Das RR-Intervall ist die Zeit zwischen zwei aufeinanderfolgenden
        R-Peaks. Der Mittelwert entspricht der durchschnittlichen
        Herzschlagdauer.

        Returns:
            float: Mittleres RR-Intervall in ms.
                   Gibt 0.0 zurück wenn weniger als 2 Peaks erkannt wurden.
        """
        peaks = self.df[self.df['is_peak']]
        if len(peaks) < 2:
            return 0.0
        rr = peaks['time'].diff().dropna() * 1000
        return float(rr.mean())

    def get_all_features(self) -> dict:
        """
        Berechnet alle Features auf einmal und gibt sie als Dictionary zurück.

        Ruft alle Berechnungsmethoden auf und rundet die Ergebnisse
        auf eine Dezimalstelle. Wird vom ML-Modell und der Streamlit-App
        verwendet.

        Returns:
            dict: Dictionary mit allen berechneten Features:
                - heart_rate (float): Durchschnittliche Herzfrequenz in bpm
                - max_heart_rate (float): Maximale Herzfrequenz in bpm
                - hrv (float): Herzratenvariabilität in ms
                - rr_mean (float): Mittleres RR-Intervall in ms
        """
        return {
            "heart_rate":     round(self.calculate_avg_hr(), 1),
            "max_heart_rate": round(self.calculate_max_hr(), 1),
            "hrv":            round(self.calculate_hrv(), 1),
            "rr_mean":        round(self.calculate_rr_mean(), 1),
        }