import pandas as pd
import plotly.graph_objects as go
from scipy.signal import find_peaks

class EKGdata:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = pd.read_csv(file_path, sep=',', header=0)
        # Spalten umbenennen damit der Rest gleich bleibt
        self.df.columns = ['time', 'voltage']

        peaks_idx, _ = find_peaks(self.df['voltage'], height=0.5, distance=150)
        self.df['is_peak'] = False
        self.df.loc[peaks_idx, 'is_peak'] = True

    def plot_time_series(self):
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
        peaks = self.df[self.df['is_peak']]
        if len(peaks) < 2:
            return 0.0
        dt_s = peaks['time'].iloc[-1] - peaks['time'].iloc[0]
        dt_min = dt_s / 60
        return len(peaks) / dt_min

    def calculate_max_hr(self) -> float:
        peaks = self.df[self.df['is_peak']]
        if len(peaks) < 2:
            return 0.0
        rr = peaks['time'].diff().dropna()
        min_rr = rr.min()
        return 60 / min_rr if min_rr > 0 else 0.0

    def calculate_hrv(self) -> float:
        peaks = self.df[self.df['is_peak']]
        if len(peaks) < 2:
            return 0.0
        rr = peaks['time'].diff().dropna() * 1000 
        return float(rr.std())

    def calculate_rr_mean(self) -> float:
        peaks = self.df[self.df['is_peak']]
        if len(peaks) < 2:
            return 0.0
        rr = peaks['time'].diff().dropna() * 1000
        return float(rr.mean())

    def get_all_features(self) -> dict:
        return {
            "heart_rate":     round(self.calculate_avg_hr(), 1),
            "max_heart_rate": round(self.calculate_max_hr(), 1),
            "hrv":            round(self.calculate_hrv(), 1),
            "rr_mean":        round(self.calculate_rr_mean(), 1),
        }