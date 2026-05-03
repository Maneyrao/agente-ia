# AburridoNT — Guía de Setup Completo

## 1. Crear proyecto en Supabase (gratis)

1. Ir a **https://supabase.com** → Create New Project
2. Nombre: `aburridont`
3. Password: guardar en algún lado seguro
4. Region: **South America (São Paulo)** ← la más cercana a Argentina
5. Esperar ~2 minutos a que se cree

## 2. Ejecutar el Schema SQL

1. En Supabase Dashboard → **SQL Editor** → **New Query**
2. Copiar y pegar TODO el contenido de `supabase-schema.sql`
3. Click **Run** → debería mostrar "Success"
4. Después, crear otro query y pegar `supabase-seed.sql`
5. Click **Run** → carga los docentes, grupos, alumnos y pagos iniciales

## 3. Obtener las credenciales

En Supabase Dashboard → **Settings** → **API**:
- **Project URL**: `https://xxxxx.supabase.co` ← copiar
- **anon public key**: `eyJhbGci...` ← copiar (es la pública, no la secret)

## 4. Conectar el Panel React

En el panel, vas a necesitar instalar el cliente de Supabase:
```bash
npm install @supabase/supabase-js
```

Y crear un archivo `supabase.js`:
```javascript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://TU-PROYECTO.supabase.co'
const supabaseKey = 'TU-ANON-KEY'

export const supabase = createClient(supabaseUrl, supabaseKey)
```

## 5. Deploy del Panel (Frontend)

**Opción recomendada: Vercel (gratis)**
1. Subir el código del panel a un repo en GitHub
2. Ir a vercel.com → Import Project → seleccionar el repo
3. Framework: React (o Next.js si migramos)
4. Variables de entorno:
   - `VITE_SUPABASE_URL` = tu URL
   - `VITE_SUPABASE_KEY` = tu anon key
5. Deploy → te da un URL tipo `aburridont.vercel.app`

## 6. Deploy del Backend (API + Agente IA)

**Opción: Railway (~USD 5/mes)**
1. Subir la carpeta `backend/` a un repo en GitHub
2. Ir a railway.app → New Project → Deploy from GitHub
3. Variables de entorno:
   - `ANTHROPIC_API_KEY` = tu API key de Anthropic
   - `SUPABASE_URL` = tu URL
   - `SUPABASE_KEY` = tu service_role key (la secreta, no la pública)
4. Railway detecta Python automáticamente
5. Deploy → te da un URL tipo `aburridont-api.up.railway.app`

## 7. Conectar WhatsApp Business (Fase 2)

Para el agente de IA que responde mensajes:

### Opción A: Meta Business API (gratis pero complejo)
1. Crear cuenta en Meta Business Suite
2. Configurar WhatsApp Business API
3. Generar Access Token
4. Configurar webhook → apuntar a tu API: `https://tu-api.railway.app/api/agente/webhook`

### Opción B: Twilio (más fácil, ~USD 15/mes)
1. Crear cuenta en Twilio
2. Comprar número de WhatsApp (~USD 1/mes)
3. Configurar webhook → misma URL

### Opción C: Baileys (gratis, no oficial)
- Usa tu número personal de WhatsApp
- No requiere Meta Business
- Riesgo: pueden bannear el número
- Ideal para testear antes de invertir

---

## Arquitectura Final

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐
│   Panel Web  │────▶│   Supabase   │◀────│  Backend   │
│  (Vercel)    │     │  (Postgres)  │     │ (Railway)  │
│  React/Next  │     │  + Auth      │     │  FastAPI   │
└─────────────┘     └──────────────┘     └─────┬──────┘
                                               │
                                    ┌──────────┴──────────┐
                                    │                     │
                              ┌─────▼─────┐        ┌─────▼─────┐
                              │  Claude    │        │ WhatsApp  │
                              │  API       │        │ Business  │
                              │ (Agente)   │        │  API      │
                              └───────────┘        └───────────┘
```

**Flujo del agente:**
1. Lead manda mensaje por WhatsApp/Instagram
2. Webhook llega al Backend (Railway)
3. Backend consulta Supabase: horarios, grupos, disponibilidad
4. Backend arma prompt y manda a Claude API
5. Claude responde con texto + acción
6. Backend guarda conversación en Supabase + ejecuta acción
7. Respuesta vuelve al lead por WhatsApp

**Flujo del panel:**
1. Thiago abre el panel web (Vercel)
2. Panel lee/escribe directo a Supabase (sin pasar por backend)
3. Cambios en alumnos disparan triggers automáticos
4. Pagos, altas, bajas se registran con timestamps

---

## Mejoras que recomiendo (prioridad)

### Inmediatas (antes de lanzar el agente):
1. **Auth en Supabase** — Login con email para que solo vos accedas al panel
2. **Generar pagos automáticos** — Cron job que el 1ro de cada mes genera registros de pago para todos los activos
3. **Notificaciones de pago** — Alert cuando un alumno lleva 5+ días sin pagar

### Corto plazo (1-2 semanas):
4. **Dashboard financiero mejorado** — Gráficos de evolución mensual
5. **Exportar a Excel** — Botón para bajar listado de pagos del mes
6. **Landing page** — Formulario que crea un lead en el CRM automáticamente

### Mediano plazo (1 mes):
7. **Agente multi-canal** — WhatsApp + Instagram + landing, todos al mismo CRM
8. **Follow-up automático** — El agente recontacta leads no convertidos a los 3 y 7 días
9. **Nivel test** — El agente hace un mini test de nivel por chat y recomienda grupo

### Para escalar (2-3 meses):
10. **Portal de alumnos** — Login para que vean su horario y paguen online
11. **Reportes para profes** — Cada profesor ve su agenda y alumnos
12. **App mobile** — PWA del panel para gestionarlo desde el celular

---

## Costos mensuales estimados

| Servicio         | Costo          |
|-----------------|----------------|
| Supabase        | Gratis (Free)  |
| Vercel          | Gratis (Hobby) |
| Railway         | ~USD 5         |
| Claude API      | ~USD 10-20     |
| WhatsApp API    | USD 0-15       |
| **Total**       | **USD 15-40**  |

Con 100+ alumnos a $80k, esto es <0.5% de la facturación.
