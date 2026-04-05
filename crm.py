from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    Contacto, ContactoCreate, ContactoUpdate,
    Mensaje, MensajeCreate,
    Seguimiento, SeguimientoCreate,
)
from app.services.store import store

router = APIRouter()

# ── Contactos ──
@router.get("/contactos", response_model=list[Contacto])
def listar_contactos(estado: str = None):
    contactos = store.get_all("contactos")
    if estado:
        contactos = [c for c in contactos if c.get("estado") == estado]
    return contactos

@router.post("/contactos", response_model=Contacto)
def crear_contacto(data: ContactoCreate):
    d = data.model_dump()
    d["estado"] = "LEAD"
    d["motivo_no"] = ""
    return store.create("contactos", d)

@router.put("/contactos/{id}", response_model=Contacto)
def actualizar_contacto(id: int, data: ContactoUpdate):
    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    r = store.update("contactos", id, updates)
    if not r: raise HTTPException(404)
    return r

@router.get("/contactos/{id}/historial")
def historial_contacto(id: int):
    """Historial completo de un contacto: mensajes + seguimientos."""
    contacto = store.get("contactos", id)
    if not contacto: raise HTTPException(404)
    mensajes = store.filter("mensajes", contact_id=id)
    seguimientos = store.filter("seguimientos", contact_id=id)
    return {
        "contacto": contacto,
        "mensajes": sorted(mensajes, key=lambda m: m.get("created_at", "")),
        "seguimientos": seguimientos,
    }

# ── Conversaciones ──
@router.get("/mensajes/{contact_id}", response_model=list[Mensaje])
def listar_mensajes(contact_id: int):
    msgs = store.filter("mensajes", contact_id=contact_id)
    return sorted(msgs, key=lambda m: m.get("created_at", ""))

@router.post("/mensajes", response_model=Mensaje)
def crear_mensaje(data: MensajeCreate):
    return store.create("mensajes", data.model_dump())

# ── Seguimientos ──
@router.get("/seguimientos", response_model=list[Seguimiento])
def listar_seguimientos(estado: str = None):
    segs = store.get_all("seguimientos")
    if estado:
        segs = [s for s in segs if s.get("estado") == estado]
    return segs

@router.post("/seguimientos", response_model=Seguimiento)
def crear_seguimiento(data: SeguimientoCreate):
    d = data.model_dump()
    d["estado"] = "pendiente"
    d["fecha_programada"] = str(d["fecha_programada"])
    return store.create("seguimientos", d)

@router.put("/seguimientos/{id}")
def actualizar_seguimiento(id: int, estado: str):
    r = store.update("seguimientos", id, {"estado": estado})
    if not r: raise HTTPException(404)
    return r

# ── Dashboard CRM ──
@router.get("/dashboard")
def crm_dashboard():
    """Resumen del funnel de ventas."""
    contactos = store.get_all("contactos")
    segs = store.get_all("seguimientos")
    funnel = {}
    for c in contactos:
        estado = c.get("estado", "LEAD")
        funnel[estado] = funnel.get(estado, 0) + 1

    pendientes = len([s for s in segs if s.get("estado") == "pendiente"])

    return {
        "total_contactos": len(contactos),
        "funnel": funnel,
        "seguimientos_pendientes": pendientes,
    }
