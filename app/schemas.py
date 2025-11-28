# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DatasetBase(BaseModel):
    filename: str
    rows: int
    columns: str 

class DatasetCreate(DatasetBase):
    pass

class DatasetResponse(DatasetBase):
    id: int
    imported_at: datetime
    table_name: str

    class Config:
        from_attributes = True  


class ErrorResponse(BaseModel):
    detail: str

class SuccessResponse(BaseModel):
    message: str
    success: bool = True


# ---------- CUSTOMERS ----------

class CustomerBase(BaseModel):
    CustomerID: int
    CustomerName: str
    Email: str

    class Config:
        from_attributes = True  # Pydantic v2


# ---------- PRODUCTS ----------

class ProductBase(BaseModel):
    StockCode: str
    Description: str
    Categoria: Optional[str] = None
    UnitPrice: float
    Image: Optional[str] = None

    class Config:
        from_attributes = True


# ---------- SALES ----------

class SaleBase(BaseModel):
    CustomerID: int
    CustomerName: str
    InvoiceDate: datetime
    StockCode: str
    Description: str
    UnitPrice: float
    Quantity: int
    Country: str
    TotalPrize: float
    Categoria: str

    class Config:
        from_attributes = True
