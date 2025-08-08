from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.schemas.access_log import AccessLogCreate, AccessLogResponse, AccessLogRequest
from backend.services.access_logs_service import  create_access_log, get_access_logs, get_user_by_fingerprint_id
from backend.database.database import get_db
from typing import List, Optional

router = APIRouter(prefix="/api/logs", tags=["logs"])

#POST : Logs from lock
@router.post("/access", response_model=AccessLogResponse)
async def log_access_attempt(log_data: AccessLogRequest, db: Session = Depends(get_db)):
    print("access called ")
    print("received data :{log_data}")
    
    try:
        user_id = None
        
        #If position get fingerprint_id and user
        if log_data.position is not None:
            user = get_user_by_fingerprint_id(db, log_data.position)
            user_id = user.id if user else None
        
        #Creation of a log
        log_entry = AccessLogCreate(
            status=log_data.status,
            fingerprint_id=log_data.position,
            accuracy_score=str(log_data.score),
            user_id=user_id,
            device_id="Serrure 1"
        )
        
        return create_access_log(db, log_entry)
        
    except Exception as e:
        print(f"Error saving access log: {e}")
        raise HTTPException(status_code=500, detail="Failed to save log")


#GET logs saved
@router.get("/access", response_model=List[AccessLogResponse])
async def get_access_logs_endpoint(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return get_access_logs(db, skip=skip, limit=limit, status_filter=status)
