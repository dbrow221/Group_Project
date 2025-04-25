from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(100), unique=True, nullable=False)

    # Assuming a customer can have many orders and recipes (if that's relevant)
    orders = relationship("Order", back_populates="customer")
    recipes = relationship("Recipe", back_populates="customer")  # Adjust as needed
