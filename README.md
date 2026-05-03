# AburridoNT

Panel admin + agente IA (Claude) para el instituto de inglés AburridoNT (`@aburridont.clases`). DB local en SQLite — sin servicios externos salvo la API de Anthropic.

## Estructura

- `backend/` — FastAPI con agente Claude + capa de datos SQLite
- `panel/` — React/Vite (admin, sin login)
- `db/` — schema y seed SQLite (`aburridont.db` se crea al primer arranque)
- `docs/` — guías y notas
- `CLAUDE.md` — contexto del proyecto para Claude Code

## Quickstart

```bash
# Backend (crea db/aburridont.db con seed al primer arranque)
cd backend && pip install -r requirements.txt && cp .env.example .env
# editar .env y pegar ANTHROPIC_API_KEY
uvicorn main:app --reload      # http://localhost:8000

# Panel (entra directo, sin login)
cd panel && npm install && cp .env.example .env && npm run dev
```
