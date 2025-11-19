@echo off
echo Iniciando la aplicación...
python -m uvicorn app.main:app --reload
pause
