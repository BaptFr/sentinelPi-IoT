import uuid
from uuid import UUID
from sqlalchemy import Column, String
from sqlalchemy.types import Enum as SQLAlchemyEnum
from backend.database.database import Base
from backend.models.enums import UserRole

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    lastname = Column(String, index=True, nullable=False)
    firstname = Column(String, nullable=False)
    fingerprint_id = Column(String, nullable=True) 
    enrollment_id = Column(String, nullable=True) 
    role = Column(SQLAlchemyEnum(UserRole), nullable=False, default=UserRole.user)
