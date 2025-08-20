from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI

import asyncio
from backend.routers.admin import router as admin_router
from backend.routers.lock_users import router as lock_users_router
from backend.routers.enrollment import router as enrollment_router
from backend.routers.access_logs import router as access_logs_router
from backend.routers.websocket import router as websocket_router
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

#Cors middlewares 
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
  
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

#Routes
app.include_router(admin_router)
app.include_router(lock_users_router)
app.include_router(enrollment_router)
app.include_router(access_logs_router)
app.include_router(websocket_router)

#Root
@app.get("/")
def read_root():
    return {"message": "Backend is running "}

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor_connections())

