from sqlalchemy import Column, Integer, String, DateTime

from datetime import datetime, timezone
import uuid

from backend.database.database import Base


class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(String, primary_key=True, index=True)
    access_time = Column(String, nullable=True)  #Debug: utc.now deprecated
    status = Column(String, nullable=False)
    device_id = Column(String, default="Serrure 1")
    fingerprint_id = Column(String, nullable=True)
    user_id = Column(String, nullable=True)
    accuracy_score = Column(String, nullable=True) 
    user_firstname = Column(String, nullable=True)
    user_lastname = Column(String, nullable=True)

    
