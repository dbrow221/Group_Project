from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import sandwiches as model  # Assuming your model file is called sandwiches.py
from ..schemas.sandwiches import SandwichCreate, SandwichUpdate  # Pydantic models for validation

def create(db: Session, request: SandwichCreate):  # Use Pydantic model for input validation
    try:
        new_item = model.Sandwich(**request.model_dump())  # Creating a new sandwich with validated data
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item

def read_all(db: Session):
    try:
        return db.query(model.Sandwich).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich ID not found!")
        return item
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def update(db: Session, item_id: int, request: SandwichUpdate):  # Ensure to use Pydantic model for update validation
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich ID not found!")
        update_data = request.dict(exclude_unset=True)  # Pydantic model validation for update
        item.update(update_data, synchronize_session=False)
        db.commit()
        return item.first()  # Return the updated sandwich
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def delete(db: Session, item_id: int):
    try:
        item = db.query(model.Sandwich).filter(model.Sandwich.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich ID not found!")
        item.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
