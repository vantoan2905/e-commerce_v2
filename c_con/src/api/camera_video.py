
# import routing
from fastapi import APIRouter, WebSocket, HTTPException
# import libraries
import cv2

# import services
from service.camera_service.camera_video import CameraVideo
from database.database import get_db
# create router
cam_video_router = APIRouter()
camera_detail_model = CameraVideo(db = get_db())

@cam_video_router.websocket("/{camera_id}/video")
async def get_video(camera_id: str, websocket: WebSocket):
    camera = camera_detail_model.get_url_camera(camera_id)
    if camera is None:
        raise HTTPException(status_code=404, detail="Camera not found")
    cap = cv2.VideoCapture(camera.url)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        await websocket.send_bytes(frame)

def get_url_video(key_camera: str):
   
    return camera_detail_model.get_url_camera(key_camera)