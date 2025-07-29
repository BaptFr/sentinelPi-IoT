from fastapi import FastAPI
from backend.routers import users
from backend.database.database import SessionLocal, engine, Base

#DB table creation
Base.metadata.create_all(bind=engine)

app = FastAPI()

#Routes
app.include_router(users.router)

#Root
@app.get("/")
def read_root():
    return {"message": "Backend is running "}

# #POST Ajout utilisateur
# @app.post("/users/", response_model=UserOut)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):

#     db_user = User(
#         lastname=user.lastname,
#         firstname=user.firstname,
#         role=user.role,
#         fingerprint=user.fingerprint,
#         face_data=user.face_data
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user



# # GET un utilisateur by id
# @app.get("/users/{user_id}", response_model=UserOut)
# def read_user(user_id: str, db: Session = Depends(get_db)):
#     try:
#         # Vérifie que l'user_id est bien un UUID
#         uid = UUID(user_id)
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid UUID format")

#     db_user = db.query(User).filter(User.id == str(uid)).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

