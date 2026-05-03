"""
CRM Router — Contactos, mensajes, seguimientos.
Estos endpoints los puede usar el panel o el agente.
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.services.store import query, insert, update

router = APIRouter()


class ContactoCreate(BaseModel):
    nombre: str
    whatsapp: str = ""
    instagram: str = ""
    canal: str = "manual"
    curso_interes: str = ""


class SeguimientoCreate(BaseModel):
    contacto_id: int
    fecha_programada: str
    mensaje_sugerido: str = ""


@router.get("/contactos")
async def list_contactos(estado: Optional[str] = None):
    params = "?order=created_at.desc"
    if estado:
        params += f"&estado=eq.{estado}"
    return await query("contactos", params)


@router.post("/contactos")
async def create_contacto(data: ContactoCreate):
    return await insert("contactos", {
        "nombre": data.nombre,
        "whatsapp": data.whatsapp,
        "instagram": data.instagram,
        "canal": data.canal,
        "estado": "LEAD",
        "curso_interes": data.curso_interes,
    })


@router.get("/contactos/{cid}/historial")
async def get_historial(cid: int):
    mensajes = await query("mensajes", f"?contacto_id=eq.{cid}&order=created_at")
    seguimientos = await query("seguimientos", f"?contacto_id=eq.{cid}&order=created_at.desc")
    contacto = await query("contactos", f"?id=eq.{cid}")
    return {
        "contacto": contacto[0] if contacto else None,
        "mensajes": mensajes,
        "seguimientos": seguimientos,
    }


@router.get("/seguimientos")
async def list_seguimientos(estado: Optional[str] = None):
    params = "?order=fecha_programada"
    if estado:
        params += f"&estado=eq.{estado}"
    return await query("seguimientos", params)


@router.post("/seguimientos")
async def create_seguimiento(data: SeguimientoCreate):
    return await insert("seguimientos", {
        "contacto_id": data.contacto_id,
        "fecha_programada": data.fecha_programada,
        "mensaje_sugerido": data.mensaje_sugerido,
        "estado": "pendiente",
    })


@router.patch("/seguimientos/{sid}")
async def update_seguimiento(sid: int, estado: str):
    return await update("seguimientos", f"?id=eq.{sid}", {"estado": estado})


@router.get("/dashboard")
async def crm_dashboard():
    """Métricas del funnel de CRM."""
    contactos = await query("contactos", "?order=id")
    estados = ["LEAD", "CONSULTANDO", "INTERESADO", "INSCRIPTO", "NO_POR_AHORA"]
    funnel = {}
    for e in estados:
        funnel[e] = len([c for c in contactos if c.get("estado") == e])

    pendientes = await query("seguimientos", "?estado=eq.pendiente")

    return {
        "total_contactos": len(contactos),
        "funnel": funnel,
        "seguimientos_pendientes": len(pendientes),
        "tasa_conversion": (
            round(funnel.get("INSCRIPTO", 0) / max(len(contactos), 1) * 100, 1)
        ),
    }
