from pydantic import BaseModel, EmailStr, validator
from datetime import datetime


class ProductBase(BaseModel):
    gender : str
    masterCategory : str
    subCategory : str
    articleType : str
    baseColour : str
    season : str
    year : str
    usage : str
    imageLink : str
    productLink : str
    productDisplayName : str
    price : str
    currency : str
    created_at : datetime
    updated_at : datetime
    reviews : str

class ProductCreate(ProductBase):
    gender : str
    masterCategory : str
    subCategory : str
    articleType : str
    baseColour : str
    season : str
    year : str
    usage : str
    imageLink : str
    productLink : str
    productDisplayName : str
    price : str
    currency : str
    created_at : datetime
    updated_at : datetime
    reviews : str


class ProductUpdate(ProductBase):
    gender : str
    masterCategory : str
    subCategory : str
    articleType : str
    baseColour : str
    season : str
    year : str
    usage : str
    imageLink : str
    productLink : str
    productDisplayName : str
    price : str
    currency : str
    created_at : datetime
    updated_at : datetime
    reviews : str

class ProductSearch(ProductBase):
    gender : str
    masterCategory : str
    subCategory : str
    articleType : str
    baseColour : str
    season : str
    year : str
    usage : str
    imageLink : str
    productLink : str
    productDisplayName : str
    price : str
    currency : str
    reviews : str
    
    
class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True  # Enable ORM mode for SQLAlchemy compatibility