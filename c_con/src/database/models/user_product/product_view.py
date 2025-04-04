from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database.base import Base
from sqlalchemy.orm import relationship
# -------------------------------------------------------------
# ProductView Model
# -------------------------------------------------------------
class ProductView(Base):
    __tablename__ = "product_views"

    view_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("user_sessions.session_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    view_time = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("UserSession", back_populates="product_views")
    product = relationship("Product", back_populates="product_views")

    def __repr__(self):
        return f"<ProductView(id={self.view_id}, product_id={self.product_id})>"
