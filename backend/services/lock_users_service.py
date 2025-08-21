from sqlalchemy.orm import Session
from fastapi import HTTPException

from backend.models.lock_users import User
from backend.core.config import settings
from backend.websocket.manager import manager

def create_user_in_db(
        db: Session,
        user_info: dict,
        fingerprint_id=None,
        enrollment_id=None
):
    db_user = User(
        lastname=user_info['lastname'],
        firstname=user_info['firstname'],
        role=user_info['role'],
        fingerprint_id=fingerprint_id,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

RASPBERRY_URL = settings.RASPBERRY_URL

async def delete_user_with_fingerprint(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    fingerprint_id = user.fingerprint_id
    
    #If no fngrprnt erasing only User in DB
    if fingerprint_id is None:
        db.delete(user)
        db.commit()
        return user
    #Else deleting fingerprint raspberry  the User in DB
    payload = {
        "action": "delete_fingerprint",
        "fingerprint_id": fingerprint_id,
        "user_id": user_id
    }
    try:
        #WS manager method
        success = await manager.send_message_to_device(payload)
        if not success:
            raise HTTPException(status_code=500, detail=f"Error deletion fingerprint in Raspberry: {resp.text}")
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calling Raspberry: {e}")
    
    
    deleted_user = user
    db.delete(user)
    db.commit()
    return deleted_user
