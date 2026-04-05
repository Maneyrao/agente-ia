"""
Store en memoria — Reemplazado por Supabase cuando se conecte.
Simula las operaciones CRUD que después van a la DB.
"""
from datetime import datetime
from typing import Optional


class InMemoryStore:
    """Almacenamiento temporal en memoria. Cada tabla es un dict {id: record}."""

    def __init__(self):
        self._id_counters = {}
        self.tables = {
            "docentes": {},
            "grupos": {},
            "alumnos": {},
            "disponibilidad": {},  # {docente_id: {dia: {hora: bool}}}
            "contactos": {},
            "mensajes": {},
            "seguimientos": {},
        }
        self._seed()

    def _next_id(self, table: str) -> int:
        self._id_counters[table] = self._id_counters.get(table, 0) + 1
        return self._id_counters[table]

    # ── Generic CRUD ──
    def get_all(self, table: str) -> list[dict]:
        return list(self.tables[table].values())

    def get(self, table: str, id: int) -> Optional[dict]:
        return self.tables[table].get(id)

    def create(self, table: str, data: dict) -> dict:
        id = self._next_id(table)
        data["id"] = id
        data["created_at"] = datetime.utcnow().isoformat()
        self.tables[table][id] = data
        return data

    def update(self, table: str, id: int, data: dict) -> Optional[dict]:
        if id not in self.tables[table]:
            return None
        record = self.tables[table][id]
        for k, v in data.items():
            if v is not None:
                record[k] = v
        record["updated_at"] = datetime.utcnow().isoformat()
        self.tables[table][id] = record
        return record

    def delete(self, table: str, id: int) -> bool:
        if id in self.tables[table]:
            del self.tables[table][id]
            return True
        return False

    def filter(self, table: str, **kwargs) -> list[dict]:
        results = []
        for record in self.tables[table].values():
            match = all(record.get(k) == v for k, v in kwargs.items())
            if match:
                results.append(record)
        return results

    # ── Disponibilidad (estructura especial) ──
    def get_disponibilidad(self, docente_id: int) -> dict:
        return self.tables["disponibilidad"].get(docente_id, {})

    def set_disponibilidad(self, docente_id: int, data: dict):
        self.tables["disponibilidad"][docente_id] = data

    # ── Seed data ──
    def _seed(self):
        # Docentes
        for d in [
            {"nombre": "Thiago", "tarifas": []},
            {"nombre": "Gianella", "tarifas": [
                {"min_alumnos": 1, "max_alumnos": 2, "valor_hora": 7500},
                {"min_alumnos": 3, "max_alumnos": 5, "valor_hora": 10000},
                {"min_alumnos": 6, "max_alumnos": 99, "valor_hora": 12000},
            ]},
            {"nombre": "Nacho", "tarifas": [
                {"min_alumnos": 1, "max_alumnos": 1, "valor_hora": 6000},
                {"min_alumnos": 2, "max_alumnos": 2, "valor_hora": 7500},
                {"min_alumnos": 3, "max_alumnos": 99, "valor_hora": 8200},
            ]},
            {"nombre": "Morena", "tarifas": [
                {"min_alumnos": 1, "max_alumnos": 1, "valor_hora": 5000},
                {"min_alumnos": 2, "max_alumnos": 2, "valor_hora": 6000},
                {"min_alumnos": 3, "max_alumnos": 99, "valor_hora": 8500},
            ]},
        ]:
            self.create("docentes", d)

        # Grupos
        for g in [
            {"nombre": "A2 FLYERS", "nivel": "A2 FLYERS", "docente_id": 2, "slots": [{"dia": "Martes", "hora": "18:00"}, {"dia": "Jueves", "hora": "18:00"}], "horas_semanales": 4, "capacidad_max": 5, "activo": True},
            {"nombre": "A0", "nivel": "A0", "docente_id": 2, "slots": [{"dia": "Martes", "hora": "20:00"}, {"dia": "Jueves", "hora": "20:00"}], "horas_semanales": 4, "capacidad_max": 5, "activo": True},
            {"nombre": "A1 SAB", "nivel": "A1", "docente_id": 2, "slots": [{"dia": "Sábado", "hora": "11:00"}, {"dia": "Sábado", "hora": "12:00"}], "horas_semanales": 2, "capacidad_max": 6, "activo": True},
            {"nombre": "A1 MAR JUE", "nivel": "A1", "docente_id": 2, "slots": [{"dia": "Martes", "hora": "19:00"}, {"dia": "Jueves", "hora": "19:00"}], "horas_semanales": 4, "capacidad_max": 5, "activo": True},
        ]:
            self.create("grupos", g)

        self._id_counters["docentes"] = 4
        self._id_counters["grupos"] = 8


# Singleton
store = InMemoryStore()
