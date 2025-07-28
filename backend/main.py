from fastapi import FastAPI
from sqlalchemy.orm import Session
from backend.database.database import SessionLocal, engine, Base
from backend.models.user import User
from backend.schemas.user import UserCreate
from datetime import datetime

Base.metadata.create_all(bind=engine) #création table une fois

app = FastAPI()

#Gestion session DB 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Route ajout utilisateur
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    birthdate = None
    if user.birthdate:
        try:
            birthdate = datetime.strptime(user.birthdate, "%d/%m/%Y").date()
        except ValueError:
            return {"error": "Date format must be DD/MM/YYYY"}

    db_user = User(
        name=user.name,
        firstname=user.firstname,
        birthdate=birthdate,
        role=user.role,
        fingerprint=user.fingerprint,
        face_data=user.face_data
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User added", "id": db_user.id}


@app.get("/")
def read_root():
    return {"message": "Backend de la serrure connectée opérationnel !"}
