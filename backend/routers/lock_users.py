from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

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
def create_user(
    user: UserCreate, db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    db_user = User(
        lastname=user.lastname,
        firstname=user.firstname,
        role=user.role,
        fingerprint=user.fingerprint,
        face_data=user.face_data
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
    user_id: str, user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    #Get by id
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updates = user_update.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(user, key, value)

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
