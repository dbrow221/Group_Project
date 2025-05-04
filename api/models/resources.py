from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship, foreign
from ..dependencies.database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item = Column(String(100), unique=True, nullable=False)
    amount = Column(DECIMAL(10, 2), index=True, nullable=False, server_default="0.0")

    # Many-to-many relationship with recipes through RecipeResource
    recipe_resources = relationship("RecipeResource", back_populates="resource")