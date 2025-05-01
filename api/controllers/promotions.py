from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import promotions as model  # Assuming the model file is named promotions.py
from ..schemas.promotions import PromotionCreate, PromotionUpdate  # Ensure these schemas are imported

def create(db: Session, request: PromotionCreate):  # Ensure you're passing the Pydantic schema
    try:
        # Create a new promotion instance using data from the Pydantic model
        new_promotion = model.Promotion(**request.model_dump())
        db.add(new_promotion)
        db.commit()
        db.refresh(new_promotion)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_promotion

def read_all(db: Session):
    try:
        promotions = db.query(model.Promotion).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promotions

def read_one(db: Session, promotion_code: str):  # Added type hint for promotion_code
    try:
        promotion = db.query(model.Promotion).filter(model.Promotion.code == promotion_code).first()
        if not promotion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion code not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promotion

def update(db: Session, promotion_code: str, request: PromotionUpdate):  # Added type hint for promotion_code and request
    try:
        promotion = db.query(model.Promotion).filter(model.Promotion.code == promotion_code)
        if not promotion.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion code not found!")
        update_data = request.dict(exclude_unset=True)
        promotion.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promotion.first()  # Return the updated promotion

def delete(db: Session, promotion_code: str):
    try:
        promotion = db.query(model.Promotion).filter(model.Promotion.code == promotion_code)
        if not promotion.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion code not found!")
        promotion.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
