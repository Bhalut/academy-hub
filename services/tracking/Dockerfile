FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY services/tracking/ /app/
COPY shared/ /app/shared/

RUN pip install --upgrade pip && pip install hatch
RUN pip install /app/shared
RUN pip install .

ENV PYTHONPATH=/app:/app/src

CMD ["uvicorn", "src.interface.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
