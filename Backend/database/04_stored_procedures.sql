-- Script de procedimientos almacenados para Sistema de Gestión de Instrumental Quirúrgico
-- Versión: 1.0
-- Fecha: 26/05/2025

USE EIVEI_DB;
GO

-- =============================================
-- Procedimiento: Iniciar nuevo procedimiento quirúrgico
-- =============================================
CREATE PROCEDURE sp_IniciarProcedimientoQuirurgico
    @SetID INT,
    @UsuarioResponsable INT,
    @TipoCirugia NVARCHAR(100),
    @Paciente NVARCHAR(100),
    @Medico NVARCHAR(100),
    @ProcedimientoID INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Insertar nuevo procedimiento
        INSERT INTO ProcedimientosQuirurgicos 
        (SetID, UsuarioResponsable, FechaProcedimiento, TipoCirugia, Paciente, Medico)
        VALUES 
        (@SetID, @UsuarioResponsable, GETDATE(), @TipoCirugia, @Paciente, @Medico);
        
        SET @ProcedimientoID = SCOPE_IDENTITY();
        
        -- Registrar auditoría
        INSERT INTO AuditoriaAcciones (UsuarioID, Accion, TablaAfectada, RegistroID, ValoresNuevos)
        VALUES (@UsuarioResponsable, 'CREAR_PROCEDIMIENTO', 'ProcedimientosQuirurgicos', @ProcedimientoID, 
                'SetID: ' + CAST(@SetID AS NVARCHAR) + ', Paciente: ' + @Paciente);
        
        COMMIT TRANSACTION;
        
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- =============================================
-- Procedimiento: Registrar conteo inicial de instrumentos
-- =============================================
CREATE PROCEDURE sp_RegistrarConteoInicial
    @ProcedimientoID INT,
    @UsuarioConteo INT,
    @FotografiaPath NVARCHAR(500) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Obtener el SetID del procedimiento
        DECLARE @SetID INT;
        SELECT @SetID = SetID FROM ProcedimientosQuirurgicos WHERE ProcedimientoID = @ProcedimientoID;
        
        -- Insertar conteos iniciales para todos los instrumentos del set
        INSERT INTO ConteosInstrumentos 
        (ProcedimientoID, InstrumentoID, TipoConteo, CantidadContada, CantidadEsperada, UsuarioConteo, FotografiaPath)
        SELECT 
            @ProcedimientoID,
            si.InstrumentoID,
            'INICIAL',
            si.Cantidad,  -- Asumimos conteo correcto inicialmente
            si.Cantidad,
            @UsuarioConteo,
            @FotografiaPath
        FROM SetInstrumentos si
        WHERE si.SetID = @SetID;
        
        -- Actualizar estado del procedimiento
        UPDATE ProcedimientosQuirurgicos 
        SET ConteoInicialCompleto = 1
        WHERE ProcedimientoID = @ProcedimientoID;
        
        -- Actualizar contador de uso de instrumentos
        UPDATE i
        SET ContadorUso = ContadorUso + 1
        FROM Instrumentos i
        INNER JOIN SetInstrumentos si ON i.InstrumentoID = si.InstrumentoID
        WHERE si.SetID = @SetID;
        
        COMMIT TRANSACTION;
        
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- =============================================
-- Procedimiento: Registrar conteo final de instrumentos
-- =============================================
CREATE PROCEDURE sp_RegistrarConteoFinal
    @ProcedimientoID INT,
    @UsuarioConteo INT,
    @FotografiaPath NVARCHAR(500) = NULL,
    @ConteosJson NVARCHAR(MAX) -- JSON con formato: [{"InstrumentoID": 1, "CantidadContada": 2}]
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Crear tabla temporal para los conteos
        CREATE TABLE #ConteosTemp (
            InstrumentoID INT,
            CantidadContada INT
        );
        
        -- Parsear JSON e insertar en tabla temporal
        INSERT INTO #ConteosTemp (InstrumentoID, CantidadContada)
        SELECT 
            JSON_VALUE(value, '$.InstrumentoID'),
            JSON_VALUE(value, '$.CantidadContada')
        FROM OPENJSON(@ConteosJson);
        
        -- Insertar conteos finales
        INSERT INTO ConteosInstrumentos 
        (ProcedimientoID, InstrumentoID, TipoConteo, CantidadContada, CantidadEsperada, UsuarioConteo, FotografiaPath)
        SELECT 
            @ProcedimientoID,
            ct.InstrumentoID,
            'FINAL',
            ct.CantidadContada,
            si.Cantidad,
            @UsuarioConteo,
            @FotografiaPath
        FROM #ConteosTemp ct
        INNER JOIN SetInstrumentos si ON ct.InstrumentoID = si.InstrumentoID
        INNER JOIN ProcedimientosQuirurgicos p ON si.SetID = p.SetID
        WHERE p.ProcedimientoID = @ProcedimientoID;
        
        -- Verificar discrepancias y crear alertas
        INSERT INTO Alertas (ProcedimientoID, InstrumentoID, TipoAlerta, Mensaje, Prioridad)
        SELECT 
            @ProcedimientoID,
            ct.InstrumentoID,
            'CONTEO_INCORRECTO',
            'Discrepancia en conteo final: Esperado ' + CAST(si.Cantidad AS NVARCHAR) + 
            ', Contado ' + CAST(ct.CantidadContada AS NVARCHAR),
            'CRITICA'
        FROM #ConteosTemp ct
        INNER JOIN SetInstrumentos si ON ct.InstrumentoID = si.InstrumentoID
        INNER JOIN ProcedimientosQuirurgicos p ON si.SetID = p.SetID
        WHERE p.ProcedimientoID = @ProcedimientoID
        AND ct.CantidadContada != si.Cantidad;
        
        -- Actualizar estado del procedimiento solo si no hay discrepancias
        IF NOT EXISTS (
            SELECT 1 FROM #ConteosTemp ct
            INNER JOIN SetInstrumentos si ON ct.InstrumentoID = si.InstrumentoID
            INNER JOIN ProcedimientosQuirurgicos p ON si.SetID = p.SetID
            WHERE p.ProcedimientoID = @ProcedimientoID
            AND ct.CantidadContada != si.Cantidad
        )
        BEGIN
            UPDATE ProcedimientosQuirurgicos 
            SET ConteoFinalCompleto = 1, EstadoProcedimiento = 'FINALIZADO'
            WHERE ProcedimientoID = @ProcedimientoID;
        END
        
        DROP TABLE #ConteosTemp;
        COMMIT TRANSACTION;
        
    END TRY
    BEGIN CATCH
        IF OBJECT_ID('tempdb..#ConteosTemp') IS NOT NULL
            DROP TABLE #ConteosTemp;
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- =============================================
-- Procedimiento: Registrar ciclo de esterilización
-- =============================================
CREATE PROCEDURE sp_RegistrarCicloEsterilizacion
    @CodigoCiclo NVARCHAR(50),
    @MetodoEsterilizacion NVARCHAR(50),
    @TemperaturaGrados DECIMAL(5,2) = NULL,
    @TiempoMinutos INT = NULL,
    @UsuarioResponsable INT,
    @InstrumentosJson NVARCHAR(MAX), -- JSON con IDs de instrumentos
    @CicloID INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    
    BEGIN TRY
        BEGIN TRANSACTION;
        
        -- Insertar ciclo de esterilización
        INSERT INTO CiclosEsterilizacion 
        (CodigoCiclo, FechaEsterilizacion, MetodoEsterilizacion, TemperaturaGrados, TiempoMinutos, UsuarioResponsable)
        VALUES 
        (@CodigoCiclo, GETDATE(), @MetodoEsterilizacion, @TemperaturaGrados, @TiempoMinutos, @UsuarioResponsable);
        
        SET @CicloID = SCOPE_IDENTITY();
        
        -- Insertar relación instrumentos-esterilización
        INSERT INTO InstrumentosEsterilizacion (InstrumentoID, CicloID)
        SELECT 
            CAST(JSON_VALUE(value, '$') AS INT),
            @CicloID
        FROM OPENJSON(@InstrumentosJson);
        
        -- Actualizar fecha de última esterilización en instrumentos
        UPDATE Instrumentos 
        SET UltimaEsterilizacion = GETDATE()
        WHERE InstrumentoID IN (
            SELECT CAST(JSON_VALUE(value, '$') AS INT)
            FROM OPENJSON(@InstrumentosJson)
        );
        
        COMMIT TRANSACTION;
        
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END;
GO

-- =============================================
-- Procedimiento: Obtener estadísticas de uso de instrumentos
-- =============================================
CREATE PROCEDURE sp_ObtenerEstadisticasUsoInstrumentos
    @FechaInicio DATETIME = NULL,
    @FechaFin DATETIME = NULL
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Si no se proporcionan fechas, usar últimos 30 días
    IF @FechaInicio IS NULL
        SET @FechaInicio = DATEADD(DAY, -30, GETDATE());
    
    IF @FechaFin IS NULL
        SET @FechaFin = GETDATE();
    
    SELECT 
        i.InstrumentoID,
        i.CodigoInstrumento,
        i.NombreInstrumento,
        i.ContadorUso AS UsoTotal,
        COUNT(DISTINCT p.ProcedimientoID) AS UsosEnPeriodo,
        ei.NombreEstado AS EstadoActual,
        i.UltimaEsterilizacion,
        DATEDIFF(DAY, i.UltimaEsterilizacion, GETDATE()) AS DiasSinEsterilizar
    FROM Instrumentos i
    INNER JOIN EstadosInstrumento ei ON i.EstadoID = ei.EstadoID
    LEFT JOIN SetInstrumentos si ON i.InstrumentoID = si.InstrumentoID
    LEFT JOIN ProcedimientosQuirurgicos p ON si.SetID = p.SetID 
        AND p.FechaProcedimiento BETWEEN @FechaInicio AND @FechaFin
    GROUP BY 
        i.InstrumentoID, i.CodigoInstrumento, i.NombreInstrumento, 
        i.ContadorUso, ei.NombreEstado, i.UltimaEsterilizacion
    ORDER BY i.ContadorUso DESC;
END;
GO

-- =============================================
-- Procedimiento: Generar reporte de procedimiento
-- =============================================
CREATE PROCEDURE sp_GenerarReporteProcedimiento
    @ProcedimientoID INT
AS
BEGIN
    SET NOCOUNT ON;
    
    -- Información general del procedimiento
    SELECT 
        p.ProcedimientoID,
        p.FechaProcedimiento,
        p.TipoCirugia,
        p.Paciente,
        p.Medico,
        p.EstadoProcedimiento,
        s.NombreSet,
        s.NumeroIdentificacion,
        u.NombreCompleto AS ResponsableInstrumentacion,
        p.ConteoInicialCompleto,
        p.ConteoFinalCompleto
    FROM ProcedimientosQuirurgicos p
    INNER JOIN SetsQuirurgicos s ON p.SetID = s.SetID
    INNER JOIN Usuarios u ON p.UsuarioResponsable = u.UsuarioID
    WHERE p.ProcedimientoID = @ProcedimientoID;
    
    -- Conteos de instrumentos
    SELECT 
        i.CodigoInstrumento,
        i.NombreInstrumento,
        ci.TipoConteo,
        ci.CantidadEsperada,
        ci.CantidadContada,
        CASE 
            WHEN ci.CantidadContada = ci.CantidadEsperada THEN 'OK'
            ELSE 'DISCREPANCIA'
        END AS Estado,
        ci.FechaConteo,
        u.NombreCompleto AS UsuarioConteo
    FROM ConteosInstrumentos ci
    INNER JOIN Instrumentos i ON ci.InstrumentoID = i.InstrumentoID
    INNER JOIN Usuarios u ON ci.UsuarioConteo = u.UsuarioID
    WHERE ci.ProcedimientoID = @ProcedimientoID
    ORDER BY i.NombreInstrumento, ci.TipoConteo;
    
    -- Alertas generadas
    SELECT 
        TipoAlerta,
        Mensaje,
        Prioridad,
        FechaCreacion,
        Resuelta,
        FechaResolucion
    FROM Alertas
    WHERE ProcedimientoID = @ProcedimientoID
    ORDER BY FechaCreacion;
END;
GO

-- =============================================
-- Procedimiento: Validar instrumentos antes de asignación
-- =============================================
CREATE PROCEDURE sp_ValidarInstrumentosParaAsignacion
    @SetID INT
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        i.InstrumentoID,
        i.CodigoInstrumento,
        i.NombreInstrumento,
        ei.NombreEstado,
        i.UltimaEsterilizacion,
        CASE 
            WHEN ei.RequiereMantenimiento = 1 THEN 'NO_DISPONIBLE'
            WHEN i.UltimaEsterilizacion IS NULL THEN 'SIN_ESTERILIZAR'
            WHEN DATEDIFF(DAY, i.UltimaEsterilizacion, GETDATE()) > 7 THEN 'ESTERILIZACION_VENCIDA'
            ELSE 'DISPONIBLE'
        END AS EstadoDisponibilidad,
        si.Cantidad AS CantidadRequerida
    FROM SetInstrumentos si
    INNER JOIN Instrumentos i ON si.InstrumentoID = i.InstrumentoID
    INNER JOIN EstadosInstrumento ei ON i.EstadoID = ei.EstadoID
    WHERE si.SetID = @SetID
    ORDER BY i.NombreInstrumento;
END;
GO

PRINT 'Procedimientos almacenados creados exitosamente.';
