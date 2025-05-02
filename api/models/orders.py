from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
from sqlalchemy.sql import func
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    order_date = Column(DATETIME, nullable=False, server_default=func.now())
    description = Column(String(300))
    order_status = Column(String(100))
    order_type = Column(String(100))

    promotion_code = Column(Integer, ForeignKey("promotions.code"))

    promotion = relationship(
        "Promotion",
        primaryjoin="Promotion.code == foreign(Order.promotion_code)",
        back_populates="orders"
    )

    customer = relationship(
        "Customer",
        primaryjoin="Customer.id == foreign(Order.customer_id)",
        back_populates="orders"
    )
    order_details = relationship("OrderDetail", back_populates="order")

