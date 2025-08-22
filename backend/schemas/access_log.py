from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccessLogBase(BaseModel):
    status: str 
    fingerprint_id: Optional[int] = None
    accuracy_score: Optional[str] = None
    device_id: Optional[str] = "Serrure 1"
    user_id: Optional[str] = None

class AccessLogCreate(BaseModel):
    status: str 
    fingerprint_id: Optional[int] = None
    accuracy_score: Optional[str] = None
    device_id: Optional[str] = "Serrure 1"
    user_id: Optional[str] = None
    user_firstname: Optional[str] = None  
    user_lastname: Optional[str] = None   

class AccessLogResponse(AccessLogCreate):
    id: str
    access_time: str
    user_id: Optional[str] = None
    user_lastname: Optional[str] = None
    user_firstname: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class AccessLogRequest(BaseModel):
    status: str
    position: Optional[int] = None
    score: Optional[str] = None
