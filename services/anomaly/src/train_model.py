import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
import requests
import json

# Obtener logs desde Loki
def fetch_logs_from_loki():
    loki_url = "http://localhost:3100/loki/api/v1/query_range"
    query = '{job="tracking_service"}'
    params = {
        "query": query,
        "start": "now-1h",
        "end": "now",
        "limit": 1000
    }
    response = requests.get(loki_url, params=params)
    logs = response.json()
    return [entry['line'] for stream in logs.get('data', {}).get('result', []) for entry in stream.get('values', [])]

# Preprocesamiento de logs
def preprocess_logs(logs):
    log_df = pd.DataFrame(logs, columns=["log"])
    log_df["length"] = log_df["log"].apply(len)
    return log_df[["length"]]

# Entrenar modelo de Machine Learning
def train_anomaly_model():
    logs = fetch_logs_from_loki()
    log_data = preprocess_logs(logs)

    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(log_data)

    joblib.dump(model, "ml/anomaly_model.pkl")
    print("Modelo de detección de anomalías entrenado y guardado.")

if __name__ == "__main__":
    train_anomaly_model()
