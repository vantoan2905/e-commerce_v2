from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from src.database.base import Base


from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(20))
    age = Column(Integer)
    gender = Column(Enum("Man", "Woman", "Other", name="gender_enum"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    sessions = relationship("UserSession", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    favorite_products = relationship("FavoriteProduct", back_populates="user")

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
