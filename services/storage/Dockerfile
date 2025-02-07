FROM python:3.11-slim

WORKDIR /app

COPY services/storage/ /app/
COPY shared/ /app/shared/
COPY services/storage/init.sql /docker-entrypoint-initdb.d/init.sql

RUN pip install --upgrade pip && pip install /app/shared && pip install .

CMD ["uvicorn", "src.interface.api.main:app", "--host", "0.0.0.0", "--port", "8040"]
