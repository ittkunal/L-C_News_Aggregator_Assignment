from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationBase(BaseModel):
    type: str
    keywords: Optional[str]
    enabled: bool

class NotificationCreate(NotificationBase):
    user_id: int

class Notification(NotificationBase):
    id: int
    user_id: int
    last_sent: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True