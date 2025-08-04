from sqlalchemy.orm import Session
from backend.models.lock_users import User

def create_user_in_db(
        db: Session,
        user_info: dict,
        fingerprint_id=None,
        face_data_id=None
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