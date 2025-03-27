from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database.base  import Base
from sqlalchemy.orm import relationship

class SearchHistory(Base):
    __tablename__ = "search_history"

    search_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("user_sessions.session_id"), nullable=False)
    keyword = Column(String(255))
    search_time = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("UserSession", back_populates="search_history")

    def __repr__(self):
        return f"<SearchHistory(id={self.search_id}, keyword={self.keyword})>"
