from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.service.product_service.product_service import ProductService
from src.schemas.product_schema import ProductCreate, ProductUpdate, ProductSearch


product_router = APIRouter()

product_service = ProductService(db=get_db())


@product_router.get("/all/", response_model=list[ProductCreate])
async def get_all_products(db: Session = Depends(get_db)):
    try:
        sevice = ProductService(db)
        products = sevice.get_all_products()
        return products
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@product_router.post("/new_product/", response_model=ProductCreate)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        sevice = ProductService(db)
        db_product = sevice.create_product(product)
        return db_product
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@product_router.get("/{product_id}/", response_model=ProductCreate)
async def get_product_by_id(product : ProductSearch, db: Session = Depends(get_db)):
    try:
        sevice = ProductService(db)
        product = sevice.get_product_by(product)
        return product
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@product_router.put("/{product_id}/", response_model=ProductCreate)
async def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    try:
        sevice = ProductService(db)
        db_product = sevice.update_product(product_id, product)
        return db_product
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")