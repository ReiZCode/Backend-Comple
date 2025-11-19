from fastapi import APIRouter, Depends, Query, Path, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/queries/products", tags=["Product Queries"])


@router.get("/", response_model=list[schemas.ProductBase])
def list_products(limit: int = 100, skip: int = 0, db: Session = Depends(get_db)):
    return db.query(models.Product).offset(skip).limit(limit).all()


@router.get("/{stock_code}", response_model=schemas.ProductBase)
def get_product(stock_code: str, db: Session = Depends(get_db)):
    product = (
        db.query(models.Product)
        .filter(models.Product.StockCode == stock_code)
        .first()
    )
    if not product:
        raise HTTPException(404, "Producto no encontrado")
    return product
