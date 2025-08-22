from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
from backend.models.access_logs import AccessLog
from backend.schemas.access_log import AccessLogCreate, AccessLogResponse, AccessLogRequest
from backend.services.access_logs_service import  create_access_log, get_user_by_fingerprint_id
from backend.database.database import get_db
from typing import List, Optional

router = APIRouter(prefix="/api/logs", tags=["logs"])

#GET logs saved
@router.get("/access", response_model=List[AccessLogResponse])
async def get_access_logs_endpoint(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(AccessLog)

    if status:
        query = query.filter(AccessLog.status == status)

    logs = query.order_by(desc(AccessLog.access_time)).offset(skip).limit(limit).all()

    return logs
