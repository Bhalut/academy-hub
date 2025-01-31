import hashlib
import uuid
from datetime import datetime

def generate_event_id() -> str:
    return str(uuid.uuid4())

def hash_string(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()

def get_current_timestamp() -> str:
    return datetime.utcnow().isoformat()
