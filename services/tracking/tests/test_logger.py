import logging

from shared.logger import log_event, log_error


def test_log_event(caplog):
    with caplog.at_level(logging.INFO):
        log_event({"test": "value"})
        assert "test" in caplog.text


def test_log_error(caplog):
    with caplog.at_level(logging.ERROR):
        log_error("Something went wrong")
        assert "Something went wrong" in caplog.text
