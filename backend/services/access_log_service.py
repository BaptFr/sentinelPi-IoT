from sqlalchemy.orm import Session
from backend.models.access_logs import AccessLog
from backend.schemas.access_log import AccessLogCreate

def create_access_log(log_data: AccessLogCreate, db: Session):
    log = AccessLog(**log_data.dict())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
