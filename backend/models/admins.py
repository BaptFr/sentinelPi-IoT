import uuid
from sqlalchemy import Column, String
from sqlalchemy.types import Enum as SQLAlchemyEnum
from backend.database.database import Base
from backend.models.enums import UserRole

class Admin(Base):
    __tablename__ = "admins"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    lastname = Column(String, index=True, nullable=False)
    firstname = Column(String, nullable=False)
    email= Column(String, unique=True, nullable=False)  #mod. unique
    hashed_password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False, default=UserRole.admin)