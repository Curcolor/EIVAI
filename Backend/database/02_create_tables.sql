-- Script de creación de tablas para Sistema de Gestión de Instrumental Quirúrgico
-- Versión: 1.0
-- Fecha: 26/05/2025

USE EIVEI_DB;
GO

-- Tabla de Usuarios (Instrumentadores)
CREATE TABLE Usuarios (
    UsuarioID INT IDENTITY(1,1) PRIMARY KEY,
    NombreUsuario NVARCHAR(50) UNIQUE NOT NULL,
    NombreCompleto NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) NOT NULL,
    PasswordHash NVARCHAR(255) NOT NULL,
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    UltimoAcceso DATETIME NULL
);

-- Tabla de Sets Quirúrgicos
CREATE TABLE SetsQuirurgicos (
    SetID INT IDENTITY(1,1) PRIMARY KEY,
    NombreSet NVARCHAR(100) NOT NULL,
    NumeroIdentificacion NVARCHAR(50) UNIQUE NOT NULL,
    TipoProcedimiento NVARCHAR(100) NOT NULL,
    Descripcion NVARCHAR(500) NULL,
    Activo BIT DEFAULT 1,
    FechaCreacion DATETIME DEFAULT GETDATE()
);

-- Tabla de Estados de Instrumentos
CREATE TABLE EstadosInstrumento (
    EstadoID INT IDENTITY(1,1) PRIMARY KEY,
    NombreEstado NVARCHAR(50) NOT NULL,
    Descripcion NVARCHAR(200) NULL,
    RequiereMantenimiento BIT DEFAULT 0
);

-- Tabla de Instrumentos
CREATE TABLE Instrumentos (
    InstrumentoID INT IDENTITY(1,1) PRIMARY KEY,
    CodigoInstrumento NVARCHAR(50) UNIQUE NOT NULL,
    NombreInstrumento NVARCHAR(100) NOT NULL,
    Descripcion NVARCHAR(500) NULL,
    EstadoID INT NOT NULL,
    ContadorUso INT DEFAULT 0,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    UltimaEsterilizacion DATETIME NULL,
    FOREIGN KEY (EstadoID) REFERENCES EstadosInstrumento(EstadoID)
);

-- Tabla de relación Set-Instrumentos
CREATE TABLE SetInstrumentos (
    SetInstrumentoID INT IDENTITY(1,1) PRIMARY KEY,
    SetID INT NOT NULL,
    InstrumentoID INT NOT NULL,
    Cantidad INT NOT NULL DEFAULT 1,
    Obligatorio BIT DEFAULT 1,
    FOREIGN KEY (SetID) REFERENCES SetsQuirurgicos(SetID),
    FOREIGN KEY (InstrumentoID) REFERENCES Instrumentos(InstrumentoID),
    UNIQUE(SetID, InstrumentoID)
);

-- Tabla de Procedimientos Quirúrgicos
CREATE TABLE ProcedimientosQuirurgicos (
    ProcedimientoID INT IDENTITY(1,1) PRIMARY KEY,
    SetID INT NOT NULL,
    UsuarioResponsable INT NOT NULL,
    FechaProcedimiento DATETIME NOT NULL,
    TipoCirugia NVARCHAR(100) NOT NULL,
    Paciente NVARCHAR(100) NOT NULL,
    Medico NVARCHAR(100) NOT NULL,
    EstadoProcedimiento NVARCHAR(20) DEFAULT 'INICIADO' CHECK (EstadoProcedimiento IN ('INICIADO', 'EN_PROCESO', 'FINALIZADO', 'CANCELADO')),
    ConteoInicialCompleto BIT DEFAULT 0,
    ConteoFinalCompleto BIT DEFAULT 0,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (SetID) REFERENCES SetsQuirurgicos(SetID),
    FOREIGN KEY (UsuarioResponsable) REFERENCES Usuarios(UsuarioID)
);

-- Tabla de Conteos de Instrumentos
CREATE TABLE ConteosInstrumentos (
    ConteoID INT IDENTITY(1,1) PRIMARY KEY,
    ProcedimientoID INT NOT NULL,
    InstrumentoID INT NOT NULL,
    TipoConteo NVARCHAR(10) NOT NULL CHECK (TipoConteo IN ('INICIAL', 'FINAL')),
    CantidadContada INT NOT NULL,
    CantidadEsperada INT NOT NULL,
    FotografiaPath NVARCHAR(500) NULL,
    UsuarioConteo INT NOT NULL,
    FechaConteo DATETIME DEFAULT GETDATE(),
    Observaciones NVARCHAR(500) NULL,
    FOREIGN KEY (ProcedimientoID) REFERENCES ProcedimientosQuirurgicos(ProcedimientoID),
    FOREIGN KEY (InstrumentoID) REFERENCES Instrumentos(InstrumentoID),
    FOREIGN KEY (UsuarioConteo) REFERENCES Usuarios(UsuarioID)
);

-- Tabla de Ciclos de Esterilización
CREATE TABLE CiclosEsterilizacion (
    CicloID INT IDENTITY(1,1) PRIMARY KEY,
    CodigoCiclo NVARCHAR(50) UNIQUE NOT NULL,
    FechaEsterilizacion DATETIME NOT NULL,
    MetodoEsterilizacion NVARCHAR(50) NOT NULL,
    TemperaturaGrados DECIMAL(5,2) NULL,
    TiempoMinutos INT NULL,
    UsuarioResponsable INT NOT NULL,
    Observaciones NVARCHAR(500) NULL,
    FOREIGN KEY (UsuarioResponsable) REFERENCES Usuarios(UsuarioID)
);

-- Tabla de relación Instrumentos-Esterilización
CREATE TABLE InstrumentosEsterilizacion (
    InstrumentoEsterilizacionID INT IDENTITY(1,1) PRIMARY KEY,
    InstrumentoID INT NOT NULL,
    CicloID INT NOT NULL,
    FechaAsignacion DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (InstrumentoID) REFERENCES Instrumentos(InstrumentoID),
    FOREIGN KEY (CicloID) REFERENCES CiclosEsterilizacion(CicloID)
);

-- Tabla de Alertas
CREATE TABLE Alertas (
    AlertaID INT IDENTITY(1,1) PRIMARY KEY,
    ProcedimientoID INT NULL,
    InstrumentoID INT NULL,
    TipoAlerta NVARCHAR(50) NOT NULL,
    Mensaje NVARCHAR(500) NOT NULL,
    Prioridad NVARCHAR(10) DEFAULT 'MEDIA' CHECK (Prioridad IN ('BAJA', 'MEDIA', 'ALTA', 'CRITICA')),
    Resuelta BIT DEFAULT 0,
    FechaCreacion DATETIME DEFAULT GETDATE(),
    FechaResolucion DATETIME NULL,
    UsuarioResolucion INT NULL,
    FOREIGN KEY (ProcedimientoID) REFERENCES ProcedimientosQuirurgicos(ProcedimientoID),
    FOREIGN KEY (InstrumentoID) REFERENCES Instrumentos(InstrumentoID),
    FOREIGN KEY (UsuarioResolucion) REFERENCES Usuarios(UsuarioID)
);

-- Tabla de Fotografías
CREATE TABLE Fotografias (
    FotografiaID INT IDENTITY(1,1) PRIMARY KEY,
    ProcedimientoID INT NULL,
    InstrumentoID INT NULL,
    RutaArchivo NVARCHAR(500) NOT NULL,
    TipoFotografia NVARCHAR(50) NOT NULL, -- 'CONTEO_INICIAL', 'CONTEO_FINAL', 'HISTORIAL_INSTRUMENTO'
    FechaCaptura DATETIME DEFAULT GETDATE(),
    UsuarioCaptura INT NOT NULL,
    FOREIGN KEY (ProcedimientoID) REFERENCES ProcedimientosQuirurgicos(ProcedimientoID),
    FOREIGN KEY (InstrumentoID) REFERENCES Instrumentos(InstrumentoID),
    FOREIGN KEY (UsuarioCaptura) REFERENCES Usuarios(UsuarioID)
);

-- Tabla de Auditoría
CREATE TABLE AuditoriaAcciones (
    AuditoriaID INT IDENTITY(1,1) PRIMARY KEY,
    UsuarioID INT NOT NULL,
    Accion NVARCHAR(100) NOT NULL,
    TablaAfectada NVARCHAR(50) NOT NULL,
    RegistroID INT NULL,
    ValoresAnteriores NVARCHAR(MAX) NULL,
    ValoresNuevos NVARCHAR(MAX) NULL,
    FechaAccion DATETIME DEFAULT GETDATE(),
    DireccionIP NVARCHAR(45) NULL,
    FOREIGN KEY (UsuarioID) REFERENCES Usuarios(UsuarioID)
);

-- Índices para mejorar el rendimiento
CREATE INDEX IX_ProcedimientosQuirurgicos_Fecha ON ProcedimientosQuirurgicos(FechaProcedimiento);
CREATE INDEX IX_ConteosInstrumentos_Procedimiento ON ConteosInstrumentos(ProcedimientoID);
CREATE INDEX IX_Instrumentos_Estado ON Instrumentos(EstadoID);
CREATE INDEX IX_Alertas_NoResuelta ON Alertas(Resuelta, FechaCreacion);
CREATE INDEX IX_AuditoriaAcciones_Usuario_Fecha ON AuditoriaAcciones(UsuarioID, FechaAccion);

PRINT 'Tablas creadas exitosamente.';
