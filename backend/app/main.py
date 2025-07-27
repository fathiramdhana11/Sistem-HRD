# File: backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes.api_router import api_router
from . import models
from .database import engine, Base
from .api.routes import auth
import os
from dotenv import load_dotenv

load_dotenv()

# Ini akan membuat tabel jika belum ada
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Gunakan environment variable untuk CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)