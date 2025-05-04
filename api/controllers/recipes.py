from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import recipes as model  # Assuming your model file is called recipes.py
from ..models.resources import Resource  # Import Resource for validation
from ..schemas.recipes import RecipeCreate, RecipeUpdate  # Ensure these schemas are imported

def create(db: Session, request: RecipeCreate):  # Make sure to pass the Pydantic schema
    try:
        # Create a new recipe instance using data from the Pydantic model
        new_item = model.Recipe(**request.model_dump())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item

def read_all(db: Session):
    try:
        result = db.query(model.Recipe).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, item_id: int):  # Added type hint for item_id
    try:
        item = db.query(model.Recipe).filter(model.Recipe.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe ID not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

def update(db: Session, item_id: int, request: RecipeUpdate):  # Added type hint for item_id and request
    try:
        item = db.query(model.Recipe).filter(model.Recipe.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe ID not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()  # Return the updated recipe

def delete(db: Session, item_id: int):  # Added type hint for item_id
    try:
        item = db.query(model.Recipe).filter(model.Recipe.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe ID not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def add_resource_to_recipe(db: Session, recipe_id: int, resource_id: int, quantity: float):
    try:
        # Validate recipe and resource existence
        recipe = db.query(model.Recipe).filter(model.Recipe.id == recipe_id).first()
        resource = db.query(Resource).filter(Resource.id == resource_id).first()
        if not recipe or not resource:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Recipe or Resource not found!"
            )

        # Add the resource to the recipe
        recipe_resource = model.RecipeResource(
            recipe_id=recipe_id, resource_id=resource_id, quantity_needed=quantity
        )
        db.add(recipe_resource)
        db.commit()
        db.refresh(recipe_resource)

        return recipe_resource
    except SQLAlchemyError as e:
        error = str(e.__dict__.get("orig", str(e)))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)