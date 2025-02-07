FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY services/ingestion/ /app/
COPY shared/ /app/shared/

RUN pip install --upgrade pip && pip install hatch
RUN pip install /app/shared
RUN pip install .

ENV PYTHONPATH=/app:/app/src

CMD ["python", "-m", "src.application.services.event_consumer"]
