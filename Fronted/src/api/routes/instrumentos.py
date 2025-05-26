"""
Rutas API para instrumentos
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.api.schemas import (
    InstrumentoCreate, InstrumentoUpdate, InstrumentoResponse,
    EstadisticasInstrumento, ResponseMessage
)
from src.api.controllers.instrumento_controller import InstrumentoController

router = APIRouter(prefix="/api/instrumentos", tags=["Instrumentos"])
instrumento_controller = InstrumentoController()

@router.post("/", response_model=InstrumentoResponse, status_code=201)
async def create_instrumento(
    instrumento: InstrumentoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo instrumento
    """
    return await instrumento_controller.create_instrumento(db, instrumento)

@router.get("/", response_model=List[InstrumentoResponse])
async def get_instrumentos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de instrumentos con paginación
    """
    return await instrumento_controller.get_instrumentos(db, skip=skip, limit=limit)

@router.get("/estadisticas", response_model=List[EstadisticasInstrumento])
async def get_estadisticas_uso(
    db: Session = Depends(get_db)
):
    """
    Obtener estadísticas de uso de instrumentos
    """
    return await instrumento_controller.get_estadisticas_uso(db)

@router.get("/mantenimiento", response_model=List[InstrumentoResponse])
async def get_instrumentos_mantenimiento(
    db: Session = Depends(get_db)
):
    """
    Obtener instrumentos que requieren mantenimiento
    """
    return await instrumento_controller.get_instrumentos_mantenimiento(db)

@router.get("/buscar", response_model=List[InstrumentoResponse])
async def buscar_instrumentos(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    db: Session = Depends(get_db)
):
    """
    Buscar instrumentos por nombre
    """
    return await instrumento_controller.buscar_instrumentos(db, q)

@router.get("/codigo/{codigo}", response_model=InstrumentoResponse)
async def get_instrumento_by_codigo(
    codigo: str,
    db: Session = Depends(get_db)
):
    """
    Obtener instrumento por código
    """
    return await instrumento_controller.get_instrumento_by_codigo(db, codigo)

@router.get("/estado/{estado_id}", response_model=List[InstrumentoResponse])
async def get_instrumentos_por_estado(
    estado_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener instrumentos por estado
    """
    return await instrumento_controller.get_instrumentos_por_estado(db, estado_id)

@router.get("/{instrumento_id}", response_model=InstrumentoResponse)
async def get_instrumento(
    instrumento_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener instrumento específico por ID
    """
    return await instrumento_controller.get_instrumento(db, instrumento_id)

@router.put("/{instrumento_id}", response_model=InstrumentoResponse)
async def update_instrumento(
    instrumento_id: int,
    instrumento: InstrumentoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar información de instrumento
    """
    return await instrumento_controller.update_instrumento(db, instrumento_id, instrumento)

@router.post("/{instrumento_id}/incrementar-uso", response_model=ResponseMessage)
async def incrementar_uso(
    instrumento_id: int,
    db: Session = Depends(get_db)
):
    """
    Incrementar contador de uso del instrumento
    """
    return await instrumento_controller.incrementar_uso(db, instrumento_id)
