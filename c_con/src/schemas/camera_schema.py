from pydantic import BaseModel
from datetime import datetime



class CameraBase(BaseModel):
    id: int
    camera_name: str
    camera_url: str
    key_camera: str
    password: str
    location: str
    status: str
    created_at: datetime

class CameraResponse(CameraBase):
    class Config:
        from_attributes = True

class CameraUpdate(CameraBase):
    id: int
    camera_name: str
    camera_url: str
    key_camera: str
    password: str
    location: str
    status: str
    created_at: datetime

class CameraCreate(CameraBase):
    camera_name: str
    camera_url: str
    key_camera: str
    password: str
    location: str
    status: str
    created_at: datetime