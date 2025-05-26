"""
Esquemas Pydantic para validación de datos de entrada y salida
"""
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr

# Esquemas base
class ResponseMessage(BaseModel):
    """Esquema para respuestas simples"""
    message: str
    success: bool = True

class PaginationParams(BaseModel):
    """Parámetros de paginación"""
    skip: int = Field(0, ge=0, description="Número de registros a omitir")
    limit: int = Field(100, ge=1, le=1000, description="Número máximo de registros")

# Esquemas de Usuario
class UsuarioBase(BaseModel):
    nombre_usuario: str = Field(..., min_length=3, max_length=50)
    nombre_completo: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    activo: bool = True

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6, max_length=100)

class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    email: Optional[EmailStr] = None
    activo: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    usuario_id: int
    fecha_creacion: datetime
    ultimo_acceso: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    usuario: UsuarioResponse
    token: str
    message: str

# Esquemas de Estado de Instrumento
class EstadoInstrumentoBase(BaseModel):
    nombre_estado: str = Field(..., min_length=1, max_length=50)
    descripcion: Optional[str] = Field(None, max_length=200)
    requiere_mantenimiento: bool = False

class EstadoInstrumentoCreate(EstadoInstrumentoBase):
    pass

class EstadoInstrumentoResponse(EstadoInstrumentoBase):
    estado_id: int
    
    class Config:
        from_attributes = True

# Esquemas de Instrumento
class InstrumentoBase(BaseModel):
    codigo_instrumento: str = Field(..., min_length=1, max_length=50)
    nombre_instrumento: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    estado_id: int

class InstrumentoCreate(InstrumentoBase):
    pass

class InstrumentoUpdate(BaseModel):
    nombre_instrumento: Optional[str] = None
    descripcion: Optional[str] = None
    estado_id: Optional[int] = None

class InstrumentoResponse(InstrumentoBase):
    instrumento_id: int
    contador_uso: int
    fecha_creacion: datetime
    ultima_esterilizacion: Optional[datetime] = None
    estado: Optional[EstadoInstrumentoResponse] = None
    
    class Config:
        from_attributes = True

# Esquemas de Set Quirúrgico
class SetQuirurgicoBase(BaseModel):
    nombre_set: str = Field(..., min_length=1, max_length=100)
    numero_identificacion: str = Field(..., min_length=1, max_length=50)
    tipo_procedimiento: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    activo: bool = True

class SetQuirurgicoCreate(SetQuirurgicoBase):
    pass

class SetQuirurgicoUpdate(BaseModel):
    nombre_set: Optional[str] = Field(None, min_length=1, max_length=100)
    numero_identificacion: Optional[str] = Field(None, min_length=1, max_length=50)
    tipo_procedimiento: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    activo: Optional[bool] = None

class SetQuirurgicoResponse(SetQuirurgicoBase):
    set_id: int
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True

# Esquemas de Procedimiento Quirúrgico
class ProcedimientoQuirurgicoBase(BaseModel):
    set_id: int
    usuario_responsable: int
    fecha_procedimiento: datetime
    tipo_cirugia: str = Field(..., min_length=1, max_length=100)
    paciente: str = Field(..., min_length=1, max_length=100)
    medico: str = Field(..., min_length=1, max_length=100)

class ProcedimientoQuirurgicoCreate(ProcedimientoQuirurgicoBase):
    pass

class ProcedimientoQuirurgicoUpdate(BaseModel):
    estado_procedimiento: Optional[str] = Field(None, pattern="^(INICIADO|EN_PROCESO|FINALIZADO|CANCELADO)$")
    conteo_inicial_completo: Optional[bool] = None
    conteo_final_completo: Optional[bool] = None

class ProcedimientoQuirurgicoResponse(ProcedimientoQuirurgicoBase):
    procedimiento_id: int
    estado_procedimiento: str
    conteo_inicial_completo: bool
    conteo_final_completo: bool
    fecha_creacion: datetime
    set_quirurgico: Optional[SetQuirurgicoResponse] = None
    usuario_responsable_rel: Optional[UsuarioResponse] = None
    
    class Config:
        from_attributes = True

# Esquemas de Conteo de Instrumentos
class ConteoInstrumentoBase(BaseModel):
    procedimiento_id: int
    instrumento_id: int
    tipo_conteo: str = Field(..., pattern="^(INICIAL|FINAL)$")
    cantidad_contada: int = Field(..., ge=0)
    cantidad_esperada: int = Field(..., ge=0)
    observaciones: Optional[str] = Field(None, max_length=500)

class ConteoInstrumentoCreate(ConteoInstrumentoBase):
    usuario_conteo: int
    fotografia_path: Optional[str] = None

class ConteoInstrumentoResponse(ConteoInstrumentoBase):
    conteo_id: int
    usuario_conteo: int
    fecha_conteo: datetime
    fotografia_path: Optional[str] = None
    tiene_discrepancia: bool
    instrumento: Optional[InstrumentoResponse] = None
    usuario_conteo_rel: Optional[UsuarioResponse] = None
    
    class Config:
        from_attributes = True

# Esquemas adicionales para Conteos
class ConteoCreateSchema(BaseModel):
    """Esquema para crear un nuevo conteo con fotos opcionales"""
    procedimiento_id: int
    instrumento_id: int
    tipo_conteo: str = Field(..., pattern="^(INICIAL|FINAL)$")
    cantidad_contada: int = Field(..., ge=0)
    cantidad_esperada: int = Field(..., ge=0)
    observaciones: Optional[str] = Field(None, max_length=500)

class ConteoUpdateSchema(BaseModel):
    """Esquema para actualizar un conteo existente"""
    cantidad_contada: Optional[int] = Field(None, ge=0)
    observaciones: Optional[str] = Field(None, max_length=500)
    discrepancia: Optional[bool] = None

class ConteoWithPhotosResponse(ConteoInstrumentoResponse):
    """Conteo con información de fotos asociadas"""
    fotos: List['FotoResponse'] = []

# Esquemas de Alertas
class AlertaBase(BaseModel):
    tipo_alerta: str = Field(..., min_length=1, max_length=50)
    mensaje: str = Field(..., min_length=1, max_length=500)
    prioridad: str = Field("MEDIA", pattern="^(BAJA|MEDIA|ALTA|CRITICA)$")

class AlertaCreate(AlertaBase):
    procedimiento_id: Optional[int] = None
    instrumento_id: Optional[int] = None

class AlertaResponse(AlertaBase):
    alerta_id: int
    procedimiento_id: Optional[int] = None
    instrumento_id: Optional[int] = None
    resuelta: bool
    fecha_creacion: datetime
    fecha_resolucion: Optional[datetime] = None
    usuario_resolucion: Optional[int] = None
    es_critica: bool
    esta_activa: bool
    
    class Config:
        from_attributes = True

# Esquemas adicionales para Alertas  
class AlertaCreateSchema(BaseModel):
    """Esquema para crear una nueva alerta"""
    tipo_alerta: str = Field(..., min_length=1, max_length=50)
    mensaje: str = Field(..., min_length=1, max_length=500)
    prioridad: str = Field("MEDIA", pattern="^(BAJA|MEDIA|ALTA|CRITICA)$")
    procedimiento_id: Optional[int] = None
    instrumento_id: Optional[int] = None

class AlertaUpdateSchema(BaseModel):
    """Esquema para actualizar una alerta"""
    resuelta: Optional[bool] = None
    observaciones_resolucion: Optional[str] = Field(None, max_length=500)

# Esquemas para Fotos
class FotoBase(BaseModel):
    nombre_archivo: str = Field(..., min_length=1, max_length=255)
    ruta_archivo: str = Field(..., min_length=1, max_length=500)
    tamaño_archivo: int = Field(..., ge=0)
    tipo_mime: str = Field(..., min_length=1, max_length=100)

class FotoCreate(FotoBase):
    conteo_id: int
    hash_archivo: Optional[str] = Field(None, max_length=32)

class FotoResponse(FotoBase):
    foto_id: int
    conteo_id: int
    fecha_subida: datetime
    hash_archivo: Optional[str] = None
    url_foto: Optional[str] = None
    url_thumbnail: Optional[str] = None
    
    class Config:
        from_attributes = True

# Esquemas para Dashboard
class DashboardStatsResponse(BaseModel):
    """Estadísticas principales del dashboard"""
    total_procedimientos_hoy: int
    procedimientos_activos: int
    alertas_pendientes: int
    alertas_criticas: int
    instrumentos_disponibles: int
    instrumentos_en_mantenimiento: int
    usuarios_activos_hoy: int
    sets_disponibles: int
    conteos_pendientes: int
    discrepancias_hoy: int

class AlertasSummaryResponse(BaseModel):
    """Resumen de alertas por tipo y prioridad"""
    total_alertas: int
    alertas_criticas: int
    alertas_altas: int
    alertas_medias: int
    alertas_bajas: int
    alertas_por_tipo: dict
    alertas_recientes: List[AlertaResponse]

class InstrumentoCriticoResponse(BaseModel):
    """Instrumento que requiere atención crítica"""
    instrumento_id: int
    codigo_instrumento: str
    nombre_instrumento: str
    estado_actual: str
    motivo_critico: str
    prioridad: str
    ultimo_uso: Optional[datetime] = None
    mantenimiento_vencido: bool
    
class ProcedimientoActivoResponse(BaseModel):
    """Procedimiento quirúrgico activo"""
    procedimiento_id: int
    tipo_cirugia: str
    paciente: str
    medico: str
    estado_procedimiento: str
    fecha_inicio: datetime
    duracion_minutos: int
    conteo_inicial_ok: bool
    conteo_final_ok: bool
    alertas_activas: int

class ConteoPendienteResponse(BaseModel):
    """Conteo pendiente de verificación"""
    conteo_id: int
    procedimiento_id: int
    instrumento_id: int
    codigo_instrumento: str
    nombre_instrumento: str
    tipo_conteo: str
    cantidad_contada: int
    cantidad_esperada: int
    tiene_discrepancia: bool
    fecha_conteo: datetime
    tiempo_pendiente_minutos: int

class EstadisticaUsoResponse(BaseModel):
    """Estadísticas de uso de instrumentos"""
    instrumento_id: int
    codigo_instrumento: str
    nombre_instrumento: str
    total_usos: int
    usos_periodo: int
    promedio_usos_mes: float
    tendencia: str  # 'CRECIENTE', 'DECRECIENTE', 'ESTABLE'
    
class TendenciaMantenimientoResponse(BaseModel):
    """Tendencias de mantenimiento"""
    mes: str
    total_mantenimientos: int
    mantenimientos_preventivos: int
    mantenimientos_correctivos: int
    costo_promedio: float
    tiempo_promedio_horas: float

class EficienciaQuirofanoResponse(BaseModel):
    """Métricas de eficiencia de quirófanos"""
    fecha: date
    total_procedimientos: int
    tiempo_promedio_procedimiento: float
    tiempo_preparacion_promedio: float
    tiempo_conteo_promedio: float
    discrepancias_porcentaje: float
    satisfaccion_score: float

class RealTimeDataResponse(BaseModel):
    """Datos en tiempo real para el dashboard"""
    timestamp: datetime
    procedimientos_en_curso: int
    alertas_nuevas_ultima_hora: int
    instrumentos_uso_actual: int
    personal_activo: int
    quirofanos_ocupados: int
    alertas_criticas_sin_resolver: int
    promedio_tiempo_conteo: float

# Esquemas de Estadísticas
class EstadisticasInstrumento(BaseModel):
    """Estadísticas de uso de instrumentos"""
    instrumento_id: int
    nombre_instrumento: str
    total_usos: int
    promedio_conteos_por_procedimiento: float
    tiempo_promedio_conteo: float
    ultima_vez_usado: Optional[datetime] = None
    estado_actual: str
    
    class Config:
        from_attributes = True

# Forward references para evitar problemas de imports circulares
ConteoWithPhotosResponse.model_rebuild()
