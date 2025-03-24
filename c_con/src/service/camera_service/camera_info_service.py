from sqlalchemy.orm import Session
from e_server.c_con.src.database.models.camera_model import Camera

class CameraInfo:
    def __init__(self, db: Session):
        """
        Initialize the CameraInfo service with a database session.

        Parameters:
            db (Session): The SQLAlchemy database session used for querying and modifying camera records.
        """

        self.db = db

    def get_all_cameras(self):
        
        """
        Retrieve all records from the camera table.

        Returns:
            list: A list of tuples, each representing a record in the camera table.
        """
        return self.db.query(Camera).all()  
    

    def get_camera_by_key(self, key_camera: str):
        """
        Retrieve a specific camera record by its key.

        Parameters:
            key_camera (str): The unique key of the camera.

        Returns:
            Camera: The camera record if found, otherwise None.
        """
        return self.db.query(Camera).filter(Camera.key_camera == key_camera).first()

    def create_camera(self, camera: Camera):
        """
        Create a new camera record.

        Parameters:
            camera (Camera): The camera object containing the values to be inserted into the database.

        Returns:
            Camera: The newly created camera record, with all fields populated.
        """
        self.db.add(camera)
        self.db.commit()
        self.db.refresh(camera)
        return camera

    def get_url_camera(self, key_camera: str):
        """
        Retrieve the camera record by its unique key.

        Parameters:
            key_camera (str): The unique key of the camera.

        Returns:
            Camera: The camera record if found, otherwise None.
        """

        camera = self.db.query(Camera).filter(Camera.key_camera == key_camera).first()
        return camera
    
    def delete_camera(self, key_camera: str):
        """
        Delete a camera record by its unique key.

        Parameters:
            key_camera (str): The unique key of the camera to be deleted.

        Returns:
            Camera: The deleted camera record, with all fields populated.
        """
        
        camera = self.db.query(Camera).filter(Camera.key_camera == key_camera).first()
        self.db.delete(camera)
        self.db.commit()
        return camera

    def update_camera(self, camera: Camera):
        
        """
        Update a camera record.

        Parameters:
            camera (Camera): The camera object containing the values to be updated in the database.

        Returns:
            Camera: The updated camera record, with all fields populated.
        """
        self.db.merge(camera)
        self.db.commit()
        return camera
    
    