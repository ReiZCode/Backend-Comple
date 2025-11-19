from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/commands/sales", tags=["Sales Commands"])


@router.post("/create")
def create_sale(sale: schemas.SaleBase, db: Session = Depends(get_db)):
    new_sale = models.Sale(**sale.model_dump())
    db.add(new_sale)
    db.commit()
    return {"message": "Sale creada correctamente"}
