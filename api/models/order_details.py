from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
from ..dependencies.database import Base

class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    amount = Column(Integer, index=True, nullable=False)

    order = relationship(
        "Order",
        primaryjoin="Order.id == foreign(OrderDetail.order_id)",
        back_populates="order_details"
    )

    sandwich = relationship(
        "Sandwich",
        primaryjoin="Sandwich.id == foreign(OrderDetail.sandwich_id)",
        back_populates="order_details"
    )
