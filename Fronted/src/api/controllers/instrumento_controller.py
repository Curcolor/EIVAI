"""
Controlador para la gestión de instrumentos
"""
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.api.schemas import (
    InstrumentoCreate, InstrumentoUpdate, InstrumentoResponse,
    EstadisticasInstrumento, ResponseMessage
)
from src.services.instrumento_service import InstrumentoService
from src.api.models.instrumento import Instrumento

class InstrumentoController:
    def __init__(self):
        self.instrumento_service = InstrumentoService()
    
    async def create_instrumento(self, db: Session, instrumento_data: InstrumentoCreate) -> InstrumentoResponse:
        """Crear nuevo instrumento"""
        try:
            # Verificar que no existe un instrumento con el mismo código
            existing = self.instrumento_service.get_by_codigo(db, instrumento_data.codigo_instrumento)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un instrumento con este código"
                )
            
            # Crear instrumento
            instrumento = self.instrumento_service.create(db, instrumento_data.dict())
            
            # Cargar con relaciones
            instrumento_completo = self.instrumento_service.get_with_estado(db, instrumento.instrumento_id)
            return InstrumentoResponse.from_orm(instrumento_completo)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear instrumento: {str(e)}"
            )
    
    async def get_instrumentos(self, db: Session, skip: int = 0, limit: int = 100) -> List[InstrumentoResponse]:
        """Obtener lista de instrumentos"""
        try:
            instrumentos = self.instrumento_service.get_all(db, skip=skip, limit=limit)
            # Cargar con estados
            response = []
            for instrumento in instrumentos:
                instrumento_completo = self.instrumento_service.get_with_estado(db, instrumento.instrumento_id)
                response.append(InstrumentoResponse.from_orm(instrumento_completo))
            return response
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener instrumentos: {str(e)}"
            )
    
    async def get_instrumento(self, db: Session, instrumento_id: int) -> InstrumentoResponse:
        """Obtener instrumento por ID"""
        try:
            instrumento = self.instrumento_service.get_with_estado(db, instrumento_id)
            if not instrumento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Instrumento no encontrado"
                )
            return InstrumentoResponse.from_orm(instrumento)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener instrumento: {str(e)}"
            )
    
    async def get_instrumento_by_codigo(self, db: Session, codigo: str) -> InstrumentoResponse:
        """Obtener instrumento por código"""
        try:
            instrumento = self.instrumento_service.get_by_codigo(db, codigo)
            if not instrumento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Instrumento no encontrado"
                )
            # Cargar con estado
            instrumento_completo = self.instrumento_service.get_with_estado(db, instrumento.instrumento_id)
            return InstrumentoResponse.from_orm(instrumento_completo)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener instrumento: {str(e)}"
            )
    
    async def update_instrumento(self, db: Session, instrumento_id: int, instrumento_data: InstrumentoUpdate) -> InstrumentoResponse:
        """Actualizar instrumento"""
        try:
            # Verificar que existe
            instrumento_existente = self.instrumento_service.get_by_id(db, instrumento_id)
            if not instrumento_existente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Instrumento no encontrado"
                )
            
            # Preparar datos para actualizar
            update_data = {k: v for k, v in instrumento_data.dict().items() if v is not None}
            
            # Actualizar
            instrumento = self.instrumento_service.update(db, instrumento_id, update_data)
            
            # Cargar con relaciones
            instrumento_completo = self.instrumento_service.get_with_estado(db, instrumento.instrumento_id)
            return InstrumentoResponse.from_orm(instrumento_completo)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar instrumento: {str(e)}"
            )
    
    async def get_instrumentos_por_estado(self, db: Session, estado_id: int) -> List[InstrumentoResponse]:
        """Obtener instrumentos por estado"""
        try:
            instrumentos = self.instrumento_service.get_by_estado(db, estado_id)
            response = []
            for instrumento in instrumentos:
                instrumento_completo = self.instrumento_service.get_with_estado(db, instrumento.instrumento_id)
                response.append(InstrumentoResponse.from_orm(instrumento_completo))
            return response
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener instrumentos por estado: {str(e)}"
            )
    
    async def get_instrumentos_mantenimiento(self, db: Session) -> List[InstrumentoResponse]:
        """Obtener instrumentos que requieren mantenimiento"""
        try:
            instrumentos = self.instrumento_service.get_que_requieren_mantenimiento(db)
            response = []
            for instrumento in instrumentos:
                instrumento_completo = self.instrumento_service.get_with_estado(db, instrumento.instrumento_id)
                response.append(InstrumentoResponse.from_orm(instrumento_completo))
            return response
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener instrumentos en mantenimiento: {str(e)}"
            )
    
    async def buscar_instrumentos(self, db: Session, termino: str) -> List[InstrumentoResponse]:
        """Buscar instrumentos por nombre"""
        try:
            instrumentos = self.instrumento_service.buscar_por_nombre(db, termino)
            response = []
            for instrumento in instrumentos:
                instrumento_completo = self.instrumento_service.get_with_estado(db, instrumento.instrumento_id)
                response.append(InstrumentoResponse.from_orm(instrumento_completo))
            return response
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al buscar instrumentos: {str(e)}"
            )
    
    async def incrementar_uso(self, db: Session, instrumento_id: int) -> ResponseMessage:
        """Incrementar contador de uso"""
        try:
            success = self.instrumento_service.incrementar_uso(db, instrumento_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Instrumento no encontrado"
                )
            return ResponseMessage(message="Contador de uso incrementado exitosamente")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al incrementar uso: {str(e)}"
            )
    
    async def get_estadisticas_uso(self, db: Session) -> List[EstadisticasInstrumento]:
        """Obtener estadísticas de uso de instrumentos"""
        try:
            # Esta función la implementaremos más adelante con consultas más complejas
            instrumentos = self.instrumento_service.get_all(db, limit=50)
            estadisticas = []
            
            for instrumento in instrumentos:
                instrumento_completo = self.instrumento_service.get_with_estado(db, instrumento.instrumento_id)
                estadisticas.append(EstadisticasInstrumento(
                    instrumento_id=instrumento.instrumento_id,
                    codigo_instrumento=instrumento.codigo_instrumento,
                    nombre_instrumento=instrumento.nombre_instrumento,
                    contador_uso=instrumento.contador_uso,
                    estado_actual=instrumento_completo.estado.nombre_estado if instrumento_completo.estado else "Sin estado",
                    procedimientos_recientes=0  # Por ahora 0, implementar después
                ))
            
            # Ordenar por uso descendente
            estadisticas.sort(key=lambda x: x.contador_uso, reverse=True)
            return estadisticas
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener estadísticas: {str(e)}"
            )
