USE hospital;

-- 1. Disponibilidades de Box
DELETE FROM DisponibilidadBox;
INSERT INTO DisponibilidadBox (disponibilidad) VALUES
  ('Libre'),
  ('Ocupado'),
  ('Inhabilitado');

-- 2. Tipos de Box
DELETE FROM TipoBox;
INSERT INTO TipoBox (tipoBox) VALUES
  ('General'),
  ('Especial');

-- 3. Especialidades
DELETE FROM Especialidad;
INSERT INTO Especialidad (nombreEspecialidad) VALUES
  ('Cardiología'),
  ('Neurología'),
  ('Pediatría');

-- 4. Jornadas
DELETE FROM Jornada;
INSERT INTO Jornada (jornadaInicio, jornadaFin) VALUES
  ('08:00:00','12:00:00'),
  ('13:00:00','17:00:00');

-- 5. Estados de Consulta
DELETE FROM EstadoConsulta;
INSERT INTO EstadoConsulta (estadoConsulta) VALUES
  ('Pendiente'),
  ('Confirmada'),
  ('Cancelada');

-- 6. Boxes de ejemplo
DELETE FROM Box;
INSERT INTO Box (idBox, numeroBox, idTipoBox, idDisponibilidadBox) VALUES
  (101, 101, 1, 1),
  (102, 102, 2, 1),
  (103, 103, 1, 2),
  (104, 104, 2, 3);

-- Ajusta el AUTO_INCREMENT para no chocar luego
ALTER TABLE Box AUTO_INCREMENT = 105;

-- 7. Médicos de ejemplo
DELETE FROM Medico;
INSERT INTO Medico (nombreCompleto, idEspecialidad, idJornada) VALUES
  ('Dr. Juan Pérez',      1, 1),
  ('Dra. María Soto',      2, 2),
  ('Dr. Pablo González',   3, 1);

-- 8. Consultas de ejemplo
DELETE FROM Consulta;
INSERT INTO Consulta (idBox, idMedico, idEstadoConsulta, fechaHoraInicio, fechaHoraFin) VALUES
  (101, 1, 1, '2025-05-16 09:00:00', '2025-05-16 09:30:00'),
  (102, 2, 2, '2025-05-16 10:00:00', '2025-05-16 10:45:00'),
  (103, 3, 3, '2025-05-16 11:00:00', '2025-05-16 11:30:00');
