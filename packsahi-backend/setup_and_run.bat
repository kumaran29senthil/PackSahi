@echo off
echo =======================================================
echo    PackSahi Backend - Local Setup ^& Run Script
echo =======================================================

echo.
echo [1/4] Creating Python Virtual Environment (venv)...
python -m venv venv

echo.
echo [2/4] Activating Virtual Environment...
call venv\Scripts\activate.bat

echo.
echo [3/4] Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm

echo.
echo [4/4] Starting FastAPI Server...
echo The API will be available at http://127.0.0.1:8000
echo Swagger UI Docs: http://127.0.0.1:8000/docs
echo.
uvicorn app.main:app --reload
