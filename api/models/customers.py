from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, foreign
from ..dependencies.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(100), unique=True, nullable=False)
    address = Column(String(255), nullable=False)

    orders = relationship(
        "Order",
        primaryjoin="Customer.id == foreign(Order.customer_id)",
        back_populates="customer"  # ✅ FIXED
    )

