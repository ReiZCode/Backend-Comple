from fastapi import APIRouter, Depends, Query, Path, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/queries/customers", tags=["Customer Queries"])


@router.get("/", response_model=list[schemas.CustomerBase])
def list_customers(limit: int = 100, skip: int = 0, db: Session = Depends(get_db)):
    return db.query(models.Customer).offset(skip).limit(limit).all()


@router.get("/{customer_id}", response_model=schemas.CustomerBase)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = (
        db.query(models.Customer)
        .filter(models.Customer.CustomerID == customer_id)
        .first()
    )
    if not customer:
        raise HTTPException(404, "Customer no encontrado")
    return customer
