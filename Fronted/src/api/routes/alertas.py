"""
Rutas API para gestión de alertas del sistema
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..middlewares.auth_middleware import require_auth
from ..schemas import (
    AlertaCreateSchema, 
    AlertaResponse, 
    AlertaUpdateSchema,
    PaginationParams,
    ResponseMessage
)
from ...services.alerta_service import AlertaService
from ...config.database import get_db

router = APIRouter(prefix="/api/alertas", tags=["Alertas"])
alerta_service = AlertaService()


@router.post("", response_model=AlertaResponse)
async def crear_alerta(
    alerta_data: AlertaCreateSchema,
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Crear una nueva alerta
    """
    try:
        alerta = await alerta_service.crear_alerta(
            db=db,
            alerta_data=alerta_data.dict(),
            usuario_id=usuario_actual.usuario_id
        )
        return alerta
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[AlertaResponse])
async def listar_alertas(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(),
    prioridad: Optional[str] = Query(None, description="Filtrar por prioridad"),
    resuelta: Optional[bool] = Query(None, description="Filtrar por estado resuelto"),
    tipo_alerta: Optional[str] = Query(None, description="Filtrar por tipo de alerta"),
    usuario_actual = Depends(require_auth)
):
    """
    Listar alertas con filtros opcionales
    """
    try:
        filtros = {}
        if prioridad:
            filtros['prioridad'] = prioridad
        if resuelta is not None:
            filtros['resuelta'] = resuelta
        if tipo_alerta:
            filtros['tipo_alerta'] = tipo_alerta
            
        alertas = await alerta_service.listar_alertas(
            db=db,
            skip=pagination.skip,
            limit=pagination.limit,
            filtros=filtros
        )
        return alertas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{alerta_id}", response_model=AlertaResponse)
async def obtener_alerta(
    alerta_id: int,
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Obtener alerta específica
    """
    try:
        alerta = await alerta_service.obtener_alerta(db=db, alerta_id=alerta_id)
        if not alerta:
            raise HTTPException(status_code=404, detail="Alerta no encontrada")
        return alerta
    except Exception as e:
        if "no encontrada" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{alerta_id}", response_model=AlertaResponse)
async def actualizar_alerta(
    alerta_id: int,
    alerta_data: AlertaUpdateSchema,
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Actualizar una alerta
    """
    try:
        alerta = await alerta_service.actualizar_alerta(
            db=db,
            alerta_id=alerta_id,
            datos_actualizacion=alerta_data.dict(exclude_unset=True)
        )
        return alerta
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if "no encontrada" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{alerta_id}", response_model=ResponseMessage)
async def eliminar_alerta(
    alerta_id: int,
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Eliminar una alerta
    """
    try:
        await alerta_service.eliminar_alerta(db=db, alerta_id=alerta_id)
        return ResponseMessage(message="Alerta eliminada exitosamente")
    except Exception as e:
        if "no encontrada" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/criticas/lista", response_model=List[AlertaResponse])
async def obtener_alertas_criticas(
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Obtener todas las alertas críticas sin resolver
    """
    try:
        alertas = await alerta_service.obtener_alertas_criticas(db=db)
        return alertas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{alerta_id}/resolver", response_model=ResponseMessage)
async def resolver_alerta(
    alerta_id: int,
    observaciones: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Marcar una alerta como resuelta
    """
    try:
        await alerta_service.resolver_alerta(
            db=db,
            alerta_id=alerta_id,
            usuario_id=usuario_actual.usuario_id,
            observaciones=observaciones
        )
        return ResponseMessage(message="Alerta resuelta exitosamente")
    except Exception as e:
        if "no encontrada" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estadisticas/resumen")
async def obtener_estadisticas_alertas(
    db: Session = Depends(get_db),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicio (YYYY-MM-DD)"),
    fecha_fin: Optional[str] = Query(None, description="Fecha fin (YYYY-MM-DD)"),
    usuario_actual = Depends(require_auth)
):
    """
    Obtener estadísticas de alertas
    """
    try:
        estadisticas = await alerta_service.obtener_estadisticas(
            db=db,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        return estadisticas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))