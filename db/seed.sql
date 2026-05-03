-- ══════════════════════════════════════════════════════════════
-- ABURRIDONT — Seed inicial (SQLite)
-- Se ejecuta sólo si las tablas están vacías.
-- ══════════════════════════════════════════════════════════════

-- DOCENTES
INSERT INTO docentes (nombre, es_owner) VALUES ('Thiago', 1);
INSERT INTO docentes (nombre, es_owner) VALUES ('Gianella', 0);
INSERT INTO docentes (nombre, es_owner) VALUES ('Nacho', 0);
INSERT INTO docentes (nombre, es_owner) VALUES ('Morena', 0);

-- TARIFAS
INSERT INTO tarifas (docente_id, min_alumnos, max_alumnos, valor_hora) VALUES (2, 1, 2, 7500);
INSERT INTO tarifas (docente_id, min_alumnos, max_alumnos, valor_hora) VALUES (2, 3, 5, 10000);
INSERT INTO tarifas (docente_id, min_alumnos, max_alumnos, valor_hora) VALUES (2, 6, 99, 12000);
INSERT INTO tarifas (docente_id, min_alumnos, max_alumnos, valor_hora) VALUES (3, 1, 1, 6000);
INSERT INTO tarifas (docente_id, min_alumnos, max_alumnos, valor_hora) VALUES (3, 2, 2, 7500);
INSERT INTO tarifas (docente_id, min_alumnos, max_alumnos, valor_hora) VALUES (3, 3, 99, 8200);
INSERT INTO tarifas (docente_id, min_alumnos, max_alumnos, valor_hora) VALUES (4, 1, 1, 5000);
INSERT INTO tarifas (docente_id, min_alumnos, max_alumnos, valor_hora) VALUES (4, 2, 2, 6000);
INSERT INTO tarifas (docente_id, min_alumnos, max_alumnos, valor_hora) VALUES (4, 3, 99, 8500);

-- DISPONIBILIDAD Gianella (id=2)
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Martes', '15:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Martes', '16:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Martes', '17:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Martes', '18:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Martes', '19:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Martes', '20:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Jueves', '15:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Jueves', '16:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Jueves', '17:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Jueves', '18:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Jueves', '19:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Jueves', '20:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Viernes', '16:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Viernes', '17:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Viernes', '18:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Viernes', '19:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Viernes', '20:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Sábado', '9:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Sábado', '10:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Sábado', '11:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Sábado', '12:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Sábado', '13:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (2, 'Sábado', '14:00');

-- DISPONIBILIDAD Nacho (id=3)
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Martes', '9:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Martes', '10:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Martes', '11:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Martes', '12:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Martes', '13:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Martes', '14:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Martes', '15:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Miércoles', '9:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Miércoles', '10:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Miércoles', '11:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Miércoles', '12:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Miércoles', '13:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Miércoles', '14:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Miércoles', '15:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Viernes', '9:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Viernes', '10:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Viernes', '11:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Viernes', '12:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Viernes', '13:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Viernes', '14:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Viernes', '15:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Viernes', '16:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Viernes', '17:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Viernes', '18:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Viernes', '19:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Viernes', '20:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Sábado', '9:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Sábado', '10:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Sábado', '17:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Sábado', '18:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Sábado', '19:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (3, 'Sábado', '20:00');

-- DISPONIBILIDAD Morena (id=4)
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Lunes', '17:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Lunes', '18:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Lunes', '19:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Lunes', '20:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Martes', '17:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Martes', '18:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Martes', '19:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Martes', '20:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Miércoles', '17:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Miércoles', '18:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Miércoles', '19:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Miércoles', '20:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Jueves', '17:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Jueves', '18:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Jueves', '19:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Jueves', '20:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Viernes', '17:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Viernes', '18:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Viernes', '19:00');
INSERT INTO disponibilidad (docente_id, dia, hora) VALUES (4, 'Viernes', '20:00');

-- GRUPOS
INSERT INTO grupos (nombre, nivel, docente_id, horas_semanales, capacidad_max) VALUES ('A2 FLYERS', 'A2 FLYERS', 2, 4, 5);
INSERT INTO grupos (nombre, nivel, docente_id, horas_semanales, capacidad_max) VALUES ('A0', 'A0', 2, 4, 5);
INSERT INTO grupos (nombre, nivel, docente_id, horas_semanales, capacidad_max) VALUES ('A1 SAB', 'A1', 2, 2, 6);
INSERT INTO grupos (nombre, nivel, docente_id, horas_semanales, capacidad_max) VALUES ('A1 MAR JUE', 'A1', 2, 4, 5);
INSERT INTO grupos (nombre, nivel, docente_id, horas_semanales, capacidad_max) VALUES ('SPK SAB', 'SPEAKING INICIAL', 3, 1, 5);
INSERT INTO grupos (nombre, nivel, docente_id, horas_semanales, capacidad_max) VALUES ('SPK V-S', 'SPEAKING INICIAL', 3, 2, 5);
INSERT INTO grupos (nombre, nivel, docente_id, horas_semanales, capacidad_max) VALUES ('A2 IND Her', 'A2', 3, 1, 1);
INSERT INTO grupos (nombre, nivel, docente_id, horas_semanales, capacidad_max) VALUES ('A1 IND Damian', 'A1', 3, 1, 1);

-- HORARIOS DE GRUPO
INSERT INTO grupo_horarios (grupo_id, dia, hora) VALUES (1, 'Martes', '18:00');
INSERT INTO grupo_horarios (grupo_id, dia, hora) VALUES (1, 'Jueves', '18:00');
INSERT INTO grupo_horarios (grupo_id, dia, hora) VALUES (2, 'Martes', '20:00');
INSERT INTO grupo_horarios (grupo_id, dia, hora) VALUES (2, 'Jueves', '20:00');
INSERT INTO grupo_horarios (grupo_id, dia, hora) VALUES (3, 'Sábado', '11:00');
INSERT INTO grupo_horarios (grupo_id, dia, hora) VALUES (3, 'Sábado', '12:00');
INSERT INTO grupo_horarios (grupo_id, dia, hora) VALUES (4, 'Martes', '19:00');
INSERT INTO grupo_horarios (grupo_id, dia, hora) VALUES (4, 'Jueves', '19:00');
INSERT INTO grupo_horarios (grupo_id, dia, hora) VALUES (5, 'Sábado', '10:00');
INSERT INTO grupo_horarios (grupo_id, dia, hora) VALUES (6, 'Viernes', '17:00');
INSERT INTO grupo_horarios (grupo_id, dia, hora) VALUES (6, 'Sábado', '9:00');
INSERT INTO grupo_horarios (grupo_id, dia, hora) VALUES (7, 'Viernes', '18:00');
INSERT INTO grupo_horarios (grupo_id, dia, hora) VALUES (8, 'Martes', '9:00');

-- ALUMNOS (con grupo)
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Valentina','Rojas','A2 FLYERS',2,1,60000,4,'Mar Jue 18:00');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Frida Ambar','Azambulla','A2 FLYERS',2,1,60000,4,'Mar Jue 18:00');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Isabella','Raspuntin','A2 FLYERS',2,1,60000,4,'Mar Jue 18:00');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Zoe','Velasquez','A0',2,2,60000,4,'Mar Jue 20:00');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Benjamín','Mira','A0',2,2,50000,4,'Mar Jue 20:00');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Florencia','Vazquez','A1',2,3,50000,2,'Sab 11-13');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Kevin','Benítez','A1',2,3,50000,2,'Sab 11-13');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Maria Fernanda','Colfer','A1',2,3,55000,2,'Sab 11-13');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Lucia','Vazquez','A1',2,3,60000,2,'Sab 11-13');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Alexia Belen','Diaz','A1',2,4,60000,4,'Mar Jue 19:00');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Julia','Del Valle Guzmán','A1',2,4,55000,4,'Mar Jue 19:00');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Antonio David','Re','A1',2,4,50000,4,'Mar Jue 19:00');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Desiree','Velasquez','A1',2,4,60000,4,'Mar Jue 19:00');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Angelica Ruth','Arancibia','SPEAKING INICIAL',3,5,36000,1,'Sab 10:00');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Daniela Sofia','Bonetti Kunt','SPEAKING INICIAL',3,6,60000,2,'Vie Sab');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Her','','A2',3,7,48000,1,'Vie 18:00');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, grupo_id, monto, horas_semanales, horario) VALUES ('Damian Leandro','Frutos','A1',3,8,52000,1,'Mar 9:00');

-- ALUMNOS individuales con Thiago (id=1)
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Melissa','Algieri','A1',1,55000,4,'Mar Jue 20:00');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Sofi','Ferreyra','A2',1,50000,4,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Sofia','Roberts','A2',1,90000,4,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Marcelo','Sotto','A1',1,45000,1,'Mie 18:00');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Florencia','Abagnale','B1',1,88000,4,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Juan Pablo','Moir','B1',1,75000,2,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Sebastián','','A1',1,52000,1,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Valentin','Bramson','A1',1,60000,2,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Lila','Bramson','B1',1,60000,2,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Esteban','Barone','B1 UPPER',1,135000,6,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Victor','','B1',1,129000,4,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Rafaela','Paulette','B1',1,100000,4,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Asane','Diop','A1',1,55000,2,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Soledad','Boytenko','A1',1,52000,1,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Kevin','','A2',1,52000,2,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Alan','Sbaglia','B1',1,94000,4,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Cristian Daniel','Ance','A2',1,52000,1,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Ariel','D','B1',1,88000,4,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Ezequiel','Rango','A2',1,55000,4,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Mora','Puntin','A1',1,60000,2,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Cami','','A1',1,60000,1,'');
INSERT INTO alumnos (nombre, apellido, nivel, docente_id, monto, horas_semanales, horario) VALUES ('Mariano','Flores Zarate','A1',1,45000,1,'');
