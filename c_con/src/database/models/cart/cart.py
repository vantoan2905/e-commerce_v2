
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime, func
from sqlalchemy.orm import relationship
from src.database.base import Base
# -------------------------------------------------------------
# Cart Model
# -------------------------------------------------------------
class Cart(Base):
    __tablename__ = "cart"
    cart_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    session_id = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    total_items = Column(Integer, nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", back_populates="cart")



