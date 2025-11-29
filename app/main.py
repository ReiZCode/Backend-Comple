from fastapi import FastAPI
from .database import Base, engine

# Importar routers
from .queries.sales_query import router as sales_query_router
from .queries.customers_query import router as customers_query_router
from .queries.products_query import router as products_query_router
from .queries.recommendations_query import router as recommendations_query_router
from .commands.sales_command import router as sales_command_router
from .routes import auth  
from fastapi.responses import RedirectResponse
Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://comple-front.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          
    allow_credentials=True,
    allow_methods=["*"],            
    allow_headers=["*"],            
)



app.include_router(sales_query_router)
app.include_router(customers_query_router)
app.include_router(products_query_router)
app.include_router(recommendations_query_router)
app.include_router(sales_command_router)
app.include_router(auth.router)  

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
