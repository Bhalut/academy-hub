"""
Module for logging events, errors and debug messages.
Logs are sent to a file or to the console.
"""

import json
import logging
from logging import Logger

LOG_FILE = "/var/log/tracking_service.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger: Logger = logging.getLogger(__name__)


def log_event(event_data: dict) -> None:
    """
    Records an event at the INFO level.

    Args:
        event_data (dict): Dictionary with event data.
    """
    logger.info(json.dumps({"event": event_data}))


def log_error(message: str) -> None:
    """
    Logs an error message.

    Args:
        message (str): Error message.
    """
    logger.error(json.dumps({"error": message}))


def log_debug(message: str) -> None:
    """
    Log a debug message.

    Args:
        message (str): Debug message.
    """
    logger.debug(json.dumps({"debug": message}))


def log_warning(message: str) -> None:
    """
    Logs a warning message.

    Args:
        message (str): Warning message.
    """
    logger.warning(json.dumps({"warning": message}))
