"""
Servicio del Agente IA — Usa Claude API para responder consultas.
El agente tiene acceso a: horarios disponibles, niveles, precios, CRM.

Cuando se conecte Supabase, este servicio lee de la DB real.
"""
import os
import json
import httpx
from typing import Optional
from app.services.store import store


CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"

NIVELES = [
    "PRE A1 STARTER", "PRE A1 STARTER +", "A1 MOVERS", "A1 YOUNGEST",
    "A2 FLYERS", "A0", "A1", "A2", "B1", "B1 UPPER", "B2",
    "SPEAKING INICIAL", "SPEAKING INT", "SPEAKING AVANZADO", "TALLER"
]

SYSTEM_PROMPT = """Sos el asistente virtual de AburridoNT (@aburridont.clases), un instituto de inglés 100% virtual.

Tu rol: Atender consultas de potenciales alumnos, asesorar sobre cursos, y gestionar inscripciones.

INFORMACIÓN DEL INSTITUTO:
- Clases 100% virtuales, grupales (máx 4-5 alumnos) e individuales
- Niveles: {niveles}
- Precio grupal nuevos alumnos: $80.000–$85.000/mes (2hs semanales)
- Speaking Club (producto de entrada): $40.000–$50.000/mes
- Clases individuales: desde $90.000/mes

HORARIOS DISPONIBLES:
{horarios_disponibles}

INSTRUCCIONES:
1. Sé amable, cercano, y entusiasta pero profesional
2. Preguntá nombre y edad/nivel del alumno
3. Recomendá el nivel y horario apropiado
4. Si el contacto está interesado, pedí WhatsApp para coordinar
5. Siempre mencioná que las clases son virtuales por Zoom
6. Si no hay horario disponible, ofrecé lista de espera
7. Respondé en español rioplatense natural

Cuando necesites tomar una acción, incluí un JSON al final de tu respuesta con la estructura:
{{"accion": "clasificar_lead|inscribir|agendar_seguimiento", "datos": {{...}}}}

CONVERSACIÓN PREVIA:
{historial}
"""


def _build_horarios_text() -> str:
    """Construye texto de horarios disponibles desde el store."""
    docentes = store.get_all("docentes")
    grupos = store.get_all("grupos")
    lines = []

    for doc in docentes:
        if doc["id"] == 1:  # Thiago no se muestra
            continue
        disp = store.get_disponibilidad(doc["id"])
        grps = [g for g in grupos if g.get("docente_id") == doc["id"] and g.get("activo")]

        # Get occupied slots
        occupied = set()
        for g in grps:
            for s in g.get("slots", []):
                occupied.add(f"{s['dia']}|{s['hora']}")

        # Get available (not occupied)
        available = []
        if disp:
            for dia, horas in disp.items():
                for hora, is_avail in horas.items():
                    if is_avail and f"{dia}|{hora}" not in occupied:
                        available.append(f"  - {dia} {hora}")

        groups_text = "\n".join([
            f"  * {g['nombre']} ({g['nivel']}) — {', '.join(s['dia'][:3]+' '+s['hora'] for s in g.get('slots',[]))} — "
            f"{len(store.filter('alumnos', grupo_id=g['id'], estado='activo'))}/{g['capacidad_max']} alumnos"
            for g in grps
        ])

        lines.append(f"\n{doc['nombre']}:")
        if groups_text:
            lines.append(f"  Grupos actuales:\n{groups_text}")
        if available:
            lines.append(f"  Horarios libres:\n" + "\n".join(available[:10]))
        else:
            lines.append("  Sin horarios libres disponibles")

    return "\n".join(lines) if lines else "No hay horarios cargados aún."


def _get_historial(contact_id: int) -> str:
    """Obtiene historial de conversación de un contacto."""
    msgs = store.filter("mensajes", contact_id=contact_id)
    msgs.sort(key=lambda m: m.get("created_at", ""))
    lines = []
    for m in msgs[-10:]:  # Últimos 10 mensajes
        role = "Alumno" if m["role"] == "user" else "Asistente"
        lines.append(f"{role}: {m['mensaje']}")
    return "\n".join(lines) if lines else "Primera conversación."


async def procesar_mensaje(
    mensaje: str,
    canal: str,
    contacto_whatsapp: str = "",
    contacto_nombre: str = "",
) -> dict:
    """
    Procesa un mensaje entrante y genera respuesta del agente.
    Returns: {"respuesta": str, "accion": str|None, "datos": dict|None}
    """

    # 1. Buscar o crear contacto
    contactos = store.filter("contactos", whatsapp=contacto_whatsapp) if contacto_whatsapp else []
    if contactos:
        contacto = contactos[0]
    else:
        contacto = store.create("contactos", {
            "nombre": contacto_nombre or "Nuevo contacto",
            "whatsapp": contacto_whatsapp,
            "instagram": "",
            "canal": canal,
            "estado": "LEAD",
            "curso_interes": "",
            "motivo_no": "",
        })

    # 2. Guardar mensaje del usuario
    store.create("mensajes", {
        "contact_id": contacto["id"],
        "canal": canal,
        "role": "user",
        "mensaje": mensaje,
    })

    # 3. Build context
    horarios_text = _build_horarios_text()
    historial = _get_historial(contacto["id"])

    system = SYSTEM_PROMPT.format(
        niveles=", ".join(NIVELES),
        horarios_disponibles=horarios_text,
        historial=historial,
    )

    # 4. Call Claude API
    if not CLAUDE_API_KEY:
        respuesta = (
            "¡Hola! Gracias por escribirnos a AburridoNT 🎓\n\n"
            "Somos un instituto de inglés 100% virtual. "
            "¿Estás buscando clases para vos o para alguien más? "
            "Contame un poco y te asesoro."
        )
        accion = None
        datos = None
    else:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": CLAUDE_API_KEY,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": CLAUDE_MODEL,
                        "max_tokens": 1024,
                        "system": system,
                        "messages": [{"role": "user", "content": mensaje}],
                    },
                    timeout=30,
                )
                data = resp.json()
                raw = data["content"][0]["text"]

                # Extract action JSON if present
                respuesta = raw
                accion = None
                datos = None
                if '{"accion"' in raw:
                    try:
                        json_start = raw.rindex('{"accion"')
                        json_str = raw[json_start:]
                        parsed = json.loads(json_str)
                        accion = parsed.get("accion")
                        datos = parsed.get("datos")
                        respuesta = raw[:json_start].strip()
                    except (json.JSONDecodeError, ValueError):
                        pass

        except Exception as e:
            respuesta = f"Error al procesar: {str(e)}"
            accion = None
            datos = None

    # 5. Guardar respuesta
    store.create("mensajes", {
        "contact_id": contacto["id"],
        "canal": canal,
        "role": "assistant",
        "mensaje": respuesta,
    })

    # 6. Procesar acción si la hay
    if accion == "clasificar_lead" and datos:
        store.update("contactos", contacto["id"], {
            "estado": datos.get("estado", "CONSULTANDO"),
            "curso_interes": datos.get("curso_interes", ""),
        })
    elif accion == "inscribir" and datos:
        store.update("contactos", contacto["id"], {"estado": "INSCRIPTO"})
    elif accion == "agendar_seguimiento" and datos:
        store.create("seguimientos", {
            "contact_id": contacto["id"],
            "fecha_programada": datos.get("fecha", ""),
            "mensaje_sugerido": datos.get("mensaje", ""),
            "estado": "pendiente",
        })

    return {
        "respuesta": respuesta,
        "accion": accion,
        "datos": datos,
        "contacto_id": contacto["id"],
    }
