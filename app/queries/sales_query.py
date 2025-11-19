from fastapi import APIRouter, Depends, Query, Path, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/queries/sales", tags=["Sales Queries"])


@router.get("/", response_model=list[schemas.SaleBase])
def list_sales(
    limit: int = Query(100, ge=1, le=1000),
    skip: int = Query(0, ge=0),
    customer_id: int | None = Query(None),
    country: str | None = Query(None),
    categoria: str | None = Query(None),
    db: Session = Depends(get_db),
):

    query = db.query(models.Sale)

    if customer_id is not None:
        query = query.filter(models.Sale.CustomerID == customer_id)
    if country:
        query = query.filter(models.Sale.Country == country)
    if categoria:
        query = query.filter(models.Sale.Categoria == categoria)

    return query.offset(skip).limit(limit).all()


@router.get("/by-customer/{customer_id}", response_model=list[schemas.SaleBase])
def sales_by_customer(
    customer_id: int = Path(...),
    db: Session = Depends(get_db),
):
    """
    Devuelve TODAS las ventas realizadas por un CustomerID
    """
    sales = db.query(models.Sale).filter(models.Sale.CustomerID == customer_id).all()

    if not sales:
        raise HTTPException(404, "No existen ventas asociadas a este cliente")

    return sales


@router.get("/by-customer/{customer_id}/summary")
def sales_summary_by_customer(
    customer_id: int = Path(...),
    db: Session = Depends(get_db),
):
    """
    Devuelve un resumen:
    - total gastado
    - compras realizadas
    - total de ítems comprados
    """
    sales = db.query(models.Sale).filter(models.Sale.CustomerID == customer_id).all()

    if not sales:
        raise HTTPException(404, "No hay ventas para este cliente")

    total_gastado = sum(s.TotalPrize for s in sales)
    total_items = sum(s.Quantity for s in sales)
    compras_realizadas = len(sales)

    return {
        "customerId": customer_id,
        "total_gastado": total_gastado,
        "total_items": total_items,
        "compras_realizadas": compras_realizadas,
    }



