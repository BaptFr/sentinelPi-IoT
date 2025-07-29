from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from backend.models.enums import UserRole

class UserCreate(BaseModel):
    lastname: str
    firstname: str
    fingerprint: Optional[str]
    face_data: Optional[str]
    role: UserRole

class UserOut(BaseModel):
    id: UUID
    lastname: str
    firstname: str
    fingerprint: Optional[str]
    face_data: Optional[str]
    role: Optional[str]

    model_config = {
        "from_attributes": True
    }
class UserUpdate(BaseModel):
    lastname: str
    firstname: str
    fingerprint: Optional[str]
    face_data: Optional[str]
    role: Optional[str]