from fastapi import FastAPI
from app.routes import auth  # pastikan path sesuai
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

app = FastAPI()

app.include_router(auth.router)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API berjalan dengan baik"}

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(os.path.join("app", "static", "favicon.ico"))

app.include_router(auth.router)
