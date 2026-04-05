from fastapi import APIRouter
from app.models.schemas import AgenteRequest, AgenteResponse
from app.services.agente_service import procesar_mensaje

router = APIRouter()

@router.post("/mensaje", response_model=AgenteResponse)
async def enviar_mensaje(data: AgenteRequest):
    """
    Endpoint principal del agente IA.
    Recibe mensaje de WhatsApp/Instagram/Landing y responde.
    """
    result = await procesar_mensaje(
        mensaje=data.mensaje,
        canal=data.canal.value,
        contacto_whatsapp=data.contacto_whatsapp,
        contacto_nombre=data.contacto_nombre,
    )
    return AgenteResponse(
        respuesta=result["respuesta"],
        accion=result.get("accion"),
        datos=result.get("datos"),
    )

@router.get("/test")
async def test_agente():
    """Test rápido del agente con un mensaje de prueba."""
    result = await procesar_mensaje(
        mensaje="Hola, quiero info sobre clases de inglés para mi hijo de 10 años",
        canal="whatsapp",
        contacto_whatsapp="+5411999999",
        contacto_nombre="Test User",
    )
    return result
