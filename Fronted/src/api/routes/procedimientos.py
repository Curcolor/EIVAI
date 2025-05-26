"""
Rutas API para procedimientos quirúrgicos
"""
from typing import List
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.api.schemas import (
    ProcedimientoQuirurgicoCreate, ProcedimientoQuirurgicoUpdate, 
    ProcedimientoQuirurgicoResponse, ResponseMessage
)
from src.api.controllers.procedimiento_controller import ProcedimientoController

router = APIRouter(prefix="/api/procedimientos", tags=["Procedimientos"])
procedimiento_controller = ProcedimientoController()

@router.post("/", response_model=ProcedimientoQuirurgicoResponse, status_code=201)
async def create_procedimiento(
    procedimiento: ProcedimientoQuirurgicoCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo procedimiento quirúrgico
    """
    return await procedimiento_controller.create_procedimiento(db, procedimiento)

@router.get("/", response_model=List[ProcedimientoQuirurgicoResponse])
async def get_procedimientos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de procedimientos con paginación
    """
    return await procedimiento_controller.get_procedimientos(db, skip=skip, limit=limit)

@router.get("/activos", response_model=List[ProcedimientoQuirurgicoResponse])
async def get_procedimientos_activos(
    db: Session = Depends(get_db)
):
    """
    Obtener procedimientos activos (INICIADO o EN_PROCESO)
    """
    return await procedimiento_controller.get_procedimientos_activos(db)

@router.get("/fecha/{fecha}", response_model=List[ProcedimientoQuirurgicoResponse])
async def get_procedimientos_por_fecha(
    fecha: date,
    db: Session = Depends(get_db)
):
    """
    Obtener procedimientos por fecha específica
    """
    return await procedimiento_controller.get_procedimientos_por_fecha(db, fecha)

@router.get("/{procedimiento_id}", response_model=ProcedimientoQuirurgicoResponse)
async def get_procedimiento(
    procedimiento_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener procedimiento específico por ID
    """
    return await procedimiento_controller.get_procedimiento(db, procedimiento_id)

@router.put("/{procedimiento_id}", response_model=ProcedimientoQuirurgicoResponse)
async def update_procedimiento(
    procedimiento_id: int,
    procedimiento: ProcedimientoQuirurgicoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar información de procedimiento
    """
    return await procedimiento_controller.update_procedimiento(db, procedimiento_id, procedimiento)

@router.post("/{procedimiento_id}/finalizar", response_model=ResponseMessage)
async def finalizar_procedimiento(
    procedimiento_id: int,
    db: Session = Depends(get_db)
):
    """
    Finalizar un procedimiento quirúrgico
    """
    return await procedimiento_controller.finalizar_procedimiento(db, procedimiento_id)
