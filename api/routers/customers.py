from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..controllers import customers as controller
from ..schemas import customers as schema
from ..dependencies.database import get_db

router = APIRouter(
    tags=["Customers"],
    prefix="/customers"
)

@router.post("/", response_model=schema.Customer, status_code=status.HTTP_201_CREATED)
def create_customer(request: schema.CustomerCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Customer])
def get_all_customers(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{customer_id}", response_model=schema.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=customer_id)

@router.put("/{customer_id}", response_model=schema.Customer)
def update_customer(customer_id: int, request: schema.CustomerUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=customer_id)

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=customer_id)
