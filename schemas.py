"""Modelos Pydantic — Schemas para request/response"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# ═══ ENUMS ═══
class EstadoAlumno(str, Enum):
    activo = "activo"
    inactivo = "inactivo"

class EstadoContacto(str, Enum):
    lead = "LEAD"
    consultando = "CONSULTANDO"
    interesado = "INTERESADO"
    inscripto = "INSCRIPTO"
    no_por_ahora = "NO_POR_AHORA"

class Canal(str, Enum):
    whatsapp = "whatsapp"
    instagram = "instagram"
    landing = "landing"
    manual = "manual"

class EstadoSeguimiento(str, Enum):
    pendiente = "pendiente"
    enviado = "enviado"
    respondido = "respondido"
    cancelado = "cancelado"


# ═══ DOCENTES ═══
class TarifaTier(BaseModel):
    min_alumnos: int
    max_alumnos: int
    valor_hora: int

class DocenteBase(BaseModel):
    nombre: str
    tarifas: list[TarifaTier] = []

class DocenteCreate(DocenteBase):
    pass

class Docente(DocenteBase):
    id: int

class DisponibilidadSlot(BaseModel):
    dia: str
    hora: str
    disponible: bool

class DisponibilidadUpdate(BaseModel):
    docente_id: int
    slots: list[DisponibilidadSlot]


# ═══ GRUPOS ═══
class HorarioSlot(BaseModel):
    dia: str
    hora: str

class GrupoBase(BaseModel):
    nombre: str
    nivel: str
    docente_id: int
    slots: list[HorarioSlot] = []
    horas_semanales: float
    capacidad_max: int = 5

class GrupoCreate(GrupoBase):
    pass

class GrupoUpdate(BaseModel):
    nombre: Optional[str] = None
    nivel: Optional[str] = None
    docente_id: Optional[int] = None
    slots: Optional[list[HorarioSlot]] = None
    horas_semanales: Optional[float] = None
    capacidad_max: Optional[int] = None
    activo: Optional[bool] = None

class Grupo(GrupoBase):
    id: int
    activo: bool = True


# ═══ ALUMNOS ═══
class AlumnoBase(BaseModel):
    nombre: str
    apellido: str = ""
    whatsapp: str = ""
    nivel: str = "A1"
    docente_id: int
    grupo_id: Optional[int] = None
    monto: int
    horas_semanales: float = 2
    horario: str = ""

class AlumnoCreate(AlumnoBase):
    pass

class AlumnoUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    whatsapp: Optional[str] = None
    nivel: Optional[str] = None
    docente_id: Optional[int] = None
    grupo_id: Optional[int] = None
    monto: Optional[int] = None
    horas_semanales: Optional[float] = None
    horario: Optional[str] = None
    estado: Optional[EstadoAlumno] = None

class Alumno(AlumnoBase):
    id: int
    estado: EstadoAlumno = EstadoAlumno.activo
    canal_ingreso: Canal = Canal.manual
    created_at: Optional[datetime] = None


# ═══ CRM — CONTACTOS ═══
class ContactoBase(BaseModel):
    nombre: str
    whatsapp: str = ""
    instagram: str = ""
    canal: Canal = Canal.whatsapp
    curso_interes: str = ""

class ContactoCreate(ContactoBase):
    pass

class ContactoUpdate(BaseModel):
    estado: Optional[EstadoContacto] = None
    motivo_no: Optional[str] = None
    curso_interes: Optional[str] = None

class Contacto(ContactoBase):
    id: int
    estado: EstadoContacto = EstadoContacto.lead
    motivo_no: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ═══ CONVERSACIONES ═══
class MensajeBase(BaseModel):
    contact_id: int
    canal: Canal
    role: str  # "user" | "assistant"
    mensaje: str

class MensajeCreate(MensajeBase):
    pass

class Mensaje(MensajeBase):
    id: int
    created_at: Optional[datetime] = None


# ═══ SEGUIMIENTOS ═══
class SeguimientoBase(BaseModel):
    contact_id: int
    fecha_programada: datetime
    mensaje_sugerido: str = ""

class SeguimientoCreate(SeguimientoBase):
    pass

class Seguimiento(SeguimientoBase):
    id: int
    estado: EstadoSeguimiento = EstadoSeguimiento.pendiente


# ═══ AGENTE IA ═══
class AgenteRequest(BaseModel):
    mensaje: str
    canal: Canal = Canal.whatsapp
    contacto_whatsapp: str = ""
    contacto_nombre: str = ""

class AgenteResponse(BaseModel):
    respuesta: str
    accion: Optional[str] = None  # "inscribir", "agendar_seguimiento", "clasificar_lead", etc.
    datos: Optional[dict] = None
