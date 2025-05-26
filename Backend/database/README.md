# Sistema de Gestión de Instrumental Quirúrgico - Base de Datos

Este directorio contiene todos los scripts SQL necesarios para crear y configurar la base de datos del Sistema de Gestión de Instrumental Quirúrgico.

## Estructura de Archivos

### Scripts Principales
- **`01_create_database.sql`** - Creación de la base de datos
- **`02_create_tables.sql`** - Creación de todas las tablas
- **`03_insert_initial_data.sql`** - Inserción de datos iniciales
- **`04_stored_procedures.sql`** - Procedimientos almacenados
- **`05_views.sql`** - Vistas del sistema
- **`06_functions_triggers.sql`** - Funciones y triggers

## Características del Sistema

### Funcionalidades Implementadas

1. **Gestión de Usuarios**
   - Perfiles de instrumentadores con inicio de sesión
   - Auditoría de acciones por usuario
   - Trazabilidad de responsabilidades

2. **Gestión de Sets Quirúrgicos**
   - Registro de sets con número de identificación
   - Relación de instrumentos por set
   - Validación de disponibilidad

3. **Control de Instrumentos**
   - Estados: En buen estado, Desgaste leve, Requiere mantenimiento
   - Contador de uso automático
   - Historial de esterilización

4. **Conteo de Instrumentos**
   - Conteo inicial y final con fotografías
   - Detección automática de discrepancias
   - Alertas en tiempo real

5. **Trazabilidad Completa**
   - Historial de uso por procedimiento
   - Registro de ciclos de esterilización
   - Auditoría completa de cambios

6. **Sistema de Alertas**
   - Alertas críticas para conteos incorrectos
   - Notificaciones de mantenimiento requerido
   - Validación de esterilización

7. **Reportes y Estadísticas**
   - Informes automáticos de procedimientos
   - Estadísticas de uso de instrumentos
   - Dashboard de actividad diaria

### Tablas Principales

- **`Usuarios`** - Instrumentadores y personal del sistema
- **`SetsQuirurgicos`** - Sets de instrumental por procedimiento
- **`Instrumentos`** - Catálogo de instrumentos quirúrgicos
- **`ProcedimientosQuirurgicos`** - Registro de cirugías
- **`ConteosInstrumentos`** - Conteos inicial y final
- **`CiclosEsterilizacion`** - Registro de esterilización
- **`Alertas`** - Sistema de notificaciones
- **`AuditoriaAcciones`** - Trazabilidad de cambios

### Vistas Principales

- **`vw_ResumenProcedimientos`** - Vista general de procedimientos
- **`vw_EstadoInstrumentos`** - Estado actual de todos los instrumentos
- **`vw_AlertasActivas`** - Alertas pendientes de resolución
- **`vw_DashboardActividadDiaria`** - Resumen de actividad del día
- **`vw_TrazabilidadInstrumentos`** - Historial completo por instrumento

### Procedimientos Almacenados Principales

- **`sp_IniciarProcedimientoQuirurgico`** - Iniciar nueva cirugía
- **`sp_RegistrarConteoInicial`** - Conteo inicial de instrumentos
- **`sp_RegistrarConteoFinal`** - Conteo final con validaciones
- **`sp_RegistrarCicloEsterilizacion`** - Registro de esterilización
- **`sp_GenerarReporteProcedimiento`** - Reporte completo de procedimiento

## Datos Iniciales

### Usuarios Predeterminados
- **admin** - Administrador del Sistema
- **instrumentador1** - María García López
- **instrumentador2** - Carlos Rodríguez Pérez

### Sets Quirúrgicos
- **CESAREA-001** - Equipo de cesárea
- **LAPARO-001** - Equipo de laparoscopia
- **GENERAL-001** - Equipo de cirugía general
- **CESAREA-002** - Equipo de cesárea (Backup)

### Instrumentos Básicos
- Bisturíes (#11, #15)
- Pinzas (Kelly, Allis)
- Tijeras (Mayo, Metzenbaum)
- Portaagujas
- Separadores
- Aspiradores
- Gasas estériles

## Requisitos Técnicos

- **SQL Server 2016 o superior**
- **Memoria**: Mínimo 512 MB para la base de datos
- **Espacio en disco**: 1 GB máximo (configurado para crecimiento automático)
- **Permisos**: dbcreator y sysadmin para la instalación

## Consideraciones de Seguridad

1. **Cambiar contraseñas por defecto** antes de usar en producción
2. Implementar cifrado de contraseñas en la aplicación
3. Configurar respaldos automáticos
4. Establecer políticas de retención de auditoría
5. Implementar acceso basado en roles

## Mantenimiento

### Respaldos Recomendados
- **Completo**: Diario
- **Diferencial**: Cada 6 horas
- **Log de transacciones**: Cada 15 minutos

### Limpieza de Datos
- Auditoría: Mantener últimos 12 meses
- Fotografías: Archivar después de 24 meses
- Alertas resueltas: Mantener últimos 6 meses

## Soporte

Para dudas sobre la implementación o modificaciones, consulte:
1. Documentación de procedimientos almacenados
2. Comentarios en el código SQL
3. Vistas de ejemplo incluidas

---

**Versión**: 1.0  
**Fecha**: 26/05/2025  
**Compatibilidad**: SQL Server 2016+
