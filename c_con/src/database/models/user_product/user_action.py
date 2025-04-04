from sqlalchemy import Column, Integer, Enum, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database.base import Base
from sqlalchemy.orm import relationship

# -------------------------------------------------------------
# UserAction Model
# -------------------------------------------------------------



class UserAction(Base):
    __tablename__ = "user_actions"

    action_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("user_sessions.session_id"), nullable=False)
    action_type = Column(Enum("click", "purchase", "add_to_cart", "remove_from_cart", name="action_type_enum"), nullable=False)
    action_detail = Column(Text)
    action_time = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("UserSession", back_populates="user_actions")

    def __repr__(self):
        return f"<UserAction(id={self.action_id}, type={self.action_type})>"
