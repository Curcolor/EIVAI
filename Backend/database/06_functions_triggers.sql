-- Script de funciones y triggers para Sistema de Gestión de Instrumental Quirúrgico
-- Versión: 1.0
-- Fecha: 26/05/2025

USE EIVEI_DB;
GO

-- =============================================
-- Función: Calcular tiempo promedio de procedimientos
-- =============================================
CREATE FUNCTION fn_TiempoPromedioProcedimientos(@TipoCirugia NVARCHAR(100) = NULL)
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @TiempoPromedio DECIMAL(10,2);
    
    SELECT @TiempoPromedio = AVG(
        DATEDIFF(MINUTE, 
            (SELECT MIN(FechaConteo) FROM ConteosInstrumentos ci WHERE ci.ProcedimientoID = p.ProcedimientoID AND ci.TipoConteo = 'INICIAL'),
            (SELECT MAX(FechaConteo) FROM ConteosInstrumentos ci WHERE ci.ProcedimientoID = p.ProcedimientoID AND ci.TipoConteo = 'FINAL')
        )
    )
    FROM ProcedimientosQuirurgicos p
    WHERE p.EstadoProcedimiento = 'FINALIZADO'
    AND (@TipoCirugia IS NULL OR p.TipoCirugia = @TipoCirugia)
    AND p.ConteoInicialCompleto = 1 
    AND p.ConteoFinalCompleto = 1;
    
    RETURN ISNULL(@TiempoPromedio, 0);
END;
GO

-- =============================================
-- Función: Verificar disponibilidad de set quirúrgico
-- =============================================
CREATE FUNCTION fn_VerificarDisponibilidadSet(@SetID INT)
RETURNS NVARCHAR(50)
AS
BEGIN
    DECLARE @Estado NVARCHAR(50) = 'DISPONIBLE';
    
    -- Verificar si hay instrumentos que requieren mantenimiento
    IF EXISTS (
        SELECT 1 FROM SetInstrumentos si
        INNER JOIN Instrumentos i ON si.InstrumentoID = i.InstrumentoID
        INNER JOIN EstadosInstrumento ei ON i.EstadoID = ei.EstadoID
        WHERE si.SetID = @SetID AND ei.RequiereMantenimiento = 1
    )
    BEGIN
        SET @Estado = 'MANTENIMIENTO_REQUERIDO';
    END
    -- Verificar esterilización
    ELSE IF EXISTS (
        SELECT 1 FROM SetInstrumentos si
        INNER JOIN Instrumentos i ON si.InstrumentoID = i.InstrumentoID
        WHERE si.SetID = @SetID 
        AND (i.UltimaEsterilizacion IS NULL OR DATEDIFF(DAY, i.UltimaEsterilizacion, GETDATE()) > 7)
    )
    BEGIN
        SET @Estado = 'ESTERILIZACION_REQUERIDA';
    END
    -- Verificar si está en uso
    ELSE IF EXISTS (
        SELECT 1 FROM ProcedimientosQuirurgicos p
        WHERE p.SetID = @SetID 
        AND p.EstadoProcedimiento IN ('INICIADO', 'EN_PROCESO')
    )
    BEGIN
        SET @Estado = 'EN_USO';
    END
    
    RETURN @Estado;
END;
GO

-- =============================================
-- Trigger: Auditoría para tabla Instrumentos
-- =============================================
CREATE TRIGGER tr_Instrumentos_Auditoria
ON Instrumentos
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @Accion NVARCHAR(20);
    DECLARE @UsuarioID INT = 1; -- Por defecto, se podría obtener del contexto de la aplicación
    
    -- Determinar el tipo de acción
    IF EXISTS(SELECT * FROM inserted) AND EXISTS(SELECT * FROM deleted)
        SET @Accion = 'UPDATE';
    ELSE IF EXISTS(SELECT * FROM inserted)
        SET @Accion = 'INSERT';
    ELSE
        SET @Accion = 'DELETE';
    
    -- Registrar cambios para UPDATE
    IF @Accion = 'UPDATE'
    BEGIN
        INSERT INTO AuditoriaAcciones (UsuarioID, Accion, TablaAfectada, RegistroID, ValoresAnteriores, ValoresNuevos)
        SELECT 
            @UsuarioID,
            @Accion,
            'Instrumentos',
            ISNULL(i.InstrumentoID, d.InstrumentoID),
            CONCAT('Estado:', d.EstadoID, ',ContadorUso:', d.ContadorUso, ',UltimaEsterilizacion:', ISNULL(CAST(d.UltimaEsterilizacion AS NVARCHAR), 'NULL')),
            CONCAT('Estado:', i.EstadoID, ',ContadorUso:', i.ContadorUso, ',UltimaEsterilizacion:', ISNULL(CAST(i.UltimaEsterilizacion AS NVARCHAR), 'NULL'))
        FROM inserted i
        FULL OUTER JOIN deleted d ON i.InstrumentoID = d.InstrumentoID;
    END
    
    -- Registrar cambios para INSERT
    IF @Accion = 'INSERT'
    BEGIN
        INSERT INTO AuditoriaAcciones (UsuarioID, Accion, TablaAfectada, RegistroID, ValoresNuevos)
        SELECT 
            @UsuarioID,
            @Accion,
            'Instrumentos',
            i.InstrumentoID,
            CONCAT('Codigo:', i.CodigoInstrumento, ',Nombre:', i.NombreInstrumento, ',Estado:', i.EstadoID)
        FROM inserted i;
    END
    
    -- Registrar cambios para DELETE
    IF @Accion = 'DELETE'
    BEGIN
        INSERT INTO AuditoriaAcciones (UsuarioID, Accion, TablaAfectada, RegistroID, ValoresAnteriores)
        SELECT 
            @UsuarioID,
            @Accion,
            'Instrumentos',
            d.InstrumentoID,
            CONCAT('Codigo:', d.CodigoInstrumento, ',Nombre:', d.NombreInstrumento, ',Estado:', d.EstadoID)
        FROM deleted d;
    END
END;
GO

-- =============================================
-- Trigger: Generar alertas automáticas en conteos
-- =============================================
CREATE TRIGGER tr_ConteosInstrumentos_Alertas
ON ConteosInstrumentos
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Generar alertas para conteos finales con discrepancias
    INSERT INTO Alertas (ProcedimientoID, InstrumentoID, TipoAlerta, Mensaje, Prioridad)
    SELECT 
        i.ProcedimientoID,
        i.InstrumentoID,
        'CONTEO_INCORRECTO',
        CONCAT('Discrepancia en conteo final para instrumento ', ins.NombreInstrumento, 
               ': Esperado ', i.CantidadEsperada, ', Contado ', i.CantidadContada),
        'CRITICA'
    FROM inserted i
    INNER JOIN Instrumentos ins ON i.InstrumentoID = ins.InstrumentoID
    WHERE i.TipoConteo = 'FINAL' 
    AND i.CantidadContada != i.CantidadEsperada;
    
    -- Actualizar estado de procedimiento si el conteo final está completo y correcto
    UPDATE p
    SET EstadoProcedimiento = 'FINALIZADO',
        ConteoFinalCompleto = 1
    FROM ProcedimientosQuirurgicos p
    INNER JOIN inserted i ON p.ProcedimientoID = i.ProcedimientoID
    WHERE i.TipoConteo = 'FINAL'
    AND NOT EXISTS (
        -- Verificar que no haya discrepancias en ningún instrumento del procedimiento
        SELECT 1 FROM ConteosInstrumentos ci
        WHERE ci.ProcedimientoID = p.ProcedimientoID
        AND ci.TipoConteo = 'FINAL'
        AND ci.CantidadContada != ci.CantidadEsperada
    )
    AND EXISTS (
        -- Verificar que todos los instrumentos del set tienen conteo final
        SELECT 1 FROM SetInstrumentos si
        INNER JOIN ConteosInstrumentos ci ON si.InstrumentoID = ci.InstrumentoID
        WHERE si.SetID = p.SetID
        AND ci.ProcedimientoID = p.ProcedimientoID
        AND ci.TipoConteo = 'FINAL'
        HAVING COUNT(*) = (SELECT COUNT(*) FROM SetInstrumentos si2 WHERE si2.SetID = p.SetID)
    );
END;
GO

-- =============================================
-- Trigger: Validar esterilización antes de uso
-- =============================================
CREATE TRIGGER tr_ProcedimientosQuirurgicos_ValidacionEsterilizacion
ON ProcedimientosQuirurgicos
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Generar alertas para instrumentos sin esterilización válida
    INSERT INTO Alertas (ProcedimientoID, InstrumentoID, TipoAlerta, Mensaje, Prioridad)
    SELECT 
        i.ProcedimientoID,
        inst.InstrumentoID,
        'ESTERILIZACION_REQUERIDA',
        CONCAT('El instrumento ', inst.NombreInstrumento, ' requiere esterilización antes del procedimiento'),
        'ALTA'
    FROM inserted i
    INNER JOIN SetInstrumentos si ON i.SetID = si.SetID
    INNER JOIN Instrumentos inst ON si.InstrumentoID = inst.InstrumentoID
    WHERE inst.UltimaEsterilizacion IS NULL 
    OR DATEDIFF(DAY, inst.UltimaEsterilizacion, GETDATE()) > 7;
    
    -- Generar alertas para instrumentos que requieren mantenimiento
    INSERT INTO Alertas (ProcedimientoID, InstrumentoID, TipoAlerta, Mensaje, Prioridad)
    SELECT 
        i.ProcedimientoID,
        inst.InstrumentoID,
        'MANTENIMIENTO_REQUERIDO',
        CONCAT('El instrumento ', inst.NombreInstrumento, ' requiere mantenimiento y no puede ser usado'),
        'CRITICA'
    FROM inserted i
    INNER JOIN SetInstrumentos si ON i.SetID = si.SetID
    INNER JOIN Instrumentos inst ON si.InstrumentoID = inst.InstrumentoID
    INNER JOIN EstadosInstrumento ei ON inst.EstadoID = ei.EstadoID
    WHERE ei.RequiereMantenimiento = 1;
END;
GO

-- =============================================
-- Trigger: Actualizar último acceso de usuarios
-- =============================================
CREATE TRIGGER tr_Usuarios_UltimoAcceso
ON AuditoriaAcciones
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    
    UPDATE u
    SET UltimoAcceso = GETDATE()
    FROM Usuarios u
    INNER JOIN inserted i ON u.UsuarioID = i.UsuarioID;
END;
GO

-- =============================================
-- Función: Obtener próximos instrumentos para mantenimiento
-- =============================================
CREATE FUNCTION fn_InstrumentosProximoMantenimiento(@DiasAnticipacion INT = 30)
RETURNS TABLE
AS
RETURN
(
    SELECT 
        i.InstrumentoID,
        i.CodigoInstrumento,
        i.NombreInstrumento,
        i.ContadorUso,
        ei.NombreEstado,
        CASE 
            WHEN i.ContadorUso >= 100 THEN 'POR_USO_INTENSIVO'
            WHEN DATEDIFF(DAY, i.UltimaEsterilizacion, GETDATE()) > (7 - @DiasAnticipacion) THEN 'POR_ESTERILIZACION'
            ELSE 'PREVENTIVO'
        END AS MotivoMantenimiento,
        i.ContadorUso AS UsosAcumulados,
        i.UltimaEsterilizacion
    FROM Instrumentos i
    INNER JOIN EstadosInstrumento ei ON i.EstadoID = ei.EstadoID
    WHERE ei.RequiereMantenimiento = 0  -- Solo instrumentos que actualmente no requieren mantenimiento
    AND (
        i.ContadorUso >= 100  -- Instrumentos con uso intensivo
        OR DATEDIFF(DAY, i.UltimaEsterilizacion, GETDATE()) > (7 - @DiasAnticipacion) -- Próximos a vencer esterilización
    )
);
GO

PRINT 'Funciones y triggers creados exitosamente.';
