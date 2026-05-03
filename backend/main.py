"""
AburridoNT API — Agente IA + CRM + Datos del panel.
DB local: SQLite (db/aburridont.db). Sin servicios externos.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import agente, crm, data
from app.db import get_conn

app = FastAPI(
    title="AburridoNT API",
    version="3.0.0",
    description="Backend: Agente IA + CRM (SQLite local)",
)

DEFAULT_ORIGINS = "http://localhost:5173,http://127.0.0.1:5173"
allowed_origins = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", DEFAULT_ORIGINS).split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(agente.router, prefix="/api/agente", tags=["Agente IA"])
app.include_router(crm.router, prefix="/api/crm", tags=["CRM"])
# Compatible con la forma /rest/v1 que ya usa el panel.
app.include_router(data.router, prefix="/rest/v1", tags=["Data"])


@app.on_event("startup")
def _startup():
    # Inicializa la DB local (crea schema y aplica seed si está vacía).
    get_conn()


@app.get("/")
def root():
    return {"status": "ok", "app": "AburridoNT API v3.0 (SQLite)"}


@app.get("/health")
def health():
    return {"status": "healthy"}
