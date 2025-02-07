import os
from typing import Any, Dict

import boto3
import motor.motor_asyncio
import psycopg2
from botocore.exceptions import ClientError
from fastapi import HTTPException
from psycopg2.extras import RealDictCursor

from shared.logger import log_error, log_event
from shared.repository.base_repository import BaseRepository

# MongoDB Config (para raw logs)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
mongo_db = mongo_client["tracking"]

# DynamoDB Config (para raw logs en producción)
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMO_TABLE_NAME = os.getenv("DYNAMO_TABLE_NAME", "TrackingEvents")
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
dynamo_table = dynamodb.Table(DYNAMO_TABLE_NAME)

# PostgreSQL Config (para datos procesados)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "tracking_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

try:
    postgres_conn = psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
        cursor_factory=RealDictCursor
    )
    postgres_conn.autocommit = True
except Exception as e:
    log_error(f"Error connecting to PostgreSQL: {str(e)}")
    postgres_conn = None


class StorageRepository(BaseRepository):
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development").lower()

    async def insert_raw(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Guarda los raw logs en MongoDB o DynamoDB"""
        try:
            if self.environment == "production":
                dynamo_table.put_item(Item=data)
            else:
                await mongo_db[collection].insert_one(data)

            log_event({"raw_insert_success": data})
            return data
        except ClientError as e:
            log_error(f"Database error: {e.response['Error']['Message']}")
            raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")

    def insert_processed(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Guarda los datos procesados en PostgreSQL"""
        if not postgres_conn:
            log_error("PostgreSQL connection is not available")
            raise HTTPException(status_code=500, detail="PostgreSQL connection unavailable")

        try:
            with postgres_conn.cursor() as cursor:
                columns = ', '.join(data.keys())
                values = ', '.join(['%s'] * len(data))
                sql = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING *"
                cursor.execute(sql, list(data.values()))
                result = cursor.fetchone()

            log_event({"processed_insert_success": result})
            return result
        except Exception as e:
            log_error(f"PostgreSQL error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"PostgreSQL error: {str(e)}")
