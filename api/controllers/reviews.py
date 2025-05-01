from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import reviews as model  # Assuming your model file is called reviews.py
from ..schemas.reviews import ReviewCreate, ReviewUpdate  # Ensure to import Pydantic models for validation

def create(db: Session, request: ReviewCreate):  # Use Pydantic model for input validation
    try:
        new_review = model.Review(**request.model_dump())  # Creating a new review with validated data
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_review

def read_all(db: Session):
    try:
        return db.query(model.Review).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def read_one(db: Session, review_id: int):
    try:
        review = db.query(model.Review).filter(model.Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review ID not found!")
        return review
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def update(db: Session, review_id: int, request: ReviewUpdate):  # Ensure to use the Pydantic model
    try:
        review = db.query(model.Review).filter(model.Review.id == review_id)
        if not review.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review ID not found!")
        update_data = request.dict(exclude_unset=True)  # Pydantic model validation for update
        review.update(update_data, synchronize_session=False)
        db.commit()
        return review.first()  # Return the updated review
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

def delete(db: Session, review_id: int):
    try:
        review = db.query(model.Review).filter(model.Review.id == review_id)
        if not review.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review ID not found!")
        review.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
