
from sqlalchemy import  Column, Integer, String, DateTime, Text
from datetime import datetime
from database.Base import Base
from sqlalchemy.orm import relationship
import datetime
class Camera(Base):
    __tablename__ = "cameras"
    id = Column(Integer, primary_key=True, index=True)
    camera_name = Column(String(255), nullable=False)
    key_camera = Column(String(255), unique=True, nullable=False)  # Thêm unique=True ở đây
    password = Column(String(255), nullable=False)
    camera_url = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    # users = relationship(
    #     "User",
    #     secondary="user_camera",
    #     back_populates="cameras"
    # )
    # events = relationship("Event", back_populates="camera")

    def __repr__(self):
        return f"Camera(id={self.id}, camera_name={self.camera_name}, camera_url={self.camera_url}, key_camera={self.key_camera}, password={self.password}, location={self.location}, status={self.status}, created_at={self.created_at})"