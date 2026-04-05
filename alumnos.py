from fastapi import APIRouter, HTTPException
from app.models.schemas import Alumno, AlumnoCreate, AlumnoUpdate
from app.services.store import store

router = APIRouter()

@router.get("/", response_model=list[Alumno])
def listar(estado: str = None, docente_id: int = None):
    alumnos = store.get_all("alumnos")
    if estado:
        alumnos = [a for a in alumnos if a.get("estado") == estado]
    if docente_id:
        alumnos = [a for a in alumnos if a.get("docente_id") == docente_id]
    return alumnos

@router.get("/{id}", response_model=Alumno)
def obtener(id: int):
    a = store.get("alumnos", id)
    if not a: raise HTTPException(404, "Alumno no encontrado")
    return a

@router.post("/", response_model=Alumno)
def crear(data: AlumnoCreate):
    d = data.model_dump()
    d["estado"] = "activo"
    d["canal_ingreso"] = "manual"
    return store.create("alumnos", d)

@router.put("/{id}", response_model=Alumno)
def actualizar(id: int, data: AlumnoUpdate):
    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    r = store.update("alumnos", id, updates)
    if not r: raise HTTPException(404)
    return r

@router.delete("/{id}")
def eliminar(id: int):
    if not store.delete("alumnos", id):
        raise HTTPException(404)
    return {"ok": True}

@router.post("/{id}/desactivar")
def desactivar(id: int):
    r = store.update("alumnos", id, {"estado": "inactivo"})
    if not r: raise HTTPException(404)
    return r

@router.post("/{id}/reactivar")
def reactivar(id: int):
    r = store.update("alumnos", id, {"estado": "activo"})
    if not r: raise HTTPException(404)
    return r
