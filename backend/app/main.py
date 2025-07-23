# File: backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes.api_router import api_router
from .database import Base, engine

# Membuat tabel di database jika belum ada (berguna untuk setup awal)
Base.metadata.create_all(bind=engine)

# Inisialisasi aplikasi FastAPI
app = FastAPI(
    title="HRIS API",
    description="API untuk Sistem Informasi Sumber Daya Manusia.",
    version="1.0.0"
)

# Konfigurasi CORS (Cross-Origin Resource Sharing)
# Mengizinkan frontend (misal: localhost:5173) untuk berkomunikasi dengan backend ini
origins = [
    "http://localhost",
    "http://localhost:5173", 
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Mengizinkan semua metode (GET, POST, etc.)
    allow_headers=["*"], # Mengizinkan semua header
)


# Daftarkan "router induk" ke aplikasi utama
# Sekarang semua endpoint dari auth, users, dan menus sudah otomatis terdaftar
app.include_router(api_router)


# Endpoint sederhana untuk mengecek apakah server berjalan
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to HRIS API!"}