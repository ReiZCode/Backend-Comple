# app/models.py
from datetime import datetime
from sqlalchemy import (
    Column, Integer, BigInteger, String, DateTime,
    Text, Float, ForeignKey
)
from sqlalchemy.orm import relationship
from .database import Base


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    rows = Column(Integer, nullable=False)
    columns = Column(Text, nullable=True)
    imported_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Dataset {self.filename} ({self.rows} filas)>"


class Customer(Base):
    __tablename__ = "customers"

    CustomerID = Column(BigInteger, primary_key=True, index=True)
    CustomerName = Column(String, nullable=False)
    Email = Column(String, nullable=False)
    Password = Column(String, nullable=False)

    # Relación 1:N con Sales
    sales = relationship("Sale", back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    StockCode = Column(String, primary_key=True, index=True)
    Description = Column(Text, nullable=False)
    Categoria = Column(String, nullable=True)
    UnitPrice = Column(Float, nullable=False)

    # Relación 1:N con Sales
    sales = relationship("Sale", back_populates="product")


class Sale(Base):
    __tablename__ = "sales"

    # No tienes columna id, así que usamos una clave compuesta lógica
    CustomerID = Column(
        BigInteger,
        ForeignKey("customers.CustomerID"),
        primary_key=True
    )
    InvoiceDate = Column(DateTime(timezone=True), primary_key=True)
    StockCode = Column(
        String,
        ForeignKey("products.StockCode"),
        primary_key=True
    )

    CustomerName = Column(String, nullable=False)
    Description = Column(Text, nullable=False)
    UnitPrice = Column(Float, nullable=False)
    Quantity = Column(BigInteger, nullable=False)
    Country = Column(String, nullable=False)
    TotalPrize = Column(Float, nullable=False)
    Categoria = Column(String, nullable=False)

    # Relaciones inversas
    customer = relationship("Customer", back_populates="sales")
    product = relationship("Product", back_populates="sales")
