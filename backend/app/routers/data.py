"""
Router compatible con PostgREST que sirve al panel admin.
Expone las tablas locales SQLite bajo /rest/v1/{table}, y RPCs bajo
/rest/v1/rpc/{name}. Soporta los operadores que usa el panel:
  GET    ?col=eq.X&order=col.desc&limit=N
  POST   body JSON
  PATCH  ?col=eq.X  body JSON
  DELETE ?col=eq.X
"""
from fastapi import APIRouter, HTTPException, Request
from app.services import store

router = APIRouter()


@router.get("/{table}")
async def get_rows(table: str, request: Request):
    qs = "?" + (request.url.query or "")
    try:
        return await store.query(table, qs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{table}")
async def create_row(table: str, request: Request):
    body = await request.json()
    try:
        if isinstance(body, list):
            return [await store.insert(table, item) for item in body]
        return await store.insert(table, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{table}")
async def update_rows(table: str, request: Request):
    qs = "?" + (request.url.query or "")
    body = await request.json()
    try:
        return await store.update(table, qs, body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{table}")
async def delete_rows(table: str, request: Request):
    qs = "?" + (request.url.query or "")
    try:
        n = await store.delete(table, qs)
        return {"deleted": n}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rpc/{name}")
async def call_rpc(name: str, request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    try:
        return await store.rpc(name, body or {})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
