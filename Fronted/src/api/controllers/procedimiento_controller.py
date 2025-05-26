"""
Controlador para la gestión de procedimientos quirúrgicos
"""
from typing import List
from datetime import datetime, date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from src.api.schemas import (
    ProcedimientoQuirurgicoCreate, ProcedimientoQuirurgicoUpdate, 
    ProcedimientoQuirurgicoResponse, ResponseMessage
)
from src.services.base_service import BaseService
from src.api.models.procedimiento_quirurgico import ProcedimientoQuirurgico
from src.api.models.set_quirurgico import SetQuirurgico
from src.api.models.usuario import Usuario

class ProcedimientoController:
    def __init__(self):
        self.procedimiento_service = BaseService(ProcedimientoQuirurgico)
    
    async def create_procedimiento(self, db: Session, procedimiento_data: ProcedimientoQuirurgicoCreate) -> ProcedimientoQuirurgicoResponse:
        """Crear nuevo procedimiento quirúrgico"""
        try:
            # Verificar que el set quirúrgico existe
            set_quirurgico = db.query(SetQuirurgico).filter(SetQuirurgico.set_id == procedimiento_data.set_id).first()
            if not set_quirurgico:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Set quirúrgico no encontrado"
                )
            
            # Verificar que el usuario responsable existe
            usuario = db.query(Usuario).filter(Usuario.usuario_id == procedimiento_data.usuario_responsable).first()
            if not usuario:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario responsable no encontrado"
                )
            
            # Crear procedimiento
            procedimiento_dict = procedimiento_data.dict()
            procedimiento_dict['estado_procedimiento'] = 'INICIADO'
            procedimiento_dict['fecha_creacion'] = datetime.utcnow()
            
            procedimiento = self.procedimiento_service.create(db, procedimiento_dict)
            
            # Cargar con relaciones
            procedimiento_completo = db.query(ProcedimientoQuirurgico).options(
                joinedload(ProcedimientoQuirurgico.set_quirurgico),
                joinedload(ProcedimientoQuirurgico.usuario_responsable_rel)
            ).filter(ProcedimientoQuirurgico.procedimiento_id == procedimiento.procedimiento_id).first()
            
            return ProcedimientoQuirurgicoResponse.from_orm(procedimiento_completo)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear procedimiento: {str(e)}"
            )
    
    async def get_procedimientos(self, db: Session, skip: int = 0, limit: int = 100) -> List[ProcedimientoQuirurgicoResponse]:
        """Obtener lista de procedimientos"""
        try:
            procedimientos = db.query(ProcedimientoQuirurgico).options(
                joinedload(ProcedimientoQuirurgico.set_quirurgico),
                joinedload(ProcedimientoQuirurgico.usuario_responsable_rel)
            ).offset(skip).limit(limit).all()
            
            return [ProcedimientoQuirurgicoResponse.from_orm(proc) for proc in procedimientos]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener procedimientos: {str(e)}"
            )
    
    async def get_procedimiento(self, db: Session, procedimiento_id: int) -> ProcedimientoQuirurgicoResponse:
        """Obtener procedimiento por ID"""
        try:
            procedimiento = db.query(ProcedimientoQuirurgico).options(
                joinedload(ProcedimientoQuirurgico.set_quirurgico),
                joinedload(ProcedimientoQuirurgico.usuario_responsable_rel)
            ).filter(ProcedimientoQuirurgico.procedimiento_id == procedimiento_id).first()
            
            if not procedimiento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Procedimiento no encontrado"
                )
            
            return ProcedimientoQuirurgicoResponse.from_orm(procedimiento)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener procedimiento: {str(e)}"
            )
    
    async def update_procedimiento(self, db: Session, procedimiento_id: int, procedimiento_data: ProcedimientoQuirurgicoUpdate) -> ProcedimientoQuirurgicoResponse:
        """Actualizar procedimiento"""
        try:
            # Verificar que existe
            procedimiento_existente = self.procedimiento_service.get_by_id(db, procedimiento_id)
            if not procedimiento_existente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Procedimiento no encontrado"
                )
            
            # Preparar datos para actualizar
            update_data = {k: v for k, v in procedimiento_data.dict().items() if v is not None}
            
            # Actualizar
            procedimiento = self.procedimiento_service.update(db, procedimiento_id, update_data)
            
            # Cargar con relaciones
            procedimiento_completo = db.query(ProcedimientoQuirurgico).options(
                joinedload(ProcedimientoQuirurgico.set_quirurgico),
                joinedload(ProcedimientoQuirurgico.usuario_responsable_rel)
            ).filter(ProcedimientoQuirurgico.procedimiento_id == procedimiento.procedimiento_id).first()
            
            return ProcedimientoQuirurgicoResponse.from_orm(procedimiento_completo)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar procedimiento: {str(e)}"
            )
    
    async def get_procedimientos_activos(self, db: Session) -> List[ProcedimientoQuirurgicoResponse]:
        """Obtener procedimientos activos (INICIADO o EN_PROCESO)"""
        try:
            procedimientos = db.query(ProcedimientoQuirurgico).options(
                joinedload(ProcedimientoQuirurgico.set_quirurgico),
                joinedload(ProcedimientoQuirurgico.usuario_responsable_rel)
            ).filter(
                ProcedimientoQuirurgico.estado_procedimiento.in_(['INICIADO', 'EN_PROCESO'])
            ).all()
            
            return [ProcedimientoQuirurgicoResponse.from_orm(proc) for proc in procedimientos]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener procedimientos activos: {str(e)}"
            )
    
    async def get_procedimientos_por_fecha(self, db: Session, fecha: date) -> List[ProcedimientoQuirurgicoResponse]:
        """Obtener procedimientos por fecha"""
        try:
            # Convertir fecha a rango de datetime
            fecha_inicio = datetime.combine(fecha, datetime.min.time())
            fecha_fin = datetime.combine(fecha, datetime.max.time())
            
            procedimientos = db.query(ProcedimientoQuirurgico).options(
                joinedload(ProcedimientoQuirurgico.set_quirurgico),
                joinedload(ProcedimientoQuirurgico.usuario_responsable_rel)
            ).filter(
                ProcedimientoQuirurgico.fecha_procedimiento >= fecha_inicio,
                ProcedimientoQuirurgico.fecha_procedimiento <= fecha_fin
            ).all()
            
            return [ProcedimientoQuirurgicoResponse.from_orm(proc) for proc in procedimientos]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener procedimientos por fecha: {str(e)}"
            )
    
    async def finalizar_procedimiento(self, db: Session, procedimiento_id: int) -> ResponseMessage:
        """Finalizar un procedimiento (cambiar estado a FINALIZADO)"""
        try:
            # Verificar que existe
            procedimiento = self.procedimiento_service.get_by_id(db, procedimiento_id)
            if not procedimiento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Procedimiento no encontrado"
                )
            
            # Verificar que se pueden finalizar (conteos completos)
            if not procedimiento.conteo_inicial_completo:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede finalizar: conteo inicial incompleto"
                )
            
            if not procedimiento.conteo_final_completo:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede finalizar: conteo final incompleto"
                )
            
            # Actualizar estado
            self.procedimiento_service.update(db, procedimiento_id, {
                'estado_procedimiento': 'FINALIZADO'
            })
            
            return ResponseMessage(message="Procedimiento finalizado exitosamente")
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al finalizar procedimiento: {str(e)}"
            )
