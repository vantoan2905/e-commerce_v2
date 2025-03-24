from fastapi import APIRouter, WebSocket, HTTPException, Depends
import cv2
from sqlalchemy.orm import Session

from src.service.user_product_Interaction_service.user_product_Interaction_service import UserProductInteraction
from src.schemas.user_product_Interaction_schema import UserProductInteractionCreate
from src.database.database import get_db

# Tạo router từ APIRouter
user_product_router = APIRouter(prefix="/api/user_product_interaction")

@user_product_router.post("/create_user_product_interaction")
async def create_user_product_interaction(user_product_interaction: UserProductInteractionCreate, db: Session = Depends(get_db)):
    service = UserProductInteraction(db)
    return service.create_user_product_interaction(user_product_interaction)

@user_product_router.get("/get_user_product_interaction")
async def get_user_product_interaction(user_id: int, product_id: int, db: Session = Depends(get_db)):
    service = UserProductInteraction(db)
    return service.get_user_product_interaction(user_id, product_id)

@user_product_router.put("/update_user_product_interaction")
async def update_user_product_interaction(user_product_interaction: UserProductInteractionCreate, db: Session = Depends(get_db)):
    service = UserProductInteraction(db)
    return service.update_user_product_interaction(user_product_interaction)

@user_product_router.delete("/delete_user_product_interaction")
async def delete_user_product_interaction(user_product_interaction: UserProductInteractionCreate, db: Session = Depends(get_db)):
    service = UserProductInteraction(db)
    return service.delete_user_product_interaction(user_product_interaction)
