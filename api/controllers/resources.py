from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import resources as model  # Assuming your model file is called resources.py
from ..schemas.resources import ResourceCreate, ResourceUpdate  # Ensure these schemas are imported

def create(db: Session, request: ResourceCreate):  # Make sure to pass the Pydantic schema
    try:
        # Create a new resource instance using data from the Pydantic model
        new_item = model.Resource(**request.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item

def read_all(db: Session):
    try:
        result = db.query(model.Resource).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, item_id: int):  # Added type hint for item_id
    try:
        item = db.query(model.Resource).filter(model.Resource.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def update(db: Session, item_id: int, request: ResourceUpdate):  # Added type hint for item_id and request
    try:
        item = db.query(model.Resource).filter(model.Resource.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource ID not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()  # Return the updated resource

def delete(db: Session, item_id: int):  # Added type hint for item_id
    try:
        item = db.query(model.Resource).filter(model.Resource.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource ID not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
