from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReviewBase(BaseModel):
    sandwich_name: str
    comments: str


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    date: Optional[datetime] = None
    comments: Optional[str] = None
    sandwich_name: Optional[str] = None

class Review(ReviewBase):
    id: int

    class ConfigDict:
        from_attributes = True