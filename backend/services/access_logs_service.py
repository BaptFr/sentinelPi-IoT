from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import datetime, timezone
import uuid

from backend.models.access_logs import AccessLog
from backend.schemas.access_log import AccessLogCreate
from backend.models.lock_users import User
from typing import List, Optional
from datetime import datetime

def create_access_log(
        db: Session,
        log_data: AccessLogCreate, 
    )-> dict:

    generated_id = str(uuid.uuid4())
    generated_time = datetime.now(timezone.utc).isoformat()
 
    db_log = AccessLog(
        id=generated_id,                    
        access_time=generated_time,         
        status=log_data.status,
        fingerprint_id=log_data.fingerprint_id,
        accuracy_score=log_data.accuracy_score,
        device_id=log_data.device_id or "Serrure 1",
        user_id=log_data.user_id
    )
    
    db.add(db_log)
    db.commit()
    
    return {
        "id": generated_id,
        "access_time": generated_time,
        "status": log_data.status,
        "fingerprint_id": log_data.fingerprint_id,
        "accuracy_score": log_data.accuracy_score,
        "device_id": log_data.device_id or "Serrure 1",
        "user_id": log_data.user_id
    }


def get_access_logs(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    status_filter: Optional[str] = None
) -> List[AccessLog]:
    query = db.query(AccessLog)
    
    if status_filter:
        query = query.filter(AccessLog.status == status_filter)
    
    return query.order_by(desc(AccessLog.access_time)).offset(skip).limit(limit).all()

def get_user_by_fingerprint_id(db: Session, fingerprint_id: int):
    return db.query(User).filter(User.fingerprint_id == fingerprint_id).first()
