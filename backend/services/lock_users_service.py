from sqlalchemy.orm import Session
from backend.models.lock_users import User

def create_user_in_db(
        db: Session,
        user_info: dict,
        fingerprint_path=None,
        face_data_path=None
):
    db_user = User(
        lastname=user_info['lastname'],
        firtname=user_info['firstname'],
        role=user_info['role'],
        fingerprint_path=fingerprint_path,
        face_data_path=face_data_path
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user