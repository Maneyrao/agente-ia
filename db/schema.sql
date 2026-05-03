-- ══════════════════════════════════════════════════════════════
-- ABURRIDONT — Schema SQLite
-- DB local, sin servidor, archivo único: db/aburridont.db
-- ══════════════════════════════════════════════════════════════

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS docentes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  es_owner INTEGER DEFAULT 0,
  activo INTEGER DEFAULT 1,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tarifas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  docente_id INTEGER REFERENCES docentes(id) ON DELETE CASCADE,
  min_alumnos INTEGER NOT NULL,
  max_alumnos INTEGER NOT NULL,
  valor_hora INTEGER NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS disponibilidad (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  docente_id INTEGER REFERENCES docentes(id) ON DELETE CASCADE,
  dia TEXT NOT NULL CHECK (dia IN ('Lunes','Martes','Miércoles','Jueves','Viernes','Sábado')),
  hora TEXT NOT NULL,
  disponible INTEGER DEFAULT 1,
  UNIQUE(docente_id, dia, hora)
);

CREATE TABLE IF NOT EXISTS grupos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  nivel TEXT NOT NULL,
  docente_id INTEGER REFERENCES docentes(id),
  horas_semanales REAL NOT NULL DEFAULT 2,
  capacidad_max INTEGER NOT NULL DEFAULT 5,
  activo INTEGER DEFAULT 1,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS grupo_horarios (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  grupo_id INTEGER REFERENCES grupos(id) ON DELETE CASCADE,
  dia TEXT NOT NULL CHECK (dia IN ('Lunes','Martes','Miércoles','Jueves','Viernes','Sábado')),
  hora TEXT NOT NULL,
  UNIQUE(grupo_id, dia, hora)
);

CREATE TABLE IF NOT EXISTS alumnos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  apellido TEXT DEFAULT '',
  whatsapp TEXT DEFAULT '',
  nivel TEXT NOT NULL DEFAULT 'A1',
  docente_id INTEGER REFERENCES docentes(id),
  grupo_id INTEGER REFERENCES grupos(id) ON DELETE SET NULL,
  monto INTEGER NOT NULL DEFAULT 0,
  horas_semanales REAL DEFAULT 2,
  horario TEXT DEFAULT '',
  estado TEXT NOT NULL DEFAULT 'activo' CHECK (estado IN ('activo','inactivo')),
  canal_ingreso TEXT DEFAULT 'manual' CHECK (canal_ingreso IN ('whatsapp','instagram','landing','manual','referido')),
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pagos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  alumno_id INTEGER REFERENCES alumnos(id) ON DELETE CASCADE,
  mes TEXT NOT NULL,
  monto INTEGER NOT NULL,
  pagado INTEGER DEFAULT 0,
  fecha_pago TEXT,
  metodo TEXT DEFAULT '',
  notas TEXT DEFAULT '',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(alumno_id, mes)
);

CREATE TABLE IF NOT EXISTS movimientos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  alumno_id INTEGER REFERENCES alumnos(id) ON DELETE CASCADE,
  tipo TEXT NOT NULL CHECK (tipo IN ('alta','baja','reactivacion')),
  mes TEXT NOT NULL,
  nombre_alumno TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS snapshots_mensuales (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mes TEXT NOT NULL UNIQUE,
  alumnos_activos INTEGER,
  alumnos_nuevos INTEGER DEFAULT 0,
  bajas INTEGER DEFAULT 0,
  facturacion_bruta INTEGER,
  costo_docentes INTEGER,
  ganancia_neta INTEGER,
  pagaron INTEGER DEFAULT 0,
  no_pagaron INTEGER DEFAULT 0,
  detalle_docentes TEXT DEFAULT '[]',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contactos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  whatsapp TEXT DEFAULT '',
  instagram TEXT DEFAULT '',
  canal TEXT DEFAULT 'whatsapp' CHECK (canal IN ('whatsapp','instagram','landing','manual','test')),
  estado TEXT DEFAULT 'LEAD' CHECK (estado IN ('LEAD','CONSULTANDO','INTERESADO','INSCRIPTO','NO_POR_AHORA')),
  curso_interes TEXT DEFAULT '',
  motivo_no TEXT DEFAULT '',
  alumno_id INTEGER REFERENCES alumnos(id),
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mensajes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  contacto_id INTEGER REFERENCES contactos(id) ON DELETE CASCADE,
  canal TEXT DEFAULT 'whatsapp',
  role TEXT NOT NULL CHECK (role IN ('user','assistant','system')),
  mensaje TEXT NOT NULL,
  metadata TEXT DEFAULT '{}',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS seguimientos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  contacto_id INTEGER REFERENCES contactos(id) ON DELETE CASCADE,
  fecha_programada TEXT NOT NULL,
  mensaje_sugerido TEXT DEFAULT '',
  estado TEXT DEFAULT 'pendiente' CHECK (estado IN ('pendiente','enviado','respondido','cancelado')),
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- ══════════════════════════════════════════════════════════════
-- TRIGGERS
-- ══════════════════════════════════════════════════════════════

CREATE TRIGGER IF NOT EXISTS trg_alumno_alta
AFTER INSERT ON alumnos
WHEN NEW.estado = 'activo'
BEGIN
  INSERT INTO movimientos (alumno_id, tipo, mes, nombre_alumno)
  VALUES (NEW.id, 'alta', strftime('%Y-%m', 'now'),
          NEW.nombre || ' ' || COALESCE(NEW.apellido, ''));
  INSERT OR IGNORE INTO pagos (alumno_id, mes, monto, pagado)
  VALUES (NEW.id, strftime('%Y-%m', 'now'), NEW.monto, 0);
END;

CREATE TRIGGER IF NOT EXISTS trg_alumno_baja
AFTER UPDATE OF estado ON alumnos
WHEN OLD.estado != NEW.estado AND NEW.estado = 'inactivo'
BEGIN
  INSERT INTO movimientos (alumno_id, tipo, mes, nombre_alumno)
  VALUES (NEW.id, 'baja', strftime('%Y-%m', 'now'),
          NEW.nombre || ' ' || COALESCE(NEW.apellido, ''));
END;

CREATE TRIGGER IF NOT EXISTS trg_alumno_reactiva
AFTER UPDATE OF estado ON alumnos
WHEN OLD.estado = 'inactivo' AND NEW.estado = 'activo'
BEGIN
  INSERT INTO movimientos (alumno_id, tipo, mes, nombre_alumno)
  VALUES (NEW.id, 'reactivacion', strftime('%Y-%m', 'now'),
          NEW.nombre || ' ' || COALESCE(NEW.apellido, ''));
  INSERT OR IGNORE INTO pagos (alumno_id, mes, monto, pagado)
  VALUES (NEW.id, strftime('%Y-%m', 'now'), NEW.monto, 0);
END;

-- ══════════════════════════════════════════════════════════════
-- INDEXES
-- ══════════════════════════════════════════════════════════════

CREATE INDEX IF NOT EXISTS idx_alumnos_estado ON alumnos(estado);
CREATE INDEX IF NOT EXISTS idx_alumnos_docente ON alumnos(docente_id);
CREATE INDEX IF NOT EXISTS idx_alumnos_grupo ON alumnos(grupo_id);
CREATE INDEX IF NOT EXISTS idx_pagos_mes ON pagos(mes);
CREATE INDEX IF NOT EXISTS idx_pagos_alumno ON pagos(alumno_id);
CREATE INDEX IF NOT EXISTS idx_movimientos_mes ON movimientos(mes);
CREATE INDEX IF NOT EXISTS idx_contactos_estado ON contactos(estado);
CREATE INDEX IF NOT EXISTS idx_mensajes_contacto ON mensajes(contacto_id);
CREATE INDEX IF NOT EXISTS idx_grupo_horarios_grupo ON grupo_horarios(grupo_id);
CREATE INDEX IF NOT EXISTS idx_disponibilidad_docente ON disponibilidad(docente_id);
