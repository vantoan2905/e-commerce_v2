from sqlalchemy.orm import Session
from src.database.models.product import Product
from src.schemas.product import ProductCreate, ProductUpdate
from typing import List, Optional
from sqlalchemy import and_


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: ProductCreate):
        db_product = Product(**product.dict())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get_all_products(self):
        return self.db.query(Product).all()

    def get_product_by(self, product: Product) -> List[Product]:
        conditions = []
        for var, value in product.dict().items():
            if value == "string" or var in ["created_at", "updated_at"]:
                continue
            conditions.append(getattr(Product, var) == value)

        if not conditions:
            return self.db.query(Product).all()

        return self.db.query(Product).filter(and_(*conditions)).all()
    
    def update_product(self, product_id: int, product: ProductUpdate):
        """
        Update an existing product in the database.

        Parameters:
            product_id (int): The id of the product to be updated.
            product (ProductUpdate): The updated product data.

        Returns:
            Product: The updated product, or None if no product with the given id exists.
        """
        db_product = self.db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            return None
        for var, value in product.dict().items():
            setattr(db_product, var, value)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    def delete_product(self, product_id: int):
        db_product = self.db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            return None
        self.db.delete(db_product)
        self.db.commit()