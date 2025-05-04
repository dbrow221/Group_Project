from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Sandwich(Base):
    __tablename__ = "sandwiches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_name = Column(String(100), nullable=False)  # Added nullable=False
    price = Column(DECIMAL(4, 2), nullable=False, server_default="0.0")
    description = Column(String(1000), nullable=True)

    # One-to-one relationship with Recipe
    recipes = relationship(
        "Recipe",
        back_populates="sandwich",
        uselist=False  # Ensures a one-to-one relationship
    )

    # Relationship with OrderDetail
    order_detail = relationship(
        "OrderDetail",
        back_populates="sandwiches"
    )

    # Relationship with Review
    review = relationship(
        "Review",
        back_populates="sandwiches"
    )