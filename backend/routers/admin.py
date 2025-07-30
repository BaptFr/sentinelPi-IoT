from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from backend.models.admins import Admin
from backend.schemas.admin import AdminCreate, AdminOut, AdminLogin, TokenOut
from backend.models.enums import UserRole
from backend.database.database import get_db
from backend.security.hashing import hash_password, verify_password
from backend.security.token import create_access_token
from backend.security.oauth2 import get_current_admin
from backend.core.config import settings

router = APIRouter(prefix="/admin", tags=["admin"])

#Admin by default creation
@router.post("/", response_model=AdminOut)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    existing_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin already exists")

    new_admin = Admin(
        email=admin.email,
        hashed_password=hash_password(admin.password),
        firstname=admin.firstname,
        lastname=admin.lastname,
        role=UserRole.admin
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

#Login Admin
@router.post("/login", response_model=TokenOut)
def login_admin(admin_login: AdminLogin, db: Session = Depends(get_db)):
    # Find Admin by email
    admin = db.query(Admin).filter(Admin.email == admin_login.email).first()
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(admin_login.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


#Login Get
@router.get("/profile")
def read_profile(current_admin: Admin = Depends(get_current_admin)):
    return current_admin