import requests
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from prometheus_client import Gauge

model = BertForSequenceClassification.from_pretrained("ml/bert_model")
tokenizer = BertTokenizer.from_pretrained("ml/bert_model")
model.eval()

BERT_ANOMALIES = Gauge("bert_log_anomalies", "Number of anomalies detected in logs using BERT")

def fetch_logs():
    loki_url = "http://localhost:3100/loki/api/v1/query_range"
    query = '{job="tracking_service"}'
    params = {"query": query, "start": "now-5m", "end": "now", "limit": 1000}
    response = requests.get(loki_url, params=params)
    logs = response.json()
    return [entry['line'] for stream in logs.get('data', {}).get('result', []) for entry in stream.get('values', [])]

def detect_anomalies():
    logs = fetch_logs()
    inputs = tokenizer(logs, padding=True, truncation=True, max_length=512, return_tensors="pt")
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=1).tolist()

    anomaly_count = sum(predictions)
    BERT_ANOMALIES.set(anomaly_count)

    return anomaly_count

if __name__ == "__main__":
    while True:
        detect_anomalies()
