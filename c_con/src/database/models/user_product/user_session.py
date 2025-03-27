from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database.base import Base
from sqlalchemy.orm import relationship

class UserSession(Base):
    __tablename__ = "user_sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    ip_address = Column(String(45))
    location = Column(String(255))
    device_info = Column(String(255))
    browser = Column(String(255))
    session_start = Column(DateTime(timezone=True), server_default=func.now())
    session_end = Column(DateTime(timezone=True))

    user = relationship("User", back_populates="sessions")
    page_views = relationship("PageView", back_populates="session")
    user_actions = relationship("UserAction", back_populates="session")
    search_history = relationship("SearchHistory", back_populates="session")
    product_views = relationship("ProductView", back_populates="session")
    tracking_data = relationship("TrackingData", back_populates="session")

    def __repr__(self):
        return f"<UserSession(id={self.session_id}, user_id={self.user_id})>"
