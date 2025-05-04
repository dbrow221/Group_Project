from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship, foreign
from datetime import datetime
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    class Resource(Base):
        __tablename__ = "resources"

        id = Column(Integer, primary_key=True, index=True, autoincrement=True)
        item = Column(String(100), unique=True, nullable=False)
        amount = Column(DECIMAL(10, 2), index=True, nullable=False, server_default="0.0")

        # Many-to-many relationship with recipes
        recipe_resources = relationship("RecipeResource", back_populates="resource")

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


