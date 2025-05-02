from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"))
    resource_id = Column(Integer, ForeignKey("resources.id"))
    amount = Column(Integer, index=True, nullable=False, server_default='0.0')

    sandwich = relationship(
        "Sandwich",
        primaryjoin="Sandwich.id == foreign(Recipe.sandwich_id)",
        back_populates="recipes"
    )

    resource = relationship(
        "Resource",
        primaryjoin="Resource.id == foreign(Recipe.resource_id)",
        back_populates="recipes"
    )
