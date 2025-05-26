-- Script de vistas para Sistema de Gestión de Instrumental Quirúrgico
-- Versión: 1.0
-- Fecha: 26/05/2025

USE EIVEI_DB;
GO

-- =============================================
-- Vista: Resumen de procedimientos quirúrgicos
-- =============================================
CREATE VIEW vw_ResumenProcedimientos
AS
SELECT 
    p.ProcedimientoID,
    p.FechaProcedimiento,
    p.TipoCirugia,
    p.Paciente,
    p.Medico,
    p.EstadoProcedimiento,
    s.NombreSet,
    s.NumeroIdentificacion AS SetNumero,
    u.NombreCompleto AS ResponsableInstrumentacion,
    p.ConteoInicialCompleto,
    p.ConteoFinalCompleto,
    CASE 
        WHEN p.ConteoInicialCompleto = 1 AND p.ConteoFinalCompleto = 1 THEN 'COMPLETO'
        WHEN p.ConteoInicialCompleto = 1 AND p.ConteoFinalCompleto = 0 THEN 'PENDIENTE_CONTEO_FINAL'
        WHEN p.ConteoInicialCompleto = 0 THEN 'PENDIENTE_CONTEO_INICIAL'
        ELSE 'INCOMPLETO'
    END AS EstadoConteos,
    -- Contar alertas activas para este procedimiento
    (SELECT COUNT(*) FROM Alertas a WHERE a.ProcedimientoID = p.ProcedimientoID AND a.Resuelta = 0) AS AlertasActivas
FROM ProcedimientosQuirurgicos p
INNER JOIN SetsQuirurgicos s ON p.SetID = s.SetID
INNER JOIN Usuarios u ON p.UsuarioResponsable = u.UsuarioID;
GO

-- =============================================
-- Vista: Estado actual de instrumentos
-- =============================================
CREATE VIEW vw_EstadoInstrumentos
AS
SELECT 
    i.InstrumentoID,
    i.CodigoInstrumento,
    i.NombreInstrumento,
    i.Descripcion,
    ei.NombreEstado AS Estado,
    ei.RequiereMantenimiento,
    i.ContadorUso,
    i.UltimaEsterilizacion,
    CASE 
        WHEN i.UltimaEsterilizacion IS NULL THEN 'SIN_ESTERILIZAR'
        WHEN DATEDIFF(DAY, i.UltimaEsterilizacion, GETDATE()) > 7 THEN 'ESTERILIZACION_VENCIDA'
        WHEN DATEDIFF(DAY, i.UltimaEsterilizacion, GETDATE()) > 5 THEN 'ESTERILIZACION_POR_VENCER'
        ELSE 'ESTERILIZACION_VIGENTE'
    END AS EstadoEsterilizacion,
    DATEDIFF(DAY, i.UltimaEsterilizacion, GETDATE()) AS DiasSinEsterilizar,
    -- Último ciclo de esterilización
    (SELECT TOP 1 ce.CodigoCiclo 
     FROM InstrumentosEsterilizacion ie 
     INNER JOIN CiclosEsterilizacion ce ON ie.CicloID = ce.CicloID
     WHERE ie.InstrumentoID = i.InstrumentoID
     ORDER BY ce.FechaEsterilizacion DESC) AS UltimoCicloEsterilizacion,
    -- Disponibilidad para uso
    CASE 
        WHEN ei.RequiereMantenimiento = 1 THEN 'NO_DISPONIBLE'
        WHEN i.UltimaEsterilizacion IS NULL THEN 'NO_DISPONIBLE'
        WHEN DATEDIFF(DAY, i.UltimaEsterilizacion, GETDATE()) > 7 THEN 'NO_DISPONIBLE'
        ELSE 'DISPONIBLE'
    END AS Disponibilidad
FROM Instrumentos i
INNER JOIN EstadosInstrumento ei ON i.EstadoID = ei.EstadoID;
GO

-- =============================================
-- Vista: Alertas activas y críticas
-- =============================================
CREATE VIEW vw_AlertasActivas
AS
SELECT 
    a.AlertaID,
    a.TipoAlerta,
    a.Mensaje,
    a.Prioridad,
    a.FechaCreacion,
    DATEDIFF(HOUR, a.FechaCreacion, GETDATE()) AS HorasDesdeCreacion,
    -- Información del procedimiento (si aplica)
    p.ProcedimientoID,
    p.TipoCirugia,
    p.Paciente,
    s.NombreSet,
    -- Información del instrumento (si aplica)
    i.CodigoInstrumento,
    i.NombreInstrumento,
    -- Usuario responsable del procedimiento
    u.NombreCompleto AS ResponsableProcedimiento
FROM Alertas a
LEFT JOIN ProcedimientosQuirurgicos p ON a.ProcedimientoID = p.ProcedimientoID
LEFT JOIN SetsQuirurgicos s ON p.SetID = s.SetID
LEFT JOIN Usuarios u ON p.UsuarioResponsable = u.UsuarioID
LEFT JOIN Instrumentos i ON a.InstrumentoID = i.InstrumentoID
WHERE a.Resuelta = 0;
GO

-- =============================================
-- Vista: Historial de uso de instrumentos
-- =============================================
CREATE VIEW vw_HistorialUsoInstrumentos
AS
SELECT 
    i.InstrumentoID,
    i.CodigoInstrumento,
    i.NombreInstrumento,
    p.ProcedimientoID,
    p.FechaProcedimiento,
    p.TipoCirugia,
    p.Paciente,
    s.NombreSet,
    u.NombreCompleto AS ResponsableInstrumentacion,
    ci.TipoConteo,
    ci.CantidadEsperada,
    ci.CantidadContada,
    CASE 
        WHEN ci.CantidadContada = ci.CantidadEsperada THEN 'OK'
        ELSE 'DISCREPANCIA'
    END AS EstadoConteo,
    ci.FechaConteo
FROM ConteosInstrumentos ci
INNER JOIN Instrumentos i ON ci.InstrumentoID = i.InstrumentoID
INNER JOIN ProcedimientosQuirurgicos p ON ci.ProcedimientoID = p.ProcedimientoID
INNER JOIN SetsQuirurgicos s ON p.SetID = s.SetID
INNER JOIN Usuarios u ON p.UsuarioResponsable = u.UsuarioID;
GO

-- =============================================
-- Vista: Estadísticas de sets quirúrgicos
-- =============================================
CREATE VIEW vw_EstadisticasSets
AS
SELECT 
    s.SetID,
    s.NombreSet,
    s.NumeroIdentificacion,
    s.TipoProcedimiento,
    -- Conteo de instrumentos en el set
    (SELECT COUNT(*) FROM SetInstrumentos si WHERE si.SetID = s.SetID) AS TotalInstrumentos,
    (SELECT SUM(si.Cantidad) FROM SetInstrumentos si WHERE si.SetID = s.SetID) AS TotalPiezas,
    -- Uso en los últimos 30 días
    (SELECT COUNT(*) 
     FROM ProcedimientosQuirurgicos p 
     WHERE p.SetID = s.SetID 
     AND p.FechaProcedimiento >= DATEADD(DAY, -30, GETDATE())) AS UsosUltimos30Dias,
    -- Uso total
    (SELECT COUNT(*) FROM ProcedimientosQuirurgicos p WHERE p.SetID = s.SetID) AS UsoTotal,
    -- Último uso
    (SELECT MAX(p.FechaProcedimiento) 
     FROM ProcedimientosQuirurgicos p 
     WHERE p.SetID = s.SetID) AS UltimoUso,
    -- Estado de disponibilidad
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM SetInstrumentos si
            INNER JOIN Instrumentos i ON si.InstrumentoID = i.InstrumentoID
            INNER JOIN EstadosInstrumento ei ON i.EstadoID = ei.EstadoID
            WHERE si.SetID = s.SetID AND ei.RequiereMantenimiento = 1
        ) THEN 'MANTENIMIENTO_REQUERIDO'
        WHEN EXISTS (
            SELECT 1 FROM SetInstrumentos si
            INNER JOIN Instrumentos i ON si.InstrumentoID = i.InstrumentoID
            WHERE si.SetID = s.SetID 
            AND (i.UltimaEsterilizacion IS NULL OR DATEDIFF(DAY, i.UltimaEsterilizacion, GETDATE()) > 7)
        ) THEN 'ESTERILIZACION_REQUERIDA'
        ELSE 'DISPONIBLE'
    END AS EstadoDisponibilidad
FROM SetsQuirurgicos s
WHERE s.Activo = 1;
GO

-- =============================================
-- Vista: Dashboard de actividad diaria
-- =============================================
CREATE VIEW vw_DashboardActividadDiaria
AS
SELECT 
    CAST(GETDATE() AS DATE) AS Fecha,
    -- Procedimientos del día
    (SELECT COUNT(*) 
     FROM ProcedimientosQuirurgicos p 
     WHERE CAST(p.FechaProcedimiento AS DATE) = CAST(GETDATE() AS DATE)) AS ProcedimientosHoy,
    -- Procedimientos completados
    (SELECT COUNT(*) 
     FROM ProcedimientosQuirurgicos p 
     WHERE CAST(p.FechaProcedimiento AS DATE) = CAST(GETDATE() AS DATE)
     AND p.EstadoProcedimiento = 'FINALIZADO') AS ProcedimientosCompletados,
    -- Procedimientos en proceso
    (SELECT COUNT(*) 
     FROM ProcedimientosQuirurgicos p 
     WHERE CAST(p.FechaProcedimiento AS DATE) = CAST(GETDATE() AS DATE)
     AND p.EstadoProcedimiento IN ('INICIADO', 'EN_PROCESO')) AS ProcedimientosEnProceso,
    -- Alertas críticas activas
    (SELECT COUNT(*) 
     FROM Alertas a 
     WHERE a.Resuelta = 0 AND a.Prioridad = 'CRITICA') AS AlertasCriticasActivas,
    -- Instrumentos que requieren mantenimiento
    (SELECT COUNT(*) 
     FROM Instrumentos i 
     INNER JOIN EstadosInstrumento ei ON i.EstadoID = ei.EstadoID
     WHERE ei.RequiereMantenimiento = 1) AS InstrumentosMantenimiento,
    -- Instrumentos sin esterilizar o con esterilización vencida
    (SELECT COUNT(*) 
     FROM Instrumentos i 
     WHERE i.UltimaEsterilizacion IS NULL 
     OR DATEDIFF(DAY, i.UltimaEsterilizacion, GETDATE()) > 7) AS InstrumentosSinEsterilizar;
GO

-- =============================================
-- Vista: Trazabilidad completa de instrumentos
-- =============================================
CREATE VIEW vw_TrazabilidadInstrumentos
AS
SELECT 
    i.InstrumentoID,
    i.CodigoInstrumento,
    i.NombreInstrumento,
    'USO_PROCEDIMIENTO' AS TipoEvento,
    p.FechaProcedimiento AS FechaEvento,
    CONCAT('Usado en procedimiento: ', p.TipoCirugia, ' - Paciente: ', p.Paciente) AS DescripcionEvento,
    u.NombreCompleto AS UsuarioResponsable,
    p.ProcedimientoID AS ReferenciaID
FROM Instrumentos i
INNER JOIN SetInstrumentos si ON i.InstrumentoID = si.InstrumentoID
INNER JOIN ProcedimientosQuirurgicos p ON si.SetID = p.SetID
INNER JOIN Usuarios u ON p.UsuarioResponsable = u.UsuarioID

UNION ALL

SELECT 
    i.InstrumentoID,
    i.CodigoInstrumento,
    i.NombreInstrumento,
    'ESTERILIZACION' AS TipoEvento,
    ce.FechaEsterilizacion AS FechaEvento,
    CONCAT('Esterilización: ', ce.MetodoEsterilizacion, ' - Ciclo: ', ce.CodigoCiclo) AS DescripcionEvento,
    u.NombreCompleto AS UsuarioResponsable,
    ce.CicloID AS ReferenciaID
FROM Instrumentos i
INNER JOIN InstrumentosEsterilizacion ie ON i.InstrumentoID = ie.InstrumentoID
INNER JOIN CiclosEsterilizacion ce ON ie.CicloID = ce.CicloID
INNER JOIN Usuarios u ON ce.UsuarioResponsable = u.UsuarioID

UNION ALL

SELECT 
    i.InstrumentoID,
    i.CodigoInstrumento,
    i.NombreInstrumento,
    'CAMBIO_ESTADO' AS TipoEvento,
    aa.FechaAccion AS FechaEvento,
    CONCAT('Cambio de estado registrado: ', aa.Accion) AS DescripcionEvento,
    u.NombreCompleto AS UsuarioResponsable,
    aa.AuditoriaID AS ReferenciaID
FROM Instrumentos i
INNER JOIN AuditoriaAcciones aa ON aa.TablaAfectada = 'Instrumentos' AND aa.RegistroID = i.InstrumentoID
INNER JOIN Usuarios u ON aa.UsuarioID = u.UsuarioID;
GO

PRINT 'Vistas creadas exitosamente.';
