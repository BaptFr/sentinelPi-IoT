from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from backend.models.enums import UserRole

class UserCreate(BaseModel):
    lastname: str
    firstname: str
    fingerprint: Optional[str]
    face_data: Optional[str]
    role: UserRole = UserRole.user

class UserOut(BaseModel):
    id: UUID
    lastname: str
    firstname: str
    fingerprint: Optional[str]
    face_data: Optional[str]
    role: Optional[UserRole]

    model_config = {
        "from_attributes": True
    }
class UserUpdate(BaseModel):
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    fingerprint: Optional[str] = None
    face_data: Optional[str] = None
    role: Optional[UserRole] = None