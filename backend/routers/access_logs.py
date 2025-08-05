from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.schemas.access_log import AccessLogCreate, AccessLogResponse
from backend.services.access_log import create_access_log

router = APIRouter(
    prefix="/access-logs",
    tags=["Access Logs"]
)

@router.post("/", response_model=AccessLogResponse, status_code=status.HTTP_201_CREATED)
def log_access(log: AccessLogCreate, db: Session = Depends(get_db)):
    return create_access_log(log, db)
