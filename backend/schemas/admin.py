from pydantic import BaseModel, EmailStr
from typing import Optional
from backend.models.enums import UserRole

#intial creation
class AdminCreate(BaseModel):
    email: EmailStr
    password: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    role: UserRole = UserRole.admin

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class AdminUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    role: Optional[str] = None

class AdminOut(BaseModel):
    id: str
    email: EmailStr
    firstname: Optional[str]
    lastname: Optional[str]
    role: Optional[str]

    model_config = {
        "from_attributes": True
    }

class AdminTokenData(BaseModel):
    email: EmailStr

class TokenOut(BaseModel):
    access_token: str
    token_type: str
