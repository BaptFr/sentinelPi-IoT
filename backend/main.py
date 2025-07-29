from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.database.database import SessionLocal, engine, Base
from backend.models.user import User
from backend.schemas.user import UserCreate
from backend.schemas.user import UserOut

Base.metadata.create_all(bind=engine)

app = FastAPI()

#Gestion session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#Routes
@app.get("/")
def read_root():
    return {"message": "Backend is running "}

#POST Ajout utilisateur
@app.post("/users/", response_model=UserOut)
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

# GET Tous les utilisateurs
@app.get("/users/", response_model=List[UserOut])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


