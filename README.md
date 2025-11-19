# API de Importación de Datos

Este es un backend en Python con FastAPI que permite importar archivos CSV o Excel a una base de datos SQL, con una interfaz Swagger para probar los endpoints.

## Características

- Importación de archivos CSV y Excel
- Documentación interactiva con Swagger UI
- Almacenamiento en base de datos SQL (SQLite por defecto)
- Endpoints RESTful para gestionar datasets
- Validación de datos con Pydantic
- Manejo de CORS

## Requisitos

- Python 3.8+
- pip

## Instalación

1. Clona el repositorio:
   ```bash
   git clone [tu-repositorio]
   cd [nombre-del-repositorio]
   ```

2. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # En Windows
   # o
   source venv/bin/activate  # En Linux/Mac
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno (opcional):
   - Copia el archivo `.env.example` a `.env`
   - Edita las variables según sea necesario

## Uso

1. Inicia el servidor de desarrollo:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Abre tu navegador y ve a:
   - Documentación interactiva (Swagger UI): http://127.0.0.1:8000/docs
   - Documentación alternativa (ReDoc): http://127.0.0.1:8000/redoc

## Endpoints

- `GET /`: Página de inicio
- `POST /upload/`: Sube un archivo CSV o Excel
- `GET /datasets/`: Lista todos los datasets importados

## Ejemplo de uso con cURL

Para subir un archivo:
```bash
curl -X 'POST' \
  'http://localhost:8000/upload/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@tu_archivo.csv;type=text/csv' \
  -F 'table_name=mi_tabla' \
  -F 'if_exists=replace'
```

## Estructura del proyecto

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # Aplicación principal
│   ├── database.py      # Configuración de la base de datos
│   ├── models.py        # Modelos de SQLAlchemy
│   └── schemas.py       # Esquemas Pydantic
├── .env                 # Variables de entorno
├── requirements.txt     # Dependencias
└── README.md           # Este archivo
```

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
