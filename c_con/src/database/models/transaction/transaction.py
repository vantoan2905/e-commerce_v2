from sqlalchemy import Column, Integer, String, DateTime, Enum, DECIMAL, ForeignKey
from sqlalchemy.sql import func
from src.database import Base
from sqlalchemy.orm import relationship

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    total_amount = Column(DECIMAL(10, 2))
    payment_method = Column(Enum("credit_card", "paypal", "bank_transfer", "cod", name="payment_method_enum"))
    payment_status = Column(Enum("pending", "completed", "failed", name="payment_status_enum"))
    transaction_time = Column(DateTime(timezone=True), server_default=func.now())
    shipping_address = Column(String(255))
    phone = Column(String(20))
    email = Column(String(100))

    user = relationship("User", back_populates="transactions")
    transaction_details = relationship("TransactionDetail", back_populates="transaction")

    def __repr__(self):
        return f"<Transaction(id={self.transaction_id}, total_amount={self.total_amount})>"
