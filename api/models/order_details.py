from sqlalchemy import Column, ForeignKey, Integer, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"), nullable=False)
    amount = Column(Integer, index=True, nullable=False)

    # Relationships
    order = relationship(
        "Order",  # String-based reference
        back_populates="order_details"
    )

    sandwich = relationship(
        "Sandwich",  # String-based reference
        back_populates="order_details"
    )