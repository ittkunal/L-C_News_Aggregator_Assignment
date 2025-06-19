import uuid
from datetime import datetime, timedelta

def generate_session_token():
    return str(uuid.uuid4())

def get_expiry(hours=24):
    return datetime.utcnow() + timedelta(hours=hours)