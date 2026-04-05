from fastapi import APIRouter, HTTPException
from app.models.schemas import DisponibilidadUpdate
from app.services.store import store

router = APIRouter()

@router.get("/{docente_id}")
def obtener_disponibilidad(docente_id: int):
    """Grilla completa: disponibilidad + grupos ocupando slots."""
    doc = store.get("docentes", docente_id)
    if not doc: raise HTTPException(404)

    disp = store.get_disponibilidad(docente_id)
    grupos = [g for g in store.get_all("grupos") if g.get("docente_id") == docente_id and g.get("activo")]

    # Build occupied map
    occupied = {}
    for g in grupos:
        for s in g.get("slots", []):
            key = f"{s['dia']}|{s['hora']}"
            alumnos = store.filter("alumnos", grupo_id=g["id"], estado="activo")
            occupied[key] = {
                "grupo_id": g["id"],
                "grupo_nombre": g["nombre"],
                "nivel": g["nivel"],
                "alumnos": len(alumnos),
                "capacidad": g["capacidad_max"],
            }

    # Count
    total_disp = 0
    total_ocup = 0
    for dia, horas in disp.items() if disp else []:
        for hora, avail in (horas.items() if isinstance(horas, dict) else []):
            if avail:
                key = f"{dia}|{hora}"
                if key in occupied:
                    total_ocup += 1
                else:
                    total_disp += 1

    return {
        "docente_id": docente_id,
        "docente_nombre": doc["nombre"],
        "disponibilidad": disp,
        "ocupados": occupied,
        "horas_ocupadas": total_ocup,
        "horas_disponibles": total_disp,
    }

@router.put("/{docente_id}")
def actualizar_disponibilidad(docente_id: int, data: DisponibilidadUpdate):
    """Actualizar disponibilidad de un docente."""
    doc = store.get("docentes", docente_id)
    if not doc: raise HTTPException(404)

    current = store.get_disponibilidad(docente_id) or {}
    for slot in data.slots:
        if slot.dia not in current:
            current[slot.dia] = {}
        current[slot.dia][slot.hora] = slot.disponible

    store.set_disponibilidad(docente_id, current)
    return {"ok": True, "docente_id": docente_id}

@router.get("/{docente_id}/potencial")
def potencial_revenue(docente_id: int):
    """Calcula el máximo ingreso potencial basado en horas libres."""
    doc = store.get("docentes", docente_id)
    if not doc: raise HTTPException(404)

    disp = store.get_disponibilidad(docente_id)
    grupos = [g for g in store.get_all("grupos") if g.get("docente_id") == docente_id and g.get("activo")]

    occupied = set()
    for g in grupos:
        for s in g.get("slots", []):
            occupied.add(f"{s['dia']}|{s['hora']}")

    horas_libres = 0
    if disp:
        for dia, horas in disp.items():
            if isinstance(horas, dict):
                for hora, avail in horas.items():
                    if avail and f"{dia}|{hora}" not in occupied:
                        horas_libres += 1

    # Max tarifa for this docente
    tarifas = doc.get("tarifas", [])
    max_tarifa = max((t["valor_hora"] for t in tarifas), default=0)

    max_alumnos_por_hora = 4
    precio_promedio = 80000  # por alumno/mes
    semanas = 4.33

    costo_docente_mensual = horas_libres * max_tarifa * semanas
    max_alumnos_total = horas_libres * max_alumnos_por_hora
    ingreso_potencial = max_alumnos_total * precio_promedio / semanas

    return {
        "docente_id": docente_id,
        "horas_libres_semanales": horas_libres,
        "max_tarifa_hora": max_tarifa,
        "costo_docente_mensual": round(costo_docente_mensual),
        "max_alumnos_nuevos": max_alumnos_total,
        "ingreso_potencial_mensual": round(ingreso_potencial),
        "ganancia_neta_potencial": round(ingreso_potencial - costo_docente_mensual),
    }
