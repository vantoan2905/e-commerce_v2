from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.database.base import Base
# -------------------------------------------------------------
# CartDetail Model
# -------------------------------------------------------------

class CartDetail(Base):
    __tablename__ = "cart_details"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    cart = relationship("Cart", back_populates="cart_details")
    product = relationship("Product", back_populates="cart_details")


