"""
Rutas API para gestión de sets quirúrgicos
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..middlewares.auth_middleware import require_auth
from ..schemas import (
    SetQuirurgicoCreate, 
    SetQuirurgicoResponse,
    PaginationParams,
    ResponseMessage
)
from ...services.set_service import SetService
from ...config.database import get_db

router = APIRouter(prefix="/api/sets", tags=["Sets Quirúrgicos"])
set_service = SetService()


@router.post("", response_model=SetQuirurgicoResponse)
async def crear_set(
    set_data: SetQuirurgicoCreate,
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Crear un nuevo set quirúrgico
    """
    try:
        set_quirurgico = await set_service.crear_set(
            db=db,
            set_data=set_data.dict(),
            usuario_id=usuario_actual.usuario_id
        )
        return set_quirurgico
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[SetQuirurgicoResponse])
async def listar_sets(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(),
    especialidad: Optional[str] = Query(None, description="Filtrar por especialidad"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    usuario_actual = Depends(require_auth)
):
    """
    Listar sets quirúrgicos con filtros opcionales
    """
    try:
        filtros = {}
        if especialidad:
            filtros['especialidad'] = especialidad
        if activo is not None:
            filtros['activo'] = activo
            
        sets = await set_service.listar_sets(
            db=db,
            skip=pagination.skip,
            limit=pagination.limit,
            filtros=filtros
        )
        return sets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{set_id}", response_model=SetQuirurgicoResponse)
async def obtener_set(
    set_id: int,
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Obtener set quirúrgico específico
    """
    try:
        set_quirurgico = await set_service.obtener_set(db=db, set_id=set_id)
        if not set_quirurgico:
            raise HTTPException(status_code=404, detail="Set quirúrgico no encontrado")
        return set_quirurgico
    except Exception as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{set_id}", response_model=SetQuirurgicoResponse)
async def actualizar_set(
    set_id: int,
    nombre: Optional[str] = None,
    descripcion: Optional[str] = None,
    especialidad: Optional[str] = None,
    activo: Optional[bool] = None,
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Actualizar un set quirúrgico
    """
    try:
        datos_actualizacion = {}
        if nombre is not None:
            datos_actualizacion['nombre'] = nombre
        if descripcion is not None:
            datos_actualizacion['descripcion'] = descripcion
        if especialidad is not None:
            datos_actualizacion['especialidad'] = especialidad
        if activo is not None:
            datos_actualizacion['activo'] = activo
            
        set_quirurgico = await set_service.actualizar_set(
            db=db,
            set_id=set_id,
            datos_actualizacion=datos_actualizacion
        )
        return set_quirurgico
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{set_id}", response_model=ResponseMessage)
async def eliminar_set(
    set_id: int,
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Eliminar un set quirúrgico
    """
    try:
        await set_service.eliminar_set(db=db, set_id=set_id)
        return ResponseMessage(message="Set quirúrgico eliminado exitosamente")
    except Exception as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{set_id}/instrumentos/{instrumento_id}")
async def agregar_instrumento_a_set(
    set_id: int,
    instrumento_id: int,
    cantidad: int = 1,
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Agregar un instrumento a un set quirúrgico
    """
    try:
        await set_service.agregar_instrumento_a_set(
            db=db,
            set_id=set_id,
            instrumento_id=instrumento_id,
            cantidad=cantidad
        )
        return ResponseMessage(message="Instrumento agregado al set exitosamente")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{set_id}/instrumentos/{instrumento_id}")
async def remover_instrumento_de_set(
    set_id: int,
    instrumento_id: int,
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Remover un instrumento de un set quirúrgico
    """
    try:
        await set_service.remover_instrumento_de_set(
            db=db,
            set_id=set_id,
            instrumento_id=instrumento_id
        )
        return ResponseMessage(message="Instrumento removido del set exitosamente")
    except Exception as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{set_id}/instrumentos")
async def obtener_instrumentos_del_set(
    set_id: int,
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Obtener todos los instrumentos de un set quirúrgico
    """
    try:
        instrumentos = await set_service.obtener_instrumentos_del_set(
            db=db,
            set_id=set_id
        )
        return instrumentos
    except Exception as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))