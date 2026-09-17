from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("emergency_requests.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(200), nullable=False)
    message = Column(String(500), nullable=False)
    notification_type = Column(String(50), default="EMERGENCY_DISPATCH") # EMERGENCY_DISPATCH, VOLUNTEER_ACCEPT, STATUS_UPDATE
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    request = relationship("EmergencyRequest", back_populates="notifications")
