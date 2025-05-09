from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import recipes as controller
from ..schemas import recipes as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Recipes'],
    prefix="/recipes"
)

@router.post("/", response_model=schema.Recipe, status_code=status.HTTP_201_CREATED)
def create(request: schema.RecipeCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Recipe])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Recipe)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Recipe)
def update(item_id: int, request: schema.RecipeUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, item_id=item_id, request=request)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@router.post("/{recipe_id}/resources", status_code=status.HTTP_201_CREATED)
def add_resource_to_recipe(recipe_id: int, resource_id: int, quantity: float, db: Session = Depends(get_db)):
    return controller.add_resource_to_recipe(db=db, recipe_id=recipe_id, resource_id=resource_id, quantity=quantity)