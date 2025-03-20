from sqlalchemy import Boolean, Column, Integer, String, DateTime
from datetime import datetime
from src.database.Base import Base
from typing import List

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=True)
    role = Column(String(50), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, name={self.name}, phone_number={self.phone_number}, role={self.role}, created_at={self.created_at})"
        # return f"User(id={self.user_id}, username={self.username}, email={self.email}, name={self.name}, role={self.role}, created_at={self.created_at})"
    

