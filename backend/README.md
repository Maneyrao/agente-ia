# AburridoNT API

Backend del agente IA para AburridoNT. Recibe mensajes de WhatsApp, los procesa con Claude, y responde automáticamente.

## Setup local

```bash
cd aburridont-api
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tus keys
uvicorn main:app --reload
```

## Endpoints

- `POST /api/agente/mensaje` — Enviar mensaje al agente
- `GET /api/agente/test` — Probar agente con mensaje de ejemplo
- `POST /api/webhooks/twilio` — Webhook para Twilio WhatsApp
- `GET/POST /api/webhooks/meta` — Webhook para Meta WhatsApp Business
- `GET /api/crm/contactos` — Listar contactos
- `GET /api/crm/dashboard` — Métricas del funnel

## Deploy en Railway

1. Push a GitHub
2. Railway → New Project → Deploy from GitHub
3. Variables de entorno: ver `.env.example`
