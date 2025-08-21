from pydantic import BaseModel, EmailStr, Field
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
    email: EmailStr = Field(..., min_length=6, max_length=100) 
    password: str = Field(..., min_length=6, max_length=100) 
    
class AdminUpdate(BaseModel):
    firstname: Optional[str] = Field(None, min_length=1, max_length=50)    
    lastname: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[str] = Field(None, min_length=5, max_length=100)
    password: Optional[str] = Field(None, min_length=6, max_length=100)

class AdminOut(BaseModel):
    id: str
    email: EmailStr
    firstname: Optional[str]
    lastname: Optional[str]
    role: Optional[UserRole]

    model_config = {
        "from_attributes": True
    }

class AdminTokenData(BaseModel):
    email: EmailStr

class TokenOut(BaseModel):
    access_token: str
    token_type: str
