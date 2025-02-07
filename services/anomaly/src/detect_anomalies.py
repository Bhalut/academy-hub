import joblib
import requests
import json
import pandas as pd
from prometheus_client import Gauge

# Cargar modelo entrenado
model = joblib.load("ml/anomaly_model.pkl")

# Métrica de Prometheus para anomalías
ANOMALY_COUNT = Gauge("log_anomalies_detected", "Número de anomalías detectadas en logs")

# Obtener logs desde Loki
def fetch_logs():
    loki_url = "http://localhost:3100/loki/api/v1/query_range"
    query = '{job="tracking_service"}'
    params = {
        "query": query,
        "start": "now-5m",
        "end": "now",
        "limit": 500
    }
    response = requests.get(loki_url, params=params)
    logs = response.json()
    return [entry['line'] for stream in logs.get('data', {}).get('result', []) for entry in stream.get('values', [])]

# Preprocesar logs y detectar anomalías
def detect_anomalies():
    logs = fetch_logs()
    log_data = pd.DataFrame(logs, columns=["log"])
    log_data["length"] = log_data["log"].apply(len)

    anomalies = model.predict(log_data[["length"]])
    anomaly_count = sum(anomalies == -1)

    ANOMALY_COUNT.set(anomaly_count)
    return anomaly_count

if __name__ == "__main__":
    while True:
        detect_anomalies()
