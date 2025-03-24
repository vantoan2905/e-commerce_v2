from sqlalchemy.orm import Session
from e_server.c_con.src.database.models.camera_model import Camera


class CameraVideo:
    def __init__(self, db: Session):
        self.db = db

    def get_url_camera(self, key_camera: str):
        """
        Retrieve the camera record by its unique key.

        Parameters:
            key_camera (str): The unique key of the camera.

        Returns:
            Camera: The camera record if found, otherwise None.
        """
        return self.db.query(Camera).filter(Camera.key_camera == key_camera).first()