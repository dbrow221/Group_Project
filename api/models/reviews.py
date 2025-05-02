from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(100), nullable=False)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"), nullable=False)
    date = Column(DATETIME, nullable=False)

    sandwich = relationship(
        "Sandwich",
        back_populates="reviews",
        lazy="selectin",
        primaryjoin="Review.sandwich_id == foreign(Sandwich.id)",
        remote_side="Sandwich.id"  # ✅ Add remote_side here
    )
