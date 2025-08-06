from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccessLogCreate(BaseModel):
    fingerprint_id: int
    status: str = "success"
    device_id: Optional[str] = None

class AccessLogResponse(AccessLogCreate):
    id: int
    access_time: datetime

    class Config:
        orm_mode = True
