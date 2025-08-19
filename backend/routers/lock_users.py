from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import shutil
import uuid
import os

from backend.database.database import get_db
from backend.security.oauth2 import get_current_admin
from backend.models.admins import Admin
from backend.models.lock_users import User
from backend.schemas.lock_user import UserOut
from backend.services.lock_users_service import delete_user_with_fingerprint


router = APIRouter(prefix="/api/lock-users", tags=["lock-users"])

#GET all users
@router.get("/", response_model=List[UserOut])
def read_users(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    users = db.query(User).all()
    return users

#GET ONE user by id
@router.get("/{user_id}", response_model=UserOut)
def read_user(
    user_id: str, db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == str(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#UPDATE ONE user
@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: str,
    firstname: str = Form(...),
    lastname: str = Form(...),

    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    
    #Get by id
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.firstname = firstname
    user.lastname = lastname
    user.role = "user"  
    
    db.commit()
    db.refresh(user)
    return user


#DELETE ONE user
@router.delete("/{user_id}", response_model=UserOut)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    return await delete_user_with_fingerprint(db, user_id)
