from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from .resources import Resource
from .sandwiches import Sandwich


class RecipeBase(BaseModel):
    amount: int


class RecipeCreate(RecipeBase):
    sandwich_id: int
    resource_id: int
    ingredients: Optional[List[Resource]]

class RecipeUpdate(BaseModel):
    sandwich_id: Optional[int] = None
    resource_id: Optional[int] = None
    amount: Optional[int] = None

class Recipe(RecipeBase):
    id: int
    sandwich: Sandwich = None
    resource: Resource = None

    class ConfigDict:
        from_attributes = True