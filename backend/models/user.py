from sqlalchemy import Column, Integer, String, Date
from backend.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    lastname = Column(String, unique=True, index=True, nullable=False)
    firstname = Column(String, nullable=False)
    birthdate = Column(Date, nullable=True)  #Format date AAAA-MM-JJ
    fingerprint = Column(String, nullable=True)
    face_data = Column(String, nullable=True)
    role = Column(String, nullable=True)