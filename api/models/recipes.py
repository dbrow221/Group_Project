from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, ForeignKey("sandwiches.id"), primary_key=True)  # Corrected ForeignKey declaration
    name = Column(String(100), unique=True, nullable=False)
    ingredients = Column(String(1000), nullable=False)

    # Many-to-many relationship with resources through RecipeResource
    recipe_resources = relationship("RecipeResource", back_populates="recipes")

    # One-to-one relationship with Sandwich
    sandwich = relationship(
        "Sandwich",
        back_populates="recipes"
    )


class RecipeResource(Base):
    __tablename__ = "recipe_resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    quantity_needed = Column(DECIMAL(10, 2), nullable=False)  # Quantity needed for the recipe

    # Relationships to Recipe and Resource
    recipe = relationship("Recipe", back_populates="recipe_resources")
    resource = relationship("Resource", back_populates="recipe_resources")