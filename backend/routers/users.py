from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.models.user import User
from backend.schemas.user import UserOut
from typing import List

from backend.database.database import SessionLocal, get_db
from backend.models.user import User
from backend.schemas.user import UserCreate, UserOut


router = APIRouter(prefix="/users", tags=["users"])




# GET all
@router.get("/", response_model=List[UserOut])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

#POST Ajout utilisateur
@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
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

#GET user by id
@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: str, db: Session = Depends(get_db)):
    print(f"Recherche user id: {user_id}")
    user = db.query(User).filter(User.id == str(user_id)).first()
    print(f"Résultat user: {user}")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
