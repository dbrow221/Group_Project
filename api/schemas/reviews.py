from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReviewBase(BaseModel):
    sandwich_name: str
    id: int


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    description: Optional[str] = None
    date: Optional[datetime] = None


class Review(ReviewBase):
    id: int

    class ConfigDict:
        from_attributes = True