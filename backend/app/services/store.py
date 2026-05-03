"""
Capa de acceso a datos sobre SQLite.

Expone helpers tipo PostgREST (query/insert/update/delete) para que el
agente y el CRM mantengan la misma forma de invocación que tenían con
Supabase, pero corriendo todo contra el archivo local db/aburridont.db.
"""
from __future__ import annotations

import re
from typing import Any, Iterable, Optional
from urllib.parse import parse_qsl, urlparse

from app.db import cursor, row_to_dict, BOOL_COLS

# Whitelist de tablas accesibles por el panel + servicios.
ALLOWED_TABLES = {
    "docentes", "tarifas", "disponibilidad", "grupos", "grupo_horarios",
    "alumnos", "pagos", "movimientos", "snapshots_mensuales",
    "contactos", "mensajes", "seguimientos",
}

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _safe_table(table: str) -> str:
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Tabla no permitida: {table}")
    return table


def _safe_ident(name: str) -> str:
    if not _IDENT_RE.match(name):
        raise ValueError(f"Identificador inválido: {name}")
    return name


def _coerce_value(v: str) -> Any:
    """Convierte el literal de un filtro PostgREST a su tipo SQLite."""
    if v == "true":
        return 1
    if v == "false":
        return 0
    if v == "null":
        return None
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    return v


def _parse_query(qs: str) -> dict:
    """
    Parsea la query string estilo PostgREST que usa el panel:
      ?col=eq.value         → filtro (col, "=", value)
      ?col=in.(a,b,c)       → filtro (col, "IN", [...])
      ?order=col,col2.desc  → orden
      ?limit=10             → limit
      ?select=col1,col2     → projection (lo aceptamos pero ignoramos para simplificar)
    """
    if qs.startswith("?"):
        qs = qs[1:]
    if not qs:
        return {"filters": [], "order": None, "limit": None}
    pairs = parse_qsl(qs, keep_blank_values=True)
    filters: list[tuple[str, str, Any]] = []
    order = None
    limit = None
    for k, v in pairs:
        if k == "order":
            parts = []
            for token in v.split(","):
                token = token.strip()
                if not token:
                    continue
                col, _, direction = token.partition(".")
                col = _safe_ident(col)
                direction = "DESC" if direction.lower() == "desc" else "ASC"
                parts.append(f"{col} {direction}")
            if parts:
                order = ", ".join(parts)
        elif k == "limit":
            try:
                limit = int(v)
            except ValueError:
                pass
        elif k == "select":
            continue
        else:
            col = _safe_ident(k)
            if "." not in v:
                filters.append((col, "=", _coerce_value(v)))
                continue
            op, _, raw = v.partition(".")
            if op == "eq":
                filters.append((col, "=", _coerce_value(raw)))
            elif op == "neq":
                filters.append((col, "!=", _coerce_value(raw)))
            elif op == "gt":
                filters.append((col, ">", _coerce_value(raw)))
            elif op == "gte":
                filters.append((col, ">=", _coerce_value(raw)))
            elif op == "lt":
                filters.append((col, "<", _coerce_value(raw)))
            elif op == "lte":
                filters.append((col, "<=", _coerce_value(raw)))
            elif op == "is":
                if raw == "null":
                    filters.append((col, "IS NULL", None))
                else:
                    filters.append((col, "=", _coerce_value(raw)))
            elif op == "in":
                items = raw.strip("()").split(",")
                vals = [_coerce_value(x.strip()) for x in items if x.strip()]
                filters.append((col, "IN", vals))
            else:
                filters.append((col, "=", _coerce_value(raw)))
    return {"filters": filters, "order": order, "limit": limit}


def _build_where(filters: list[tuple[str, str, Any]]):
    if not filters:
        return "", []
    chunks = []
    params: list[Any] = []
    for col, op, val in filters:
        if op == "IS NULL":
            chunks.append(f"{col} IS NULL")
        elif op == "IN":
            placeholders = ",".join(["?"] * len(val))
            chunks.append(f"{col} IN ({placeholders})")
            params.extend(val)
        else:
            chunks.append(f"{col} {op} ?")
            params.append(val)
    return "WHERE " + " AND ".join(chunks), params


def _normalize_payload(table: str, data: dict) -> dict:
    """Convierte True/False de Python a 1/0 para SQLite."""
    out = {}
    for k, v in data.items():
        if isinstance(v, bool):
            out[k] = int(v)
        else:
            out[k] = v
    return out


# ── API pública (compatible con el cliente Supabase anterior) ──

async def query(table: str, params: str = "") -> list[dict]:
    table = _safe_table(table)
    parsed = _parse_query(params)
    where_sql, where_params = _build_where(parsed["filters"])
    sql = f"SELECT * FROM {table} {where_sql}"
    if parsed["order"]:
        sql += f" ORDER BY {parsed['order']}"
    if parsed["limit"]:
        sql += f" LIMIT {int(parsed['limit'])}"
    with cursor() as cur:
        cur.execute(sql, where_params)
        return [row_to_dict(r) for r in cur.fetchall()]


async def insert(table: str, data: dict) -> Optional[dict]:
    table = _safe_table(table)
    payload = _normalize_payload(table, data)
    cols = [_safe_ident(c) for c in payload.keys()]
    placeholders = ",".join(["?"] * len(cols))
    col_list = ",".join(cols)
    sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})"
    with cursor() as cur:
        cur.execute(sql, list(payload.values()))
        new_id = cur.lastrowid
        cur.execute(f"SELECT * FROM {table} WHERE id = ?", [new_id])
        row = cur.fetchone()
        return row_to_dict(row) if row else None


async def update(table: str, params: str, data: dict) -> Optional[dict]:
    table = _safe_table(table)
    payload = _normalize_payload(table, data)
    parsed = _parse_query(params)
    where_sql, where_params = _build_where(parsed["filters"])
    set_sql = ", ".join(f"{_safe_ident(k)} = ?" for k in payload.keys())
    sql = f"UPDATE {table} SET {set_sql} {where_sql}"
    with cursor() as cur:
        cur.execute(sql, list(payload.values()) + where_params)
        # devolver primer afectado
        cur.execute(f"SELECT * FROM {table} {where_sql}", where_params)
        row = cur.fetchone()
        return row_to_dict(row) if row else None


async def delete(table: str, params: str) -> int:
    table = _safe_table(table)
    parsed = _parse_query(params)
    where_sql, where_params = _build_where(parsed["filters"])
    if not where_sql:
        # hard guard: no permitimos DELETE sin filtros
        raise ValueError("DELETE requiere filtros")
    sql = f"DELETE FROM {table} {where_sql}"
    with cursor() as cur:
        cur.execute(sql, where_params)
        return cur.rowcount


# ── RPCs ──

async def rpc(name: str, params: dict | None = None):
    params = params or {}
    if name == "generar_pagos_mes":
        mes = params.get("p_mes") or params.get("mes")
        if not mes:
            return 0
        with cursor() as cur:
            cur.execute(
                """
                INSERT OR IGNORE INTO pagos (alumno_id, mes, monto, pagado)
                SELECT id, ?, monto, 0 FROM alumnos WHERE estado = 'activo'
                """,
                [mes],
            )
            return cur.rowcount
    raise ValueError(f"RPC desconocida: {name}")
