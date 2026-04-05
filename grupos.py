from fastapi import APIRouter, HTTPException
from app.models.schemas import Grupo, GrupoCreate, GrupoUpdate
from app.services.store import store

router = APIRouter()

@router.get("/", response_model=list[Grupo])
def listar(activo: bool = None):
    grupos = store.get_all("grupos")
    if activo is not None:
        grupos = [g for g in grupos if g.get("activo") == activo]
    return grupos

@router.get("/{id}")
def obtener(id: int):
    g = store.get("grupos", id)
    if not g: raise HTTPException(404, "Grupo no encontrado")
    # Enrich with alumnos
    alumnos = store.filter("alumnos", grupo_id=id, estado="activo")
    return {**g, "alumnos": alumnos, "cantidad_alumnos": len(alumnos)}

@router.post("/", response_model=Grupo)
def crear(data: GrupoCreate):
    d = data.model_dump()
    d["activo"] = True
    return store.create("grupos", d)

@router.put("/{id}", response_model=Grupo)
def actualizar(id: int, data: GrupoUpdate):
    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    r = store.update("grupos", id, updates)
    if not r: raise HTTPException(404)
    return r

@router.delete("/{id}")
def eliminar(id: int):
    # Desasignar alumnos del grupo
    alumnos = store.filter("alumnos", grupo_id=id)
    for a in alumnos:
        store.update("alumnos", a["id"], {"grupo_id": None})
    if not store.delete("grupos", id):
        raise HTTPException(404)
    return {"ok": True, "alumnos_desasignados": len(alumnos)}

@router.get("/{id}/disponibilidad")
def disponibilidad(id: int):
    """Cuántos lugares quedan en el grupo."""
    g = store.get("grupos", id)
    if not g: raise HTTPException(404)
    count = len(store.filter("alumnos", grupo_id=id, estado="activo"))
    return {
        "grupo_id": id,
        "capacidad_max": g["capacidad_max"],
        "ocupados": count,
        "disponibles": g["capacidad_max"] - count,
    }
