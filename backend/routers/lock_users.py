from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import shutil
import uuid
import os

from backend.database.database import get_db
from backend.models.admins import Admin
from backend.models.lock_users import User
from backend.schemas.lock_user import UserCreate, UserOut, UserUpdate
from backend.security.oauth2 import get_current_admin


router = APIRouter(prefix="/lock-users", tags=["lock-users"])

#GET all users
@router.get("/", response_model=List[UserOut])
def read_users(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    users = db.query(User).all()
    return users

#POST Add user
@router.post("/", response_model=UserOut)
async def create_user(
    firstname: str = Form(...),
    lastname: str = Form(...),
    role: str = Form(...),
    face_data: UploadFile = File(...),
  
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    #Name generation for files
    face_filename = f"faces/{uuid.uuid4()}.{face_data.filename.split('.')[-1]}"

    #File local saving
    with open(f"uploads/{face_filename}", "wb") as fp:
        shutil.copyfileobj(face_data.file, fp)

    db_user = User(
        lastname=lastname,
        firstname=firstname,
        role=role,
        face_data_path=f"/uploads/{face_filename}"
    )


    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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
    face_data: UploadFile = File(None),

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
    
    if face_data:
        face_filename = f"faces/{uuid.uuid4()}.{face_data.filename.split('.')[-1]}"
        with open(f"uploads/{face_filename}", "wb") as fp:
            shutil.copyfileobj(face_data.file, fp)
        user.face_data_path = f"/uploads/{face_filename}"

    db.commit()
    db.refresh(user)
    return user


#DELETE ONE user
@router.delete("/{user_id}", response_model=UserOut)
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):

    user= db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    #supp et finaliser
    db.delete(user)
    db.commit()
    return user
