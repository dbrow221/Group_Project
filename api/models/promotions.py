from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    code = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    discount = Column(Float, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    orders = relationship("Order", back_populates="promotion", lazy="selectin")
