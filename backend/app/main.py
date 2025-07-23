# File: backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes.api_router import api_router
from . import models # Import models package
from .database import engine

# Ini akan membuat tabel jika belum ada
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HRIS API",
    description="API for Human Resource Information System",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ganti dengan domain frontend Anda di produksi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)