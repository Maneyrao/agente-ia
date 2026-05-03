# AburridoNT — Contexto del proyecto

## Qué es

**AburridoNT** (`@aburridont.clases`) es un instituto de inglés 100% virtual. Este repo contiene:

1. Un **panel admin** (React/Vite) para gestionar docentes, grupos, alumnos, horarios, pagos y CRM.
2. Un **backend FastAPI** que expone un **agente IA** (Claude) para atender consultas de leads y un proxy de datos para el panel.
3. Un **schema SQLite local** (`db/schema.sql`) con seed de docentes/grupos/alumnos.

El agente fue diseñado **canal-agnóstico**: recibe `{mensaje, canal, contacto}` y devuelve `{respuesta, acción}`. La capa de canal (WhatsApp/Instagram/landing) se enchufa por encima.

## Estado actual (2026-05-03)

- **DB migrada de Supabase a SQLite local.** Un único archivo `db/aburridont.db` (gitignored). Sin servicios externos. Schema y seed se aplican automáticamente al primer arranque del backend.
- **Auth del panel removida.** El panel entra directo, sin login. Se eliminaron `Login`, `usuarios_panel` y la RPC `validar_login`.
- El backend expone los endpoints PostgREST-like (`/rest/v1/{table}`) que el panel ya consumía, así que la migración no requirió rediseñar el panel.
- Archivos viejos de Supabase movidos a `_legacy/` (`db/supabase-schema.sql`, `db/supabase-seed.sql`, `services/supabase.py`).
- WhatsApp/Twilio siguen fuera de scope.

## Stack

| Capa | Tecnología |
|---|---|
| Frontend | React 18 + Vite (sin TypeScript, JSX) |
| Backend | FastAPI 0.115 + Uvicorn + httpx + Pydantic v2 |
| LLM | Anthropic Claude — default `claude-sonnet-4-6` (override vía `CLAUDE_MODEL` env var) |
| DB | **SQLite local** — archivo `db/aburridont.db`, sin servidor |

## Estructura del repo

```
Aburridont Project/
├── backend/                     # FastAPI
│   ├── app/
│   │   ├── db.py                # conexión sqlite3 + auto-init schema/seed
│   │   ├── routers/
│   │   │   ├── agente.py        # POST /api/agente/mensaje, GET /test
│   │   │   ├── crm.py           # contactos, dashboard, métricas funnel
│   │   │   └── data.py          # /rest/v1/{table} estilo PostgREST (panel)
│   │   └── services/
│   │       ├── agente_service.py  # ⭐ corazón: prompt + Claude (tool-use nativo)
│   │       └── store.py           # query/insert/update/delete + RPC sobre SQLite
│   ├── main.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── .env.example
│   └── README.md
├── panel/                       # React + Vite
│   ├── src/
│   │   ├── App.jsx              # ⚠️ 50KB monolito (refactor pendiente)
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── db/
│   ├── schema.sql               # SQLite — tablas, triggers, índices
│   ├── seed.sql                 # docentes, grupos, alumnos, disponibilidad
│   └── aburridont.db            # archivo SQLite (gitignored, se regenera)
├── docs/
├── _legacy/                     # NO TOCAR (archivos Supabase, zips, etc.)
├── CLAUDE.md
├── README.md
├── .gitignore
└── .claudeignore
```

## Modelo de datos

Tablas SQLite (ver `db/schema.sql` para detalle):

- `docentes`, `tarifas`, `disponibilidad` — staff y precios escalonados.
- `grupos`, `grupo_horarios` — clases con docente, nivel, capacidad.
- `alumnos` — con grupo asignado o individuales.
- `pagos` — generados por trigger al alta de alumno o por RPC `generar_pagos_mes(p_mes)`.
- `movimientos` — auto-tracking de altas/bajas/reactivaciones por triggers.
- `snapshots_mensuales` — fotos de cierre de mes.
- `contactos` (CRM): `LEAD → CONSULTANDO → INTERESADO → INSCRIPTO | NO_POR_AHORA`.
- `mensajes` — historial conversacional del agente.
- `seguimientos` — re-engagement programado.

Booleanos se almacenan como INTEGER (0/1) y se serializan a JSON como `true`/`false` por el cliente DB (`db.py:BOOL_COLS`).

## Cómo correr local

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # poner ANTHROPIC_API_KEY
uvicorn main:app --reload  # http://localhost:8000
```
Al primer arranque crea `db/aburridont.db` con schema + seed.

### Panel
```bash
cd panel
npm install
cp .env.example .env       # ya viene con VITE_API_URL=http://localhost:8000
npm run dev                # http://localhost:5173
```

El panel le habla al backend por `VITE_API_URL`. Sin login: entra directo al dashboard.

## Niveles que maneja el instituto

`PRE A1 STARTER`, `PRE A1 STARTER +`, `A1 MOVERS`, `A1 YOUNGEST`, `A2 FLYERS`, `A0`, `A1`, `A2`, `B1`, `B1 UPPER`, `B2`, `SPEAKING INICIAL`, `SPEAKING INT`, `SPEAKING AVANZADO`, `TALLER`.

Precios actuales (resumen del system prompt):
- Grupal nuevo: $80.000–$85.000/mes (2hs/sem)
- Speaking Club (entrada): $40.000–$50.000/mes
- Individuales: desde $90.000/mes

## Convenciones

- **Idioma**: español rioplatense para respuestas al usuario; comentarios en español OK.
- **Modelo Claude**: default `claude-sonnet-4-6` (env `CLAUDE_MODEL` para override).
- **Tool-use**: agente usa tool-use nativo. Tools en `agente_service.TOOLS`: `clasificar_lead`, `inscribir`, `seguimiento`. Solo se ejecuta el primer `tool_use` por turno.
- **CORS**: backend lee `CORS_ORIGINS` (CSV). Default `localhost:5173`.
- **Acceso a tablas**: `store.py:ALLOWED_TABLES` controla qué tablas puede tocar el panel y los servicios. Si agregás una tabla, sumala ahí.

## TODOs conocidos

1. `App.jsx` es un monolito de ~50KB con identificadores de 1 letra. Refactor pendiente.
2. Soporte multi-tool por turno en el agente (hoy solo se ejecuta el primer `tool_use`).
3. `cerrar_mes` (snapshot mensual) no está implementado todavía como RPC en `store.py`. El panel no lo usa hoy — sumarlo si hace falta.

## Cosas que NO hacer

- **No** volver a Supabase ni a ninguna DB cloud.
- **No** modificar nada en `_legacy/`.
- **No** commitear `.env`, `db/aburridont.db`, ni la `ANTHROPIC_API_KEY`.
- **No** romper la separación canal-agnóstica del agente.
- **No** reintroducir login en el panel (el usuario lo quiere sin auth).

## Identidad del usuario

- Tomás (Thiago) Maneyro — fundador y dev. Espera respuestas concisas en español, sin sobreexplicar. Le gusta entender el "por qué" de cada decisión.
