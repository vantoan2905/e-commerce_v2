import os
import datetime
import random
import hashlib
from dotenv import load_dotenv
from faker import Faker
import pandas as pd
import tqdm

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
    product_interactions = relationship("UserProductInteraction", back_populates="user")


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


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String(255), nullable=False)
    masterCategory = Column(String(255), nullable=False)
    subCategory = Column(String(255), nullable=False)
    articleType = Column(String(255), nullable=False)
    baseColour = Column(String(255), nullable=False)
    season = Column(String(255), nullable=False)
    year = Column(String(255), nullable=False)
    usage = Column(String(255), nullable=False)
    imageLink = Column(String(255), nullable=False)
    productLink = Column(String(255), nullable=False)
    productDisplayName = Column(String(255), nullable=False)
    price = Column(String(255), nullable=False)
    currency = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    reviews = Column(Integer)

    product_interactions = relationship("UserProductInteraction", back_populates="product")


class UserProductInteraction(Base):
    __tablename__ = "user_product_interactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    interaction_type = Column(String(50), nullable=False)  
    rating = Column(Integer, nullable=True)  
    review = Column(Text, nullable=True)     
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="product_interactions")
    product = relationship("Product", back_populates="product_interactions")


def seed_data():
    fake = Faker()
    session = SessionLocal()

    # ------------------- Seed Products -----------------------
    path  = r"D:\project\ecommence\e_server\c_con\src\df_product.csv"
    df_products = pd.read_csv(path)

    products = []
    for _, row in tqdm.tqdm(df_products.iterrows(), total=len(df_products), desc="Seeding Products"):
        product = Product(
            id=row["id"],
            gender=row['gender'] if row['gender'] is not None else None,
            masterCategory=row['masterCategory'] if row['masterCategory'] is not None else None,
            subCategory=row['subCategory'] if row['subCategory'] is not None else None,
            articleType=row['articleType'] if row['articleType'] is not None else None,
            baseColour=row['baseColour'] if row['baseColour'] is not None else None,
            season=row['season'] if row['season'] is not None else None,
            year=str(row['year']) if row['year'] is not None else None,
            usage=row['usage'] if row['usage'] is not None else None,
            imageLink=row['link'] if row['link'] is not None else None,
            productLink=row['link'] if row['link'] is not None else None,
            productDisplayName=row['productDisplayName'] if row['productDisplayName'] is not None else None,
            price=f"{fake.random_int(min=10, max=100)}.99",
            currency="USD",
            reviews=fake.random_int(min=0, max=5)
        )
        products.append(product)
        session.add(product)
    session.commit()

    data_product = pd.DataFrame({
        "gender": [p.gender for p in products],
        "masterCategory": [p.masterCategory for p in products],
        "subCategory": [p.subCategory for p in products],
        "articleType": [p.articleType for p in products],
        "baseColour": [p.baseColour for p in products],
        "season": [p.season for p in products],
        "year": [p.year for p in products],
        "usage": [p.usage for p in products],
        "imageLink": [p.imageLink for p in products],
        "productLink": [p.productLink for p in products],
        "productDisplayName": [p.productDisplayName for p in products],
        "price": [p.price for p in products],
        "currency": [p.currency for p in products],
        "reviews": [p.reviews for p in products],
    })
    data_product.to_csv("products.csv", index=False)

    # ------------------- Seed Users -----------------------
    users = []
    default_password = []
    for _ in tqdm.tqdm(range(10), desc="Seeding Users"):
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

    # ------------------- Seed Cameras -----------------------
    cameras = []
    for _ in tqdm.tqdm(range(5), desc="Seeding Cameras"):
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
    for user in tqdm.tqdm(users, desc="Seeding User-Camera Relationships"):
        random_cams = fake.random_elements(elements=cameras, length=3, unique=True)
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
    for cam in tqdm.tqdm(cameras, desc="Seeding Events per Camera"):
        for _ in range(fake.random_int(min=3, max=5)):
            event = Event(
                key_camera=cam.key_camera,
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
    for ev in tqdm.tqdm(events, desc="Seeding EventReviews"):
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

    # ------------------- Seed UserProductInteractions ----------------
    for user in tqdm.tqdm(users, desc="Seeding User-Product Interactions"):
        num_interactions = fake.random_int(min=1, max=30)
        for _ in range(num_interactions):
            product = random.choice(products)
            interaction_type = fake.random_element(elements=("view", "add_to_cart", "purchase", "review"))
            rating = None
            review_text = None
            if interaction_type == "review":
                rating = fake.random_int(min=1, max=5)
                review_text = fake.sentence(nb_words=10)
            interaction = UserProductInteraction(
                user_id=user.id,
                product_id=product.id,
                interaction_type=interaction_type,
                rating=rating,
                review=review_text,
                created_at=datetime.datetime.utcnow()
            )
            session.add(interaction)
    session.commit()

    session.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_data()
    print("Database created.")
