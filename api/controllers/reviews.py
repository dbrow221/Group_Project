from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import reviews as model  # Assuming your model file is called reviews.py

def create(db: Session, request):
    new_review = model.Review(
        sandwich_name=request.sandwich_name,
        description=request.description,
        date=request.date,
    )

    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_review


def read_all(db: Session):
    try:
        reviews = db.query(model.Review).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return reviews


def read_one(db: Session, review_id: int):
    try:
        review = db.query(model.Review).filter(model.Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return review


def update(db: Session, review_id: int, request):
    try:
        review = db.query(model.Review).filter(model.Review.id == review_id)
        if not review.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review ID not found!")
        update_data = request.dict(exclude_unset=True)
        review.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return review.first()


def delete(db: Session, review_id: int):
    try:
        review = db.query(model.Review).filter(model.Review.id == review_id)
        if not review.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review ID not found!")
        review.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
