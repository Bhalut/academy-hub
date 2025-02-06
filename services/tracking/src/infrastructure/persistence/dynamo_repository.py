import os
from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

from shared.logger import log_error, log_event
from shared.repository.base_repository import BaseRepository

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMO_TABLE_NAME = os.getenv("DYNAMO_TABLE_NAME", "TrackingEvents")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMO_TABLE_NAME)


class DynamoRepository(BaseRepository):
    async def insert(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            table.put_item(Item=data)
            log_event({"dynamo_insert_success": data})
            return data
        except ClientError as e:
            log_error(f"Database error: {e.response['Error']['Message']}")
            raise HTTPException(status_code=500, detail=f"Database error: {e.response['Error']['Message']}")

    async def find_by_id(self, collection: str, id: str) -> Optional[Dict[str, Any]]:
        try:
            response = table.get_item(Key={"id": id})
            return response.get("Item", None)
        except ClientError as e:
            log_error(f"Database lookup error: {e.response['Error']['Message']}")
            return None

    async def find_all(self, collection: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            scan_kwargs = {"FilterExpression": None}
            if filters:
                from boto3.dynamodb.conditions import Attr
                filter_expression = None
                for key, value in filters.items():
                    condition = Attr(key).eq(value)
                    filter_expression = condition if not filter_expression else filter_expression & condition
                scan_kwargs["FilterExpression"] = filter_expression

            response = table.scan(**scan_kwargs)
            return response.get("Items", [])
        except ClientError as e:
            log_error(f"Database query error: {e.response['Error']['Message']}")
            return []

    async def update(self, collection: str, id: str, update_data: Dict[str, Any]) -> bool:
        try:
            update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in update_data.keys())
            expression_values = {f":{k}": v for k, v in update_data.items()}

            response = table.update_item(
                Key={"id": id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues="UPDATED_NEW",
            )
            return "Attributes" in response
        except ClientError as e:
            log_error(f"Database update error: {e.response['Error']['Message']}")
            raise HTTPException(status_code=500, detail=f"Database update error: {e.response['Error']['Message']}")

    async def delete(self, collection: str, id: str) -> bool:
        try:
            response = table.delete_item(Key={"id": id})
            return "Attributes" in response
        except ClientError as e:
            log_error(f"Database delete error: {e.response['Error']['Message']}")
            raise HTTPException(status_code=500, detail=f"Database delete error: {e.response['Error']['Message']}")
