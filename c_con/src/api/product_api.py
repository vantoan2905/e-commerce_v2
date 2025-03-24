from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.service.product_service.product_service import ProductService
from src.database.database import get_db
from src.schemas.product_schema import ProductCreate, ProductUpdate, ProductSearch
from typing import Dict
product_router = APIRouter(prefix="/api/products")

@product_router.get("/")
async def get_all_products(db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.get_all_products()

@product_router.post("/")
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.create_product(product)

@product_router.post("/get_product")
async def get_product_by(product: ProductCreate, db: Session = Depends(get_db)):

    product_service = ProductService(db)
    return product_service.get_product_by(product)

@product_router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.delete_product(product_id)

@product_router.put("/{product_id}")
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    product_service = ProductService(db)
    return product_service.update_product(product_id, product)
