import os
from sqlalchemy.orm import Session
from backend.models.admins import Admin
from backend.models.enums import UserRole
from backend.security.hashing import hash_password
from backend.core.config import settings 

def init_admin(db: Session):
    
    default_email = settings.DEFAULT_ADMIN_EMAIL
    default_password = settings.DEFAULT_ADMIN_PASSWORD

    if not default_email or not default_password:
        print(" No default Admin in the environment")
        return

    #Existing Admin control
    existing_admin = db.query(Admin).filter(Admin.email == default_email).first()
    if existing_admin:
        print("Default Admin existing. Skeeping creation.")
        return

    admin = Admin(
        email=default_email,
        hashed_password=hash_password(default_password),
        firstname="Default",
        lastname="Admin",
        role=UserRole.admin
    )
    db.add(admin)
    db.commit()
    print("Default Admin created")
    