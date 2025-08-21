from sqlalchemy.orm import Session
from fastapi import HTTPException

from backend.models.lock_users import User
from backend.core.config import settings
from backend.websocket.manager import manager


DEVICE_ID = settings.DEVICE_ID
RASPBERRY_URL = settings.RASPBERRY_URL

#Create new user in DB
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
    #Else deleting fingerprint raspberry then the User in DB
    payload = {
        "action": "delete_fingerprint",
        "fingerprint_id": fingerprint_id,
        "user_id": user_id
    }
    try:
        #WS manager method Message send verification
        success = await manager.send_message_to_device(message=payload, device_id=DEVICE_ID)
        
        if not success:
            print(f"Erreur WS pour supprimer l'empreinte {fingerprint_id}")
            raise HTTPException(status_code=500, detail="Failed to delete fingerprint")

        confirmed = await manager.wait_for_device_confirmation(fingerprint_id=fingerprint_id)
        #Debug condition to before deleting in DB : Raspberry delete confirmation verification
        if not confirmed:
            print(f"Fingerprint suppresion failed on Raspberry part")
            raise HTTPException(status_code=500, detail="Device failed to delete fingerprint") 
   
    except Exception as e:
            print(f"Exception WS: {e}")
            raise HTTPException(status_code=500, detail=f"WS error: {e}")
    
    
    deleted_user = user
    db.delete(user)
    db.commit()

    return deleted_user
