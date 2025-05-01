from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import order_details as model
from sqlalchemy.exc import SQLAlchemyError
from ..schemas.order_details import OrderDetailCreate, OrderDetailUpdate  # Make sure schemas are correctly imported

def create(db: Session, request: OrderDetailCreate):  # Type hinting for clarity
    try:
        new_item = model.OrderDetail(**request.model_dump())  # Safe if request is a Pydantic model
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item

def read_all(db: Session):
    try:
        result = db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, item_id: int):  # Add type hint
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def update(db: Session, item_id: int, request: OrderDetailUpdate):  # Type hinting and correct schema
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()  # Could return item.one() after commit

def delete(db: Session, item_id: int):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
