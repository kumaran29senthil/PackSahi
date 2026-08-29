from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.database import engine, Base
import app.models.scan  # Import models to ensure they are registered with Base

# Create database tables (For local dev without alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PackSahi Legal Metrology AI Engine",
    description="API for checking compliance of packaged commodities",
    version="1.0.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "PackSahi Engine is running"}
