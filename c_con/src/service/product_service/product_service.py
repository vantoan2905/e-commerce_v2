from sqlalchemy.orm import Session
from src.database.models.product.product import Product
from src.schemas.product_schema import ProductCreate, ProductUpdate
from typing import List, Optional
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
import torch
from torchvision import transforms
from PIL import Image
import dotenv
from dotenv import load_dotenv
import os
import datetime


class ProductService:
    def __init__(self, db: Session):
        load_dotenv()
        
        # Database session
        self._db = db
        # Load model
        self._gender_model_path = os.getenv("GENDER_MODEL_PATH")
        self._master_category_model_path = os.getenv("MASTER_CATEGORY_MODEL_PATH")
        self._sub_category_model_path = os.getenv("SUB_CATEGORY_MODEL_PATH")
        self._article_type_model_path = os.getenv("ARTICLE_TYPE_MODEL_PATH")
        self._base_colour_model_path = os.getenv("BASE_COLOUR_MODEL_PATH")
        self._season_model_path = os.getenv("SEASON_MODEL_PATH")
        self._usage_model_path = os.getenv("USAGE_MODEL_PATH")
        self._currency_model_path = os.getenv("CURRENCY_MODEL_PATH")
        

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

    def get_all_products(self) -> List[Product]:
        """
        Retrieve all products from the database.

        Returns:
            List[Product]: A list of all product records in the database.
        """
        try:
            products = self.db.query(Product).all()
            print(products[1])
            return products
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return []

    def get_product_by(self, product: Product) -> List[Product]:
        """
        Retrieve products from the database that match the specified criteria.

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

        
        """
        db_product = self.db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            return None
        self.db.delete(db_product)
        self.db.commit()
        
        
    def get_product_by_image(self, image_path: str) -> List[Product]:
        """
        Retrieve products from the database based on image predictions.

        """
        try:
            
            
            # Load models
            gender_model = torch.load(self._gender_model_path)
            master_category_model = torch.load(self._master_category_model_path)
            sub_category_model = torch.load(self._sub_category_model_path)
            article_type_model = torch.load(self._article_type_model_path)
            base_colour_model = torch.load(self._base_colour_model_path)
            season_model = torch.load(self._season_model_path)
            usage_model = torch.load(self._usage_model_path)
            currency_model = torch.load(self._currency_model_path)

            models = [
                gender_model, master_category_model, sub_category_model, 
                article_type_model, base_colour_model, season_model, 
                usage_model, currency_model
            ]
            for model in models:
                model.eval()

            transform_pipeline = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225]),
            ])


            image = Image.open(image_path).convert("RGB")
            image_tensor = transform_pipeline(image).unsqueeze(0)  

            gender_pred = gender_model(image_tensor).argmax(dim=1).item()
            master_category_pred = master_category_model(image_tensor).argmax(dim=1).item()
            sub_category_pred = sub_category_model(image_tensor).argmax(dim=1).item()
            article_type_pred = article_type_model(image_tensor).argmax(dim=1).item()
            base_colour_pred = base_colour_model(image_tensor).argmax(dim=1).item()
            season_pred = season_model(image_tensor).argmax(dim=1).item()
            usage_pred = usage_model(image_tensor).argmax(dim=1).item()
            currency_pred = currency_model(image_tensor).argmax(dim=1).item()

            criteria = {
                "gender": gender_pred,
                "master_category": master_category_pred,
                "sub_category": sub_category_pred,
                "article_type": article_type_pred,
                "base_colour": base_colour_pred,
                "season": season_pred,
                "usage": usage_pred,
                "currency": currency_pred,
            }

            from src.schemas.product_schema import ProductCreate
            criteria_obj = ProductCreate(**criteria)

            products = self.get_product_by(criteria_obj)
            return products

        except Exception as e:
            print(f"Error in get_product_by_image: {e}")
            return []

    
    
    def add_product_by_image(self, image_path: str) -> bool:
        """
        Add a product to the database based on image predictions.
        """
        image_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        # rebase64 the image
        img = Image.open(image_path).convert("RGB")

        image_tensor = image_transform(img)

        image_tensor = image_tensor.unsqueeze(0)

        gender_model = torch.load(self._gender_model_path)
        master_category_model = torch.load(self._master_category_model_path)
        sub_category_model = torch.load(self._sub_category_model_path)
        article_type_model = torch.load(self._article_type_model_path)
        base_colour_model = torch.load(self._base_colour_model_path)
        season_model = torch.load(self._season_model_path)
        usage_model = torch.load(self._usage_model_path)
        currency_model = torch.load(self._currency_model_path)

        gender_model.eval()
        master_category_model.eval()
        sub_category_model.eval()
        article_type_model.eval()
        base_colour_model.eval()
        season_model.eval()
        usage_model.eval()
        currency_model.eval()

        with torch.no_grad():
            gender_output = gender_model(image_tensor)
            master_category_output = master_category_model(image_tensor)
            sub_category_output = sub_category_model(image_tensor)
            article_type_output = article_type_model(image_tensor)
            base_colour_output = base_colour_model(image_tensor)
            season_output = season_model(image_tensor)
            usage_output = usage_model(image_tensor)
        
        predicted_gender = torch.argmax(gender_output, dim=1).item()
        predicted_master_category = torch.argmax(master_category_output, dim=1).item()
        predicted_sub_category = torch.argmax(sub_category_output, dim=1).item()
        predicted_article_type = torch.argmax(article_type_output, dim=1).item()
        predicted_base_colour = torch.argmax(base_colour_output, dim=1).item()
        predicted_season = torch.argmax(season_output, dim=1).item()
        predicted_usage = torch.argmax(usage_output, dim=1).item()

        currency = "USD"
        price = 0.0
        reviews = "No reviews yet"
        create_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        product_instance = self._db.query(Product).filter(
            Product.gender == predicted_gender,
            Product.masterCategory== predicted_master_category,
            Product.subCategory == predicted_sub_category,
            Product.articleType == predicted_article_type,
            Product.baseColour == predicted_base_colour,
            Product.season == predicted_season,
            Product.usage == predicted_usage
        ).first()

        if not product_instance:
            print("No matching product found for the predicted image attributes.")
            return False

        product_instance.currency = currency
        product_instance.price = price
        product_instance.reviews = reviews
        product_instance.updated_at = updated_at
        product_instance.created_at = create_at

        try:
            self._db.commit()
            self._db.refresh(product_instance)
            return True
        except Exception as e:
            self._db.rollback()
            print(f"Error updating product: {e}")
            return False