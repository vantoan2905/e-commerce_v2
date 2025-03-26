from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from src.database import Base
from sqlalchemy.orm import relationship

class UserProductInteraction(Base):
    __tablename__ = "user_product_interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    interaction_type = Column(String(50), nullable=False)
    rating = Column(Integer, nullable=True)
    review = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    product = relationship("Product")

    def __repr__(self):
        return f"<UserProductInteraction(user_id={self.user_id}, product_id={self.product_id}, type={self.interaction_type})>"
