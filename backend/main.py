from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.routers.admin import router as admin_router
from backend.routers.lock_users import router as lock_users_router
from backend.database.database import SessionLocal, engine, Base
from backend.core.init_admin import init_admin

#DB table creation
Base.metadata.create_all(bind=engine)

@asynccontextmanager
#Admin ? | Default Admin
async def lifespan(app: FastAPI):
    with SessionLocal() as db:
        init_admin(db)
    yield

app = FastAPI(lifespan=lifespan)

#Routes
app.include_router(admin_router)
app.include_router(lock_users_router)

#Root
@app.get("/")
def read_root():
    return {"message": "Backend is running "}
