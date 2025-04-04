from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.database.database import get_db
from src.service.product_service.product_service import ProductService
from src.schemas.product_schema import ProductCreate, ProductUpdate, ProductSearch, ProductResponse
import datetime
import dotenv
from dotenv import load_dotenv
import os
import base64
product_router = APIRouter(prefix="/api/products", tags=["api/products"])

def get_product_service(db: Session = Depends(get_db)):
    return ProductService(db)

@product_router.get("/health_check")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}
# -----------------------------------------------------
# User methods
# -----------------------------------------------------
@product_router.get("/all/", response_model=List[ProductResponse])
async def get_all_products(service: ProductService = Depends(get_product_service)):
    """Retrieve all products."""
    try:
        products = service.get_all_products()
        return products
    except Exception as e:
        # Consider using a logging library instead of print
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@product_router.get("/product_by/", response_model=ProductResponse)
async def get_product_by(search_params: ProductSearch, service: ProductService = Depends(get_product_service)):
    """Retrieve a product based on search criteria."""
    try:
        product = service.get_product_by(search_params)
        return product
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@product_router.get("/product_by_image/")
async def search_product_by_image(product_image: str, service: ProductService = Depends(get_product_service)):
    """Retrieve products by image list."""
    try:
        base64_image = product_image.split(",")[1] if "," in product_image else product_image
        # Decode the base64 image string
        decoded_image = base64.b64decode(base64_image)
        # Save the image to a temporary file (optional, depending on your use case)
        load_dotenv()
        static_dir = os.getenv("STATIC_DIR")
        with open(f"{static_dir}/temp_image.jpg", "wb") as image_file:
            image_file.write(decoded_image)
        path = f"{static_dir}/temp_image.jpg"
        # Ensure you pass the product_image to the service if needed
        product = service.get_product_by_image(path)
        # Clean up the temporary file if necessary
        os.remove(path)
        return product
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# -----------------------------------------------------
#  admin method
# -----------------------------------------------------
@product_router.post("/new_product/", response_model=ProductResponse)
async def create_product(product: ProductCreate, service: ProductService = Depends(get_product_service)):
    """Create a new product."""
    try:
        db_product = service.create_product(product)
        return db_product
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@product_router.put("/{product_id}/", response_model=ProductResponse)
async def update_product(product_id: int, product: ProductUpdate, service: ProductService = Depends(get_product_service)):
    """Update a product by ID."""
    try:
        db_product = service.update_product(product_id, product)
        return db_product
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@product_router.delete("/{product_id}/")
async def delete_product(product_id: int, service: ProductService = Depends(get_product_service)):
    """Delete a product by ID."""
    try:
        service.delete_product(product_id)
        return {"message": "Product deleted successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
@product_router.put("/update_product_by_image/")
async def add_product_by_image(product_image: str, product: ProductUpdate, service: ProductService = Depends(get_product_service)):
    """Update a product by image."""
    try:
        base64_image = product_image.split(",")[1] if "," in product_image else product_image
        # Decode the base64 image string
        decoded_image = base64.b64decode(base64_image)
        # Save the image to a temporary file (optional, depending on your use case)
        load_dotenv()
        static_dir = os.getenv("STATIC_DIR")
        with open(f"{static_dir}/temp_image.jpg", "wb") as image_file:
            image_file.write(decoded_image)
        path = f"{static_dir}/temp_image.jpg"
        
        db_product = service.add_product_by_image(path)
        return db_product
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")