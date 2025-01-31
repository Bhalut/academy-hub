import json
import logging

LOG_FILE = "/var/log/tracking_service.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)


def log_event(event_data: dict):
    logging.info(json.dumps({"event": event_data}))


def log_error(message: str):
    logging.error(json.dumps({"error": message}))


def log_debug(message: str):
    logging.debug(json.dumps({"debug": message}))


def log_warning(message: str):
    logging.warning(json.dumps({"warning": message}))
