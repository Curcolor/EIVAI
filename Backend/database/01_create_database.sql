-- Script de creación de base de datos para Sistema de Gestión de Instrumental Quirúrgico
-- Versión: 1.0
-- Fecha: 26/05/2025

USE master;
GO

-- Verificar si la base de datos existe y eliminarla si es necesario
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'EIVEI_DB')
BEGIN
    ALTER DATABASE EIVEI_DB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE EIVEI_DB;
END
GO

-- Crear la base de datos
CREATE DATABASE EIVEI_DB
ON 
(
    NAME = 'EIVEI_DB_Data',
    FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\EIVEI_DB.mdf',
    SIZE = 100MB,
    MAXSIZE = 1GB,
    FILEGROWTH = 10MB
)
LOG ON 
(
    NAME = 'EIVEI_DB_Log',
    FILENAME = 'C:\Program Files\Microsoft SQL Server\MSSQL15.MSSQLSERVER\MSSQL\DATA\EIVEI_DB.ldf',
    SIZE = 10MB,
    MAXSIZE = 100MB,
    FILEGROWTH = 5MB
);
GO

-- Usar la base de datos creada
USE EIVEI_DB;
GO

-- Configurar opciones de base de datos
ALTER DATABASE EIVEI_DB SET RECOVERY FULL;
ALTER DATABASE EIVEI_DB SET AUTO_CLOSE OFF;
ALTER DATABASE EIVEI_DB SET AUTO_SHRINK OFF;
GO

PRINT 'Base de datos EIVEI_DB creada exitosamente.';
