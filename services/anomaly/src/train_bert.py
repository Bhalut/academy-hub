import pandas as pd
import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import requests
from sklearn.model_selection import train_test_split
import joblib


def fetch_logs_from_loki():
    loki_url = "http://localhost:3100/loki/api/v1/query_range"
    query = '{job="tracking_service"}'
    params = {"query": query, "start": "now-1h", "end": "now", "limit": 5000}
    response = requests.get(loki_url, params=params)
    logs = response.json()
    return [entry['line'] for stream in logs.get('data', {}).get('result', []) for entry in stream.get('values', [])]


def prepare_data():
    logs = fetch_logs_from_loki()
    df = pd.DataFrame(logs, columns=["log"])

    df["label"] = df["log"].apply(lambda x: 1 if "error" in x.lower() else 0)

    return train_test_split(df["log"], df["label"], test_size=0.2, random_state=42)


def train_bert():
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)

    X_train, X_test, y_train, y_test = prepare_data()

    train_encodings = tokenizer(list(X_train), truncation=True, padding=True, max_length=512)
    test_encodings = tokenizer(list(X_test), truncation=True, padding=True, max_length=512)

    class LogDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels

        def __len__(self):
            return len(self.labels)

        def __getitem__(self, idx):
            return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}, torch.tensor(self.labels[idx])

    train_dataset = LogDataset(train_encodings, list(y_train))
    test_dataset = LogDataset(test_encodings, list(y_test))

    training_args = TrainingArguments(
        output_dir="./bert_logs",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_dir="./bert_logs",
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset
    )

    trainer.train()

    model.save_pretrained("ml/bert_model")
    tokenizer.save_pretrained("ml/bert_model")


if __name__ == "__main__":
    train_bert()
