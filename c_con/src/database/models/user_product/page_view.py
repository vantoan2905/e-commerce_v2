from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database.base import Base
from sqlalchemy.orm import relationship

class PageView(Base):
    __tablename__ = "page_views"

    view_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("user_sessions.session_id"), nullable=False)
    url = Column(String(255))
    view_start = Column(DateTime(timezone=True), server_default=func.now())
    view_duration = Column(Integer)

    session = relationship("UserSession", back_populates="page_views")

    def __repr__(self):
        return f"<PageView(view_id={self.view_id}, url={self.url})>"
