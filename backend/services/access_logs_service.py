from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc
from datetime import datetime, timezone
import uuid
import pytz

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
    #Date/Hour France
    paris_tz = pytz.timezone('Europe/Paris')
    generated_time = datetime.now(paris_tz)
    formatted_time = generated_time.strftime(' Le %d/%m/%Y à %H:%M:%S')

    db_log = AccessLog(
        id=generated_id,                    
        access_time=formatted_time,         
        status=log_data.status,
        fingerprint_id=log_data.fingerprint_id,
        accuracy_score=log_data.accuracy_score,
        device_id=log_data.device_id or "Serrure 1",
        user_id=log_data.user_id,
        user_firstname=log_data.user_firstname,
        user_lastname=log_data.user_lastname
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
        "user_id": log_data.user_id,
       "user_firstname": getattr(log_data, "user_firstname", None),
        "user_lastname": getattr(log_data, "user_lastname", None)
    }

def get_user_by_fingerprint_id(
    db: Session, 
    fingerprint_id: str):
    fingerprint_id = message.get("fingerprint_id")
    print(f"[DEBUG] Reçu fingerprint_id : {fingerprint_id}")

    all_fingerprints = [u.fingerprint_id for u in db.query(User).all()]
    print(f"[DEBUG] Fingerprints en base : {all_fingerprints}")

    user = get_user_by_fingerprint_id(db, fingerprint_id)
    if user:
        print(f"[DEBUG] Utilisateur trouvé : {user.firstname} {user.lastname}")
    else:
        print(f"[DEBUG] Aucun utilisateur trouvé pour fingerprint_id {fingerprint_id}")


    return db.query(User).filter(User.fingerprint_id == str(fingerprint_id)).first()
