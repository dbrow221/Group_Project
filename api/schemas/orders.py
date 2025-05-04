from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail
from .customers import Customer



class OrderBase(BaseModel):
    customer_id: int  # Assuming this is still required
    description: Optional[str] = None
    sandwich_id: int  # Include sandwich_id
    quantity: int  # Include quantity
    order_type: str

class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    description: Optional[str] = None
    order_status: Optional[str] = None
    promotion_code: Optional[str] = None
    order_date: Optional[datetime] = None
    order_type: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
