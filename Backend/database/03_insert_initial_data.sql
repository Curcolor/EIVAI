-- Script de inserción de datos iniciales para Sistema de Gestión de Instrumental Quirúrgico
-- Versión: 1.0
-- Fecha: 26/05/2025

USE EIVEI_DB;
GO

-- Insertar estados de instrumentos
INSERT INTO EstadosInstrumento (NombreEstado, Descripcion, RequiereMantenimiento) VALUES
('En buen estado', 'Instrumento en condiciones óptimas para su uso', 0),
('Desgaste leve', 'Instrumento con desgaste mínimo pero funcional', 0),
('Requiere mantenimiento', 'Instrumento que necesita revisión o reparación', 1),
('Fuera de servicio', 'Instrumento no disponible para uso', 1);

-- Insertar usuario administrador por defecto
INSERT INTO Usuarios (NombreUsuario, NombreCompleto, Email, PasswordHash, Activo) VALUES
('admin', 'Administrador del Sistema', 'admin@hospital.com', 'hash_temporal_admin', 1),
('instrumentador1', 'María García López', 'maria.garcia@hospital.com', 'hash_temporal_maria', 1),
('instrumentador2', 'Carlos Rodríguez Pérez', 'carlos.rodriguez@hospital.com', 'hash_temporal_carlos', 1);

-- Insertar sets quirúrgicos básicos
INSERT INTO SetsQuirurgicos (NombreSet, NumeroIdentificacion, TipoProcedimiento, Descripcion) VALUES
('Equipo de cesárea', 'CESAREA-001', 'Cesárea', 'Set completo para procedimientos de cesárea'),
('Equipo de laparoscopia', 'LAPARO-001', 'Laparoscopia', 'Set especializado para cirugía laparoscópica'),
('Equipo de cirugía general', 'GENERAL-001', 'Cirugía General', 'Set básico para procedimientos quirúrgicos generales'),
('Equipo de cesárea', 'CESAREA-002', 'Cesárea', 'Set completo para procedimientos de cesárea - Backup');

-- Insertar instrumentos básicos
INSERT INTO Instrumentos (CodigoInstrumento, NombreInstrumento, Descripcion, EstadoID) VALUES
('BISP-001', 'Bisturí #11', 'Bisturí hoja número 11', 1),
('BISP-002', 'Bisturí #15', 'Bisturí hoja número 15', 1),
('PINZ-001', 'Pinza Kelly', 'Pinza hemostática Kelly curva', 1),
('PINZ-002', 'Pinza Allis', 'Pinza de prensión Allis', 1),
('TIJR-001', 'Tijera Mayo', 'Tijera Mayo recta', 1),
('TIJR-002', 'Tijera Metzenbaum', 'Tijera Metzenbaum curva', 1),
('PORT-001', 'Portaagujas', 'Portaagujas Mayo-Hegar', 1),
('SEPA-001', 'Separador Farabeuf', 'Separador autoestático Farabeuf', 1),
('ASPI-001', 'Aspirador quirúrgico', 'Tubo de aspiración quirúrgica', 1),
('GASA-001', 'Gasas estériles', 'Paquete de gasas estériles 4x4', 1);

-- Relacionar instrumentos con sets quirúrgicos
-- Set de cesárea #1
INSERT INTO SetInstrumentos (SetID, InstrumentoID, Cantidad, Obligatorio) VALUES
(1, 1, 2, 1), -- Bisturí #11
(1, 2, 1, 1), -- Bisturí #15
(1, 3, 4, 1), -- Pinza Kelly
(1, 4, 2, 1), -- Pinza Allis
(1, 5, 1, 1), -- Tijera Mayo
(1, 6, 1, 1), -- Tijera Metzenbaum
(1, 7, 2, 1), -- Portaagujas
(1, 8, 2, 1), -- Separador Farabeuf
(1, 9, 1, 1), -- Aspirador
(1, 10, 10, 1); -- Gasas

-- Set de laparoscopia
INSERT INTO SetInstrumentos (SetID, InstrumentoID, Cantidad, Obligatorio) VALUES
(2, 1, 1, 1), -- Bisturí #11
(2, 3, 2, 1), -- Pinza Kelly
(2, 5, 1, 1), -- Tijera Mayo
(2, 7, 1, 1), -- Portaagujas
(2, 10, 5, 1); -- Gasas

-- Set de cirugía general
INSERT INTO SetInstrumentos (SetID, InstrumentoID, Cantidad, Obligatorio) VALUES
(3, 1, 2, 1), -- Bisturí #11
(3, 2, 1, 1), -- Bisturí #15
(3, 3, 6, 1), -- Pinza Kelly
(3, 4, 4, 1), -- Pinza Allis
(3, 5, 2, 1), -- Tijera Mayo
(3, 6, 1, 1), -- Tijera Metzenbaum
(3, 7, 2, 1), -- Portaagujas
(3, 8, 3, 1), -- Separador Farabeuf
(3, 9, 1, 1), -- Aspirador
(3, 10, 15, 1); -- Gasas

-- Set de cesárea #2 (backup)
INSERT INTO SetInstrumentos (SetID, InstrumentoID, Cantidad, Obligatorio) VALUES
(4, 1, 2, 1), -- Bisturí #11
(4, 2, 1, 1), -- Bisturí #15
(4, 3, 4, 1), -- Pinza Kelly
(4, 4, 2, 1), -- Pinza Allis
(4, 5, 1, 1), -- Tijera Mayo
(4, 6, 1, 1), -- Tijera Metzenbaum
(4, 7, 2, 1), -- Portaagujas
(4, 8, 2, 1), -- Separador Farabeuf
(4, 9, 1, 1), -- Aspirador
(4, 10, 10, 1); -- Gasas

PRINT 'Datos iniciales insertados exitosamente.';
