from sqlalchemy.orm import Session
from fastapi import HTTPException

from backend.models.lock_users import User
from backend.core.config import settings
import requests


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

def delete_user_with_fingerprint(db, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    fingerprint_id = user.fingerprint_id

    if fingerprint_id is not None:
        try:
            url = f"{RASPBERRY_URL}/delete_fingerprint/{fingerprint_id}"
            resp = requests.delete(url, timeout=10)
            if resp.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Erreur suppression empreinte Raspberry: {resp.text}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur appel Raspberry: {e}")
    deleted_user = user
    db.delete(user)
    db.commit()
    return deleted_user

    