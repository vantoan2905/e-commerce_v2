from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database.base import Base
from sqlalchemy.orm import relationship

# -------------------------------------------------------------
# FavoriteProduct Model
# -------------------------------------------------------------



class FavoriteProduct(Base):
    __tablename__ = "favorite_products"

    fav_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    added_time = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="favorite_products")
    product = relationship("Product", back_populates="favorite_products")

    def __repr__(self):
        return f"<FavoriteProduct(id={self.fav_id}, product_id={self.product_id})>"
