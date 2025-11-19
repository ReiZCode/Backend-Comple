from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models 

router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginData(BaseModel):
    email: str
    password: str


@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    
    user = (
        db.query(models.Customer)  
        .filter(models.Customer.Email == data.email) 
        .first()
    )

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

  
    if user.Password != data.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

  
    return {
        "ok": True,
        "user": {
            "id": user.CustomerID,   
            "email": user.Email,
            "name": user.CustomerName,  
        },
    }
