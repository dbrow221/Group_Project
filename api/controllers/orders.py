from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import orders as model
from ..models import sandwiches as sandwich_model
from ..models import order_details as order_detail_model
from sqlalchemy.exc import SQLAlchemyError
from ..schemas.orders import OrderCreate  # Use this for validation

def create(db: Session, request: OrderCreate):
    try:
        # Fetch the sandwich to get its price
        sandwich = db.query(sandwich_model.Sandwich).filter(sandwich_model.Sandwich.id == request.sandwich_id).first()
        if not sandwich:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found!")

        # Calculate the total price
        total_price = sandwich.price * request.quantity

        # Create a new Order instance
        new_order = model.Order(
            customer_id=request.customer_id,  # Assuming this field is still required
            description=request.description,
            order_status="Pending",  # Default status
            order_type="Online",  # Default type
            total_price=total_price  # Add a field for total price
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Create a corresponding OrderDetail
        new_order_detail = order_detail_model.OrderDetail(
            order_id=new_order.id,
            sandwich_id=request.sandwich_id,
            amount=request.quantity
        )
        db.add(new_order_detail)
        db.commit()
        db.refresh(new_order_detail)

    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return {
        "order_id": new_order.id,
        "customer_id": new_order.customer_id,
        "description": new_order.description,
        "order_status": new_order.order_status,
        "order_type": new_order.order_type,
        "total_price": new_order.total_price,
        "sandwich_id": request.sandwich_id,
        "quantity": request.quantity
    }