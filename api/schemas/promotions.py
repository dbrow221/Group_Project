from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PromotionBase(BaseModel):
    title: str
    description: Optional[str] = None
    discount_percent: float
    start_date: datetime
    end_date: datetime


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    discount_percent: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Promotion(PromotionBase):
    id: int

    class Config:
        from_attributes = True
