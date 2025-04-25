from typing import Optional, List
from pydantic import BaseModel
from .sandwiches import Sandwich


class CustomerBase(BaseModel):
    name: str
    email: str
    phone: str
    address: str



class CustomerCreate(CustomerBase):
    pass  # Add fields like email, phone if needed


class CustomerUpdate(BaseModel):
    name: Optional[str] = None


class Customer(CustomerBase):
    id: int
    order_id: Optional[int]
    class Config:
        from_attributes = True
