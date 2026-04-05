"""
AburridoNT Backend — FastAPI
Endpoints para: Panel admin + Agente IA + CRM
Sin conexión a Supabase aún (se agrega después)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import docentes, grupos, alumnos, horarios, crm, agente

app = FastAPI(
    title="AburridoNT API",
    description="Backend para instituto de inglés AburridoNT — Panel admin, CRM y Agente IA",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: ["https://aburridont.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docentes.router, prefix="/api/docentes", tags=["Docentes"])
app.include_router(grupos.router, prefix="/api/grupos", tags=["Grupos"])
app.include_router(alumnos.router, prefix="/api/alumnos", tags=["Alumnos"])
app.include_router(horarios.router, prefix="/api/horarios", tags=["Horarios"])
app.include_router(crm.router, prefix="/api/crm", tags=["CRM"])
app.include_router(agente.router, prefix="/api/agente", tags=["Agente IA"])


@app.get("/")
def root():
    return {"status": "ok", "app": "AburridoNT API v1.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}
