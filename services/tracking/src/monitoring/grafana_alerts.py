from prometheus_client import Counter

ALERT_HIGH_LATENCY = Counter("high_latency_alerts", "Number of high latency alerts")
ALERT_ERROR_RATE = Counter("error_rate_alerts", "Number of error rate alerts")


def trigger_high_latency_alert():
    ALERT_HIGH_LATENCY.inc()


def trigger_error_rate_alert():
    ALERT_ERROR_RATE.inc()
