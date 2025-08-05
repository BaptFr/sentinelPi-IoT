from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from backend.database.database import Base

class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True)
    fingerprint_id = Column(Integer, nullable=False)
    status = Column(String, default="success")  # "success" ou "failure"
    device_id = Column(String, nullable=True)
    access_time = Column(DateTime, default=datetime.utcnow)
