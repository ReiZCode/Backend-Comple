# app/queries/recommendations_query.py

from fastapi import APIRouter, HTTPException, Query, Path, Depends
from sqlalchemy.orm import Session
import pandas as pd

from ..database import get_db
from .. import models
from ..recommendations import graph_recommender as rec

router = APIRouter(
    prefix="/queries/recommendations",
    tags=["Recommendations"],
)


@router.get("/by-customer/{customer_id}")
def get_recommendations_for_customer(
    customer_id: str = Path(
        ...,
        description="ID del cliente tal como está en la tabla sales (CustomerID)",
    ),
    k: int = Query(10, ge=1, le=50, description="Cantidad de productos recomendados"),
    db: Session = Depends(get_db),
):
    """
    Devuelve recomendaciones de productos para un cliente,
    basadas en la tabla 'sales' de la base de datos (Supabase)
    y el algoritmo de Dijkstra.
    """

    # Traer todas las ventas desde la BD
    sales = db.query(models.Sale).all()
    if not sales:
        raise HTTPException(status_code=404, detail="No hay ventas en la base de datos")

    # Convertir a DataFrame compatible con el algoritmo
    rows = []
    for s in sales:
        rows.append(
            {
                "CustomerID": str(s.CustomerID),   # lo pasamos a string para que coincida con el algoritmo
                "StockCode": s.StockCode,
                "Description": s.Description,
                "TotalPrize": float(s.TotalPrize or 0),
            }
        )

    df = pd.DataFrame(rows)

    #  Asegurarnos de que el ID del cliente esté en el DataFrame
    customer_id_str = str(customer_id)
    if customer_id_str not in df["CustomerID"].values:
        raise HTTPException(
            status_code=404,
            detail=f"El cliente {customer_id} no tiene ventas registradas",
        )

    #  Llamar al recomendador
    try:
        recomendaciones = rec.recomendar_productos_para_cliente(
            df, customer_id_str, k=k
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return recomendaciones
