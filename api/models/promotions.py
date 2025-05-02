from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    code = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    discount = Column(Float, nullable=False)

    orders = relationship(
        "Order",
        back_populates="promotion",
        lazy="selectin",
        primaryjoin="Promotion.code == foreign(Order.promotion_code)"
    )
