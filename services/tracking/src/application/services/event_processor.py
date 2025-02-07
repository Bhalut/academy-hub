import datetime
import os

import httpx
import redis

from shared.logger import log_error

INGESTION_SERVICE_URL = os.getenv("INGESTION_SERVICE_URL", "http://ingestion:8020")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def serialize_event_data(event_data):
    if isinstance(event_data, dict):
        return {key: serialize_event_data(value) for key, value in event_data.items()}
    elif isinstance(event_data, list):
        return [serialize_event_data(item) for item in event_data]
    elif isinstance(event_data, datetime.datetime):
        return event_data.isoformat()
    return event_data


async def process_event(event_data: dict):
    try:
        event_data = serialize_event_data(event_data)
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{INGESTION_SERVICE_URL}/events/",
                json=event_data,
                timeout=2.0,
            )
            response.raise_for_status()
            return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        log_error(f"Ingestion unreachable, storing event in Redis queue: {str(e)}")
        r.rpush("tracking_failed_events", event_data)
        return {"error": "Ingestion service not available, event stored in redis"}
