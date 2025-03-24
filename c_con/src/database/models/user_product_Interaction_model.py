
from sqlalchemy import  Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from src.database.Base import Base
from sqlalchemy.orm import relationship
import datetime


class UserProductInteraction(Base):
    __tablename__ = "user_product_interactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    interaction_type = Column(String(50), nullable=False)  
    rating = Column(Integer, nullable=True)  
    review = Column(Text, nullable=True)     
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="product_interactions")
    product = relationship("Product", back_populates="product_interactions")