"""
Router del Agente IA.
POST /api/agente/mensaje — procesa un mensaje y devuelve respuesta
GET  /api/agente/test    — endpoint de prueba
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.agente_service import procesar_mensaje

router = APIRouter()


class MensajeRequest(BaseModel):
    mensaje: str
    canal: str = "whatsapp"
    whatsapp: str = ""
    nombre: str = ""


class MensajeResponse(BaseModel):
    respuesta: str
    accion: Optional[str] = None
    datos: Optional[dict] = None
    contacto_id: Optional[int] = None


@router.post("/mensaje", response_model=MensajeResponse)
async def enviar_mensaje(req: MensajeRequest):
    result = await procesar_mensaje(
        mensaje=req.mensaje,
        canal=req.canal,
        contacto_whatsapp=req.whatsapp,
        contacto_nombre=req.nombre,
    )
    return result


@router.get("/test")
async def test_agente():
    result = await procesar_mensaje(
        mensaje="Hola, quiero averiguar por clases de inglés para mi hijo de 8 años",
        canal="test",
        contacto_whatsapp="+5411test",
        contacto_nombre="Test User",
    )
    return result
