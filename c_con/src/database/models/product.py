
from sqlalchemy import  Column, Integer, String, DateTime, Text
from datetime import datetime
from src.database.Base import Base
from sqlalchemy.orm import relationship
import datetime


class Product(Base):
    __tablename__ = "products"
    # default values 
    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String(255), nullable=False)
    masterCategory= Column(String(255), nullable=False)
    subCategory = Column(String(255), nullable=False)
    articleType = Column(String(255), nullable=False)
    baseColour = Column(String(255), nullable=False)
    season = Column(String(255), nullable=False)
    year = Column(String(255), nullable=False)
    usage = Column(String(255), nullable=False)
    imageLink = Column(String(255), nullable=False)
    productLink = Column(String(255), nullable=False)
    productDisplayName  = Column(String(255), nullable=False)
    #gender,masterCategory,subCategory,articleType,baseColour,season,year,usage,productDisplayName
    
    # user updated values
    price = Column(String(255), nullable=False)
    currency = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    reviews = Column(Integer, nullable=False)

    def __repr__(self):
        return f"Product(articleType = {self.articleType}, baseColour = {self.baseColour}, season = {self.season}, year = {self.year}, usage = {self.usage}, productDisplayName = {self.productDisplayName}), price = {self.price}, currency = {self.currency}, reviews = {self.reviews})"