"""
Conexión a SQLite local. Inicializa el archivo en el primer arranque
ejecutando db/schema.sql; aplica db/seed.sql sólo si la tabla docentes
está vacía.
"""
import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = Path(os.getenv("DB_PATH", ROOT / "db" / "aburridont.db"))
SCHEMA_PATH = ROOT / "db" / "schema.sql"
SEED_PATH = ROOT / "db" / "seed.sql"

# Columnas booleanas — se serializan como bool en JSON.
BOOL_COLS = {"es_owner", "activo", "disponible", "pagado"}


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


_conn: sqlite3.Connection | None = None


def get_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = _connect()
        init_db(_conn)
    return _conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    cur = conn.execute("SELECT count(*) AS n FROM docentes")
    if cur.fetchone()["n"] == 0 and SEED_PATH.exists():
        conn.executescript(SEED_PATH.read_text(encoding="utf-8"))
    conn.commit()


@contextmanager
def cursor():
    conn = get_conn()
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()


def row_to_dict(row: sqlite3.Row) -> dict:
    """Convierte sqlite3.Row a dict y normaliza booleanos."""
    d = dict(row)
    for k, v in list(d.items()):
        if k in BOOL_COLS and isinstance(v, int):
            d[k] = bool(v)
    return d
