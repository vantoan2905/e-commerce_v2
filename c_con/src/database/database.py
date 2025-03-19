from dependencies.dependencies import Config


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



config = Config()
db_user = config.get_user()
db_password = config.get_password()
db_host = config.get_host()
db_port = config.get_port()
db_name = config.get_name()

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# db = SessionLocal()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# class DatabaseController:
#     """
#     Controller for managing database sessions and initializing data models.
#     """

#     def __init__(self) -> None:
#         """
#         Initialize the DatabaseController.

#         Loads database configuration, establishes a session via SessionLocal,
#         and instantiates the data models.
#         """
#         self.db_session = SessionLocal()

#         self.user_model = User()
#         self.camera_detail_model = CameraDetail()
#         self.user_camera_model = ReUserCamera()

#     def get_user_model(self) -> User:
#         """
#         Get the user model instance.

#         Returns:
#             User: The user model initialized with the database session.
#         """
#         return self.user_model

#     def get_camera_detail_model(self) -> CameraDetail:
#         """
#         Get the camera detail model instance.

#         Returns:
#             CameraDetail: The camera detail model initialized with the database session.
#         """
#         return self.camera_detail_model

#     def get_user_camera_model(self) -> ReUserCamera:
#         """
#         Get the user-camera model instance.

#         Returns:
#             ReUserCamera: The user-camera model initialized with the database session.
#         """
#         return self.user_camera_model

#     def close(self):
#         """
#         Close the database session.
#         """
#         self.db_session.close()
