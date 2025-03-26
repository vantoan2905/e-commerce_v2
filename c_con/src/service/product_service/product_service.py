from sqlalchemy.orm import Session
from e_server.c_con.src.database.models.product.product_model import Product
from src.schemas.product_schema import ProductCreate, ProductUpdate
from typing import List, Optional
from sqlalchemy import and_


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product: ProductCreate):
        """
        Create a new product record.

        Parameters:
            product (ProductCreate): The product to be inserted into the database.

        Returns:
            Product: The newly created product record, with all fields populated.
        """
        db_product = Product(**product.dict())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get_all_products(self):
        """
        Retrieve all products from the database.

        Returns:
            List[Product]: A list of all product records in the database.
        """
        return self.db.query(Product).all()

    def get_product_by(self, product: Product) -> List[Product]:
        """
        Retrieve products from the database that match the specified criteria.

        Parameters:
            product (Product): A product instance with attributes to filter the products in the database.

        Returns:
            List[Product]: A list of products that match the specified criteria. If no criteria are provided,
                        all products are returned.
        """

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
        """
        Delete a product from the database.

        Parameters:
            product_id (int): The ID of the product to be deleted.

        Returns:
            Product: The deleted product, or None if no product with the given id exists.
        """
        db_product = self.db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            return None
        self.db.delete(db_product)
        self.db.commit()