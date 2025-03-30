from sqlalchemy.sql import func
from src.database.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Float, Numeric

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String(255), nullable=False)
    masterCategory = Column(String(255), nullable=False)
    subCategory = Column(String(255), nullable=False)
    articleType = Column(String(255), nullable=False)
    baseColour = Column(String(255), nullable=False)
    season = Column(String(255), nullable=False)
    year = Column(String(255), nullable=False)
    usage = Column(String(255), nullable=False)
    imageLink = Column(String(255), nullable=False)
    productLink = Column(String(255), nullable=False)
    productDisplayName = Column(String(255), nullable=False)
    price = Column(String(255), nullable=False)
    currency = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    reviews = Column(Integer)

    product_views = relationship("ProductView", back_populates="product")
    favorite_products = relationship("FavoriteProduct", back_populates="product")
    transaction_details = relationship("TransactionDetail", back_populates="product")

    def __repr__(self):
        return (f"<Product(name={self.productDisplayName}, price={self.price}, "
                f"currency={self.currency}, reviews={self.reviews})>")
