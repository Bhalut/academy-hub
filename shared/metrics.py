import logging
import time

from fastapi import FastAPI, Request
from prometheus_client import Histogram, generate_latest, CONTENT_TYPE_LATEST, Counter
from starlette.responses import Response

EVENTS_PROCESSED = Counter("events_processed_total", "Total events processed")
EVENTS_FAILED = Counter("events_failed_total", "Total failed events")
EVENTS_RECEIVED = Counter("events_received_total", "Total events received")

REQUEST_LATENCY = Histogram("request_latency_seconds", "HTTP Request Latency")

logging.basicConfig(level=logging.INFO)


def setup_metrics(app: FastAPI):
    @app.middleware("http")
    async def prometheus_middleware(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        REQUEST_LATENCY.observe(process_time)
        logging.info(f"Request {request.method} {request.url} - {process_time:.3f}s")
        return response

    @app.get("/metrics")
    async def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
