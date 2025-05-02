from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Sandwich(Base):
    __tablename__ = "sandwiches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_name = Column(String(100), unique=True, nullable=True)
    price = Column(DECIMAL(4, 2), nullable=False, server_default='0.0')
    description = Column(String(1000), nullable=True)

    recipes = relationship(
        "Recipe",
        primaryjoin="Sandwich.id == Recipe.sandwich_id",
        back_populates="sandwich"
    )

    order_details = relationship(
        "OrderDetail",
        primaryjoin="Sandwich.id == OrderDetail.sandwich_id",
        back_populates="sandwich"
    )

    reviews = relationship(
        "Review",
        primaryjoin="Sandwich.sandwich_name == foreign(Review.sandwich_name)",
        back_populates="sandwich"
    )
