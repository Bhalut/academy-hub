import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import requests


# Obtener logs desde Loki
def fetch_logs_from_loki():
    loki_url = "http://localhost:3100/loki/api/v1/query_range"
    query = '{job="tracking_service"}'
    params = {"query": query, "start": "now-1h", "end": "now", "limit": 5000}
    response = requests.get(loki_url, params=params)
    logs = response.json()
    return [entry['line'] for stream in logs.get('data', {}).get('result', []) for entry in stream.get('values', [])]


# Preprocesamiento de logs
def preprocess_logs(logs):
    log_df = pd.DataFrame(logs, columns=["log"])
    log_df["length"] = log_df["log"].apply(len)
    log_df["entropy"] = log_df["log"].apply(lambda x: len(set(x)) / len(x) if len(x) > 0 else 0)
    return log_df[["length", "entropy"]].values


# Crear secuencias para LSTM
def create_sequences(data, seq_length=10):
    sequences = []
    labels = []
    for i in range(len(data) - seq_length):
        sequences.append(data[i: i + seq_length])
        labels.append(data[i + seq_length])
    return np.array(sequences), np.array(labels)


# Entrenar LSTM
def train_lstm():
    logs = fetch_logs_from_loki()
    data = preprocess_logs(logs)

    # Normalización
    mean, std = np.mean(data, axis=0), np.std(data, axis=0)
    data = (data - mean) / std

    # Crear secuencias
    X, y = create_sequences(data)

    # Definir modelo LSTM
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
        Dropout(0.2),
        LSTM(32, return_sequences=False),
        Dropout(0.2),
        Dense(X.shape[2])
    ])

    model.compile(optimizer="adam", loss="mse")

    # Entrenar
    model.fit(X, y, epochs=10, batch_size=32, validation_split=0.1)

    # Guardar modelo
    model.save("ml/lstm_model.h5")
    joblib.dump((mean, std), "ml/lstm_scaler.pkl")
    print("Modelo LSTM entrenado y guardado.")


if __name__ == "__main__":
    train_lstm()
