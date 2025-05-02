from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
from sqlalchemy.sql import func
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    comments = Column(String(100), nullable=False)
    sandwich_name = Column(String(100), ForeignKey("sandwiches.sandwich_name"), nullable=False)
    date = Column(DATETIME, nullable=False, server_default=func.now())

    sandwich = relationship(
        "Sandwich",
        back_populates="reviews",
        lazy="selectin",
        remote_side="Sandwich.sandwich_name"  # ✅ Remote side without primaryjoin
    )
