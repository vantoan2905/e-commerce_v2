from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from src.database import Base
from sqlalchemy.orm import relationship

class TrackingData(Base):
    __tablename__ = "tracking_data"

    tracking_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("user_sessions.session_id"), nullable=False)
    cookie_data = Column(Text)
    pixel_data = Column(Text)
    ad_tracking_code = Column(String(255))
    tracking_time = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("UserSession", back_populates="tracking_data")

    def __repr__(self):
        return f"<TrackingData(id={self.tracking_id})>"
