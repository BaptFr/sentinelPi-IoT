import uuid
from uuid import UUID
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy import Column, Integer, String
from backend.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    lastname = Column(String, unique=True, index=True, nullable=False)
    firstname = Column(String, nullable=False)
    fingerprint = Column(String, nullable=True)
    face_data = Column(String, nullable=True)
    role = Column(String, nullable=True)
    