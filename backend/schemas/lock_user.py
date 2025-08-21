from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from backend.models.enums import UserRole


class UserCreate(BaseModel):
    lastname: str
    firstname: str
    fingerprint_id: Optional[str] = None  #TEMP !!
    enrollment_id: Optional[str] = None #TEMP !!
    role: UserRole = UserRole.user

class EnrollmentConfirm(BaseModel):
    enrollment_id: str
    fingerprint_id: str
    device_id: str

class UserOut(BaseModel):
    id: UUID
    lastname: str
    firstname: str
    fingerprint_id: Optional[str] = None # TEMP !!
    enrollment_id: Optional[str] = None
    role: UserRole

    model_config = {
        "from_attributes": True
    }

class UserUpdate(BaseModel):
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    fingerprint_id: Optional[str] = None
    enrollment_id: Optional[str] = None
    role: UserRole.user
