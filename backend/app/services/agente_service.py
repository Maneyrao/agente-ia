"""
Servicio del Agente IA.
Recibe mensaje → arma contexto desde Supabase → llama a Claude → responde.

Las acciones (clasificar_lead, inscribir, seguimiento) se ejecutan vía
tool-use nativo de la API de Anthropic, no parseando texto del modelo.
"""
import os
import httpx
from app.services.store import query, insert, update

CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")

# Definición de herramientas que el agente puede invocar.
# El modelo decide cuándo usarlas; nosotros las ejecutamos contra Supabase.
TOOLS = [
    {
        "name": "clasificar_lead",
        "description": (
            "Actualiza el estado del contacto en el funnel CRM. "
            "Usar cuando detectes interés, dudas, o decisión del lead. "
            "estado: LEAD (recién llega) → CONSULTANDO (hace preguntas) → "
            "INTERESADO (quiere inscribirse) → NO_POR_AHORA (rechaza)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "estado": {
                    "type": "string",
                    "enum": [
                        "LEAD",
                        "CONSULTANDO",
                        "INTERESADO",
                        "NO_POR_AHORA",
                    ],
                },
                "curso_interes": {
                    "type": "string",
                    "description": "Nivel/curso que le interesa (ej: A1, Speaking Int).",
                },
            },
            "required": ["estado"],
        },
    },
    {
        "name": "inscribir",
        "description": (
            "Marca al contacto como INSCRIPTO. Usar SOLO cuando el alumno "
            "confirmó explícitamente que se quiere inscribir en un curso/horario."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "curso": {"type": "string", "description": "Curso/grupo confirmado."},
                "horario": {"type": "string", "description": "Día y hora confirmados."},
            },
            "required": [],
        },
    },
    {
        "name": "seguimiento",
        "description": (
            "Programa un re-engagement para más adelante (lead tibio que "
            "pidió tiempo, o que dejó de responder). Usar cuando convenga "
            "volver a contactar en X días."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "fecha": {
                    "type": "string",
                    "description": "Fecha programada en formato ISO (YYYY-MM-DD o ISO 8601 completo).",
                },
                "mensaje": {
                    "type": "string",
                    "description": "Mensaje sugerido para el re-contacto.",
                },
            },
            "required": ["fecha", "mensaje"],
        },
    },
]

NIVELES = [
    "PRE A1 STARTER", "PRE A1 STARTER +", "A1 MOVERS", "A1 YOUNGEST",
    "A2 FLYERS", "A0", "A1", "A2", "B1", "B1 UPPER", "B2",
    "SPEAKING INICIAL", "SPEAKING INT", "SPEAKING AVANZADO", "TALLER",
]

SYSTEM_PROMPT = """Sos el asistente virtual de AburridoNT (@aburridont.clases), un instituto de inglés 100% virtual.

Tu rol: Atender consultas de potenciales alumnos, asesorar sobre cursos, y gestionar inscripciones.

INFORMACIÓN DEL INSTITUTO:
- Clases 100% virtuales por Zoom, grupales (máx 4 alumnos) e individuales
- Niveles disponibles: {niveles}
- Precio grupal nuevos: $80.000–$85.000/mes (2hs semanales)
- Speaking Club (entrada): $40.000–$50.000/mes
- Individuales: desde $90.000/mes

HORARIOS DISPONIBLES:
{horarios}

INSTRUCCIONES:
1. Sé amable, cercano, usá español rioplatense natural
2. Preguntá nombre y edad/nivel del alumno
3. Recomendá nivel y horario apropiado según disponibilidad
4. Si está interesado, pedí WhatsApp para coordinar
5. Si no hay horario, ofrecé lista de espera
6. No inventes horarios que no están en la lista

ACCIONES (tools): tenés tres tools disponibles — clasificar_lead, inscribir, seguimiento.
Usalas cuando el contexto lo justifique. No anuncies que las usás; ejecutá la tool
y respondé al usuario con lenguaje natural.

HISTORIAL:
{historial}"""


async def _build_horarios() -> str:
    """Construye texto de horarios desde Supabase."""
    docentes = await query("docentes", "?es_owner=eq.false&activo=eq.true&order=id")
    grupos = await query("grupos", "?activo=eq.true&order=id")
    horarios = await query("grupo_horarios", "?order=grupo_id")
    alumnos = await query("alumnos", "?estado=eq.activo&order=id")
    disponibilidad = await query("disponibilidad", "?disponible=eq.true&order=docente_id")

    lines = []
    for doc in docentes:
        did = doc["id"]
        doc_grupos = [g for g in grupos if g["docente_id"] == did]

        # Occupied slots
        occupied = set()
        for g in doc_grupos:
            g_horarios = [h for h in horarios if h["grupo_id"] == g["id"]]
            for h in g_horarios:
                occupied.add(f"{h['dia']}|{h['hora']}")

        # Available slots
        doc_disp = [d for d in disponibilidad if d["docente_id"] == did]
        available = []
        for d in doc_disp:
            key = f"{d['dia']}|{d['hora']}"
            if key not in occupied:
                available.append(f"  - {d['dia']} {d['hora']}")

        # Groups info
        groups_text = []
        for g in doc_grupos:
            g_horarios = [h for h in horarios if h["grupo_id"] == g["id"]]
            g_alumnos = [a for a in alumnos if a.get("grupo_id") == g["id"]]
            slots_str = ", ".join(
                f"{h['dia'][:3]} {h['hora']}" for h in g_horarios
            )
            groups_text.append(
                f"  * {g['nombre']} ({g['nivel']}) — {slots_str} — "
                f"{len(g_alumnos)}/{g['capacidad_max']} alumnos"
            )

        lines.append(f"\n{doc['nombre']}:")
        if groups_text:
            lines.append("  Grupos:\n" + "\n".join(groups_text))
        if available:
            lines.append(
                "  Horarios libres:\n" + "\n".join(available[:12])
            )
        else:
            lines.append("  Sin horarios libres")

    return "\n".join(lines) if lines else "No hay horarios cargados."


async def _get_historial(contact_id: int) -> str:
    """Últimos mensajes de un contacto."""
    msgs = await query(
        "mensajes",
        f"?contacto_id=eq.{contact_id}&order=created_at.desc&limit=10",
    )
    msgs.reverse()
    lines = []
    for m in msgs:
        role = "Alumno" if m["role"] == "user" else "Asistente"
        lines.append(f"{role}: {m['mensaje']}")
    return "\n".join(lines) if lines else "Primera conversación."


async def procesar_mensaje(
    mensaje: str,
    canal: str = "whatsapp",
    contacto_whatsapp: str = "",
    contacto_nombre: str = "",
) -> dict:
    """Procesa un mensaje y genera respuesta."""

    # 1. Find or create contact
    contactos = []
    if contacto_whatsapp:
        contactos = await query(
            "contactos", f"?whatsapp=eq.{contacto_whatsapp}"
        )

    if contactos:
        contacto = contactos[0]
    else:
        contacto = await insert("contactos", {
            "nombre": contacto_nombre or "Nuevo contacto",
            "whatsapp": contacto_whatsapp,
            "canal": canal,
            "estado": "LEAD",
        })

    if not contacto:
        return {"respuesta": "Error interno", "accion": None, "datos": None}

    cid = contacto["id"]

    # 2. Save user message
    await insert("mensajes", {
        "contacto_id": cid,
        "canal": canal,
        "role": "user",
        "mensaje": mensaje,
    })

    # 3. Build context
    horarios = await _build_horarios()
    historial = await _get_historial(cid)

    system = SYSTEM_PROMPT.format(
        niveles=", ".join(NIVELES),
        horarios=horarios,
        historial=historial,
    )

    # 4. Call Claude (con tool-use nativo)
    respuesta = ""
    accion = None
    datos = None

    if not CLAUDE_API_KEY:
        respuesta = (
            "¡Hola! Gracias por escribir a AburridoNT 🎓\n"
            "Somos un instituto de inglés 100% virtual. "
            "¿Buscás clases para vos o para alguien más?"
        )
    else:
        try:
            async with httpx.AsyncClient(timeout=30) as client:
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
                        "tools": TOOLS,
                        "messages": [{"role": "user", "content": mensaje}],
                    },
                )
                data = resp.json()
                # content es lista de bloques: text | tool_use
                texto_blocks = []
                for block in data.get("content", []):
                    btype = block.get("type")
                    if btype == "text":
                        texto_blocks.append(block.get("text", ""))
                    elif btype == "tool_use" and accion is None:
                        # primera tool_use gana — no soportamos múltiples por turno
                        accion = block.get("name")
                        datos = block.get("input") or {}
                respuesta = "\n".join(t.strip() for t in texto_blocks if t).strip()
                if not respuesta and accion:
                    # el modelo invocó tool sin texto; damos un fallback amable
                    respuesta = "Listo, te confirmo en un momento."
        except Exception:
            respuesta = "Disculpá, hubo un error. ¿Podés repetir tu consulta?"

    # 5. Save response
    await insert("mensajes", {
        "contacto_id": cid,
        "canal": canal,
        "role": "assistant",
        "mensaje": respuesta,
    })

    # 6. Process action (tool_use)
    if accion == "clasificar_lead":
        patch = {"estado": (datos or {}).get("estado", "CONSULTANDO")}
        if (datos or {}).get("curso_interes"):
            patch["curso_interes"] = datos["curso_interes"]
        await update("contactos", f"?id=eq.{cid}", patch)
    elif accion == "inscribir":
        patch = {"estado": "INSCRIPTO"}
        if (datos or {}).get("curso"):
            patch["curso_interes"] = datos["curso"]
        await update("contactos", f"?id=eq.{cid}", patch)
    elif accion == "seguimiento" and datos and datos.get("fecha"):
        await insert("seguimientos", {
            "contacto_id": cid,
            "fecha_programada": datos["fecha"],
            "mensaje_sugerido": datos.get("mensaje", ""),
            "estado": "pendiente",
        })

    return {
        "respuesta": respuesta,
        "accion": accion,
        "datos": datos,
        "contacto_id": cid,
    }
