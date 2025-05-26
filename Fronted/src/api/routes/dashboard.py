# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\api\routes\dashboard.py
"""
Rutas API para el dashboard de estadísticas
"""
from typing import Optional
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...config.database import get_db
from ..middlewares.auth_middleware import require_auth
from ..controllers.dashboard_controller import DashboardController

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])
dashboard_controller = DashboardController()


@router.get("/stats")
async def get_dashboard_stats(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio para estadísticas"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin para estadísticas"),
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Obtener estadísticas generales del dashboard
    """
    return await dashboard_controller.get_dashboard_stats(
        db=db,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )


@router.get("/alertas-summary")
async def get_alertas_summary(
    limit: int = Query(5, ge=1, le=20, description="Número de alertas a mostrar"),
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Obtener resumen de alertas para el dashboard
    """
    return await dashboard_controller.get_alertas_summary(db=db, limit=limit)


@router.get("/completo")
async def get_dashboard_completo(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio para estadísticas"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin para estadísticas"),
    db: Session = Depends(get_db),
    usuario_actual = Depends(require_auth)
):
    """
    Obtener todos los datos del dashboard en una sola llamada
    """
    return await dashboard_controller.get_dashboard_completo(
        db=db,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
