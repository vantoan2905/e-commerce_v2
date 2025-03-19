import os
import datetime
from dotenv import load_dotenv
from faker import Faker
import pandas as pd
import hashlib

from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime,
    ForeignKey, Text, Table
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

load_dotenv()
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


user_camera_table = Table(
    'user_camera',
    Base.metadata,
    Column('user_name', String(50), ForeignKey('users.username'), primary_key=True),
    Column('key_camera', String(255), ForeignKey('cameras.key_camera'), primary_key=True),
    Column('created_at', DateTime, default=datetime.datetime.utcnow)
)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(50), nullable=True)
    role = Column(String(50), default="user")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    reviews = relationship("EventReview", back_populates="user")
    cameras = relationship("Camera", secondary=user_camera_table, back_populates="users")


class Camera(Base):
    __tablename__ = "cameras"
    id = Column(Integer, primary_key=True, index=True)
    camera_name = Column(String(255), nullable=False)
    key_camera = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    camera_url = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    users = relationship("User", secondary=user_camera_table, back_populates="cameras")
    events = relationship("Event", back_populates="camera")


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    key_camera = Column(String(255), ForeignKey("cameras.key_camera"), nullable=False)
    event_type = Column(String(50), nullable=False)
    event_time = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="new")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    camera = relationship("Camera", back_populates="events")
    reviews = relationship("EventReview", back_populates="event")


class EventReview(Base):
    __tablename__ = "event_reviews"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    review = Column(Text, nullable=True)
    rating = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    event = relationship("Event", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


# ---------------------------------------------------------
# Seed data
# ---------------------------------------------------------
def seed_data():
    fake = Faker()
    session = SessionLocal()

    # ------------------- Seed Users -----------------------
    users = []
    default_password = []
    for _ in range(10):
        password = fake.password()
        user = User(
            email=fake.unique.email(),
            username=fake.user_name(),
            password=hashlib.sha256(password.encode()).hexdigest(),
            name=fake.name(),
            phone_number=fake.phone_number(),
            role=fake.random_element(elements=("user", "admin")),
        )
        users.append(user)
        session.add(user)
        default_password.append(password)
    session.commit() 
    data_user = pd.DataFrame({
        "email": [user.email for user in users],
        "username": [user.username for user in users],
        "name": [user.name for user in users],
        "phone_number": [user.phone_number for user in users],
        "role": [user.role for user in users],
        "password": default_password
    })
    data_user.to_csv("users.csv", index=False)
    
    cameras = []
    for _ in range(5):
        camera = Camera(
            camera_name=fake.street_name(),
            camera_url=fake.image_url(),
            key_camera=fake.password(),  
            password=fake.password(),
            location=fake.address(),
            status=fake.random_element(elements=("active", "inactive")),
        )
        cameras.append(camera)
        session.add(camera)
    session.commit()  
    
    data_camera = pd.DataFrame({
        "camera_name": [camera.camera_name for camera in cameras],
        "camera_url": [camera.camera_url for camera in cameras],
        "key_camera": [camera.key_camera for camera in cameras],
        "password": [camera.password for camera in cameras],
        "location": [camera.location for camera in cameras],
        "status": [camera.status for camera in cameras]
    })
    data_camera.to_csv("cameras.csv", index=False)

    # ------------------- Seed UserCamera ------------------
    for user in users:
        random_cams = fake.random_elements(elements=cameras, length=3, unique=False)
        for cam in random_cams:
            ins = user_camera_table.insert().values(
                user_name=user.username,
                key_camera=cam.key_camera,
                created_at=datetime.datetime.utcnow()
            )
            session.execute(ins)
    session.commit() 

    # ------------------- Seed Events ----------------------
    events = []
    for cam in cameras:
        for _ in range(fake.random_int(min=3, max=5)):
            event = Event(
                key_camera=cam.key_camera,  # Sử dụng key_camera của Camera
                event_type=fake.random_element(elements=("motion", "offline", "tamper")),
                status=fake.random_element(elements=("new", "viewed", "resolved")),
            )
            events.append(event)
            session.add(event)
    session.commit()  

    data_event = pd.DataFrame({
        "event_id": [event.id for event in events],
        "key_camera": [event.key_camera for event in events],
        "event_type": [event.event_type for event in events],
        "status": [event.status for event in events],
        "created_at": [event.created_at for event in events]
    })
    data_event.to_csv("events.csv", index=False)

    # ------------------- Seed EventReviews ----------------
    for ev in events:
        number_of_reviews = fake.random_int(min=0, max=2)
        for _ in range(number_of_reviews):
            random_user = fake.random_element(elements=users)
            review = EventReview(
                event_id=ev.id,
                user_id=random_user.id,
                review=fake.sentence(nb_words=10),
                rating=fake.random_int(min=1, max=5),
            )
            session.add(review)
    session.commit()
    session.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_data()
    print("Database created.")
