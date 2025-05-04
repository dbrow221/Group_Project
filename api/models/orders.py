from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from ..dependencies.database import Base
from sqlalchemy.sql import func

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    order_date = Column(DATETIME, nullable=False, server_default=func.now())
    description = Column(String(300))
    order_status = Column(String(100))
    order_type = Column(String(100))
    total_price = Column(DECIMAL(10, 2))  # Add a total_price field
    promotion_code = Column(Integer, ForeignKey('promotions.code'))

    order_detail = relationship("OrderDetail", back_populates="orders")
    customer = relationship("Customer",primaryjoin='Customer.id==Order.customer_id', back_populates="orders")

    promotion = relationship("Promotion", primaryjoin="Promotion.code==Order.promotion_code", back_populates="orders")