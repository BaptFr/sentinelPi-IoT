from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    lastname: str
    firstname: str
    birthdate: Optional[str]  #format de date ???
    fingerprint: Optional[str]
    face_data: Optional[str]
    role: Optional[str] = "user"

class UserOut(BaseModel):
    id: int
    lastname: str
    firstname: str
    birthdate: Optional[str]
    fingerprint: Optional[str]
    face_data: Optional[str]
    role: Optional[str]

    model_config = {
        "from_attributes": True
    }