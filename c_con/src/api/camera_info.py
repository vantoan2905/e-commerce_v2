from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session
from src.service.camera_service.camera_info import CameraInfo
from src.database.database import get_db
from src.schemas.camera import CameraBase, CameraResponse,CameraCreate, CameraUpdate

cam_info_router = APIRouter(prefix="/api/camera_info")


@cam_info_router.get("/")
async def get_all_cameras(db: Session = Depends(get_db)):
    """
    Retrieve all records from the camera table.

    Returns:
        dict: A dictionary containing a list of all camera records, under the key "cameras".
    """
    camera_detail_model = CameraInfo(db)
    cameras = camera_detail_model.get_all_cameras()
    print(cameras)
    return {"cameras": cameras}

@cam_info_router.post("/")
async def create_camera(camera: CameraCreate, db: Session = Depends(get_db)):
    """
    Create a new camera record.

    Parameters:
        camera (CameraCreate): The camera object containing the values to be inserted into the database.

    Returns:
        dict: A dictionary containing the newly created camera record, under the key "camera".
    """

    camera_detail_model = CameraInfo(db)
    new_camera = camera_detail_model.create_camera(camera)
    return {"camera": new_camera}

@cam_info_router.get("/{key_camera}/")
async def get_camera_by_key(key_camera: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific camera record by its key.

    Parameters:
        key_camera (str): The unique key of the camera.

    Returns:
        dict: A dictionary containing the camera record, under the key "camera", if found.
              Otherwise, raises an HTTPException with status code 404 and detail "Camera not found".
    """
    camera_detail_model = CameraInfo(db)
    camera = camera_detail_model.get_camera_by_key(key_camera)
    if camera is None:
        raise HTTPException(status_code=404, detail="Camera not found")
    return {"camera": camera}

@cam_info_router.put("/{key_camera}/")
async def update_camera(key_camera: str, camera: CameraUpdate, db: Session = Depends(get_db)):
    """
    Update a camera record.

    Parameters:
        key_camera (str): The unique key of the camera.
        camera (CameraUpdate): The camera object containing the values to be updated in the database.

    Returns:
        dict: A dictionary containing the updated camera record, under the key "camera", if found.
              Otherwise, raises an HTTPException with status code 404 and detail "Camera not found".
    """
    camera_detail_model = CameraInfo(db)
    updated_camera = camera_detail_model.update_camera(camera)
    return {"camera": updated_camera}

@cam_info_router.delete("/{key_camera}/")
async def delete_camera(key_camera: str, db: Session = Depends(get_db)):
    """
    Delete a camera record by its unique key.

    Parameters:
        key_camera (str): The unique key of the camera.

    Returns:
        dict: A dictionary containing the deleted camera record, under the key "camera", if found.
              Otherwise, raises an HTTPException with status code 404 and detail "Camera not found".
    """

    camera_detail_model = CameraInfo(db)
    deleted_camera = camera_detail_model.delete_camera(key_camera)
    return {"camera": deleted_camera}

