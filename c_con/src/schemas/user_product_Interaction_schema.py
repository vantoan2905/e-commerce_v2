from pydantic import BaseModel, EmailStr, validator
from datetime import datetime


class UserProductInteractionCreate(BaseModel):
    user_id : int
    product_id : int
    interaction_type : str
    rating : int
    review : str     
    created_at : datetime

class UserProductInteractionUpdate(BaseModel):
    user_id : int
    product_id : int
    interaction_type : str
    rating : int
    review : str
    created_at : datetime

class UserProductInteraction(UserProductInteractionCreate):
    id : int

