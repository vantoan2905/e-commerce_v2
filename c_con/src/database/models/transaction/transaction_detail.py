from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from src.database.base import Base
from sqlalchemy.orm import relationship

class TransactionDetail(Base):
    __tablename__ = "transaction_details"

    detail_id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.transaction_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(DECIMAL(10, 2))

    transaction = relationship("Transaction", back_populates="transaction_details")
    product = relationship("Product", back_populates="transaction_details")

    def __repr__(self):
        return f"<TransactionDetail(id={self.detail_id}, product_id={self.product_id})>"
