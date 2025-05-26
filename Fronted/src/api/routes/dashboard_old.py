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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alertas-summary", response_model=AlertasSummaryResponse)
async def get_alertas_summary(
    usuario_actual = Depends(require_auth)
):
    """
    Obtener resumen de alertas por tipo y prioridad
    """
    try:
        summary = await dashboard_controller.get_alertas_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/instrumentos-criticos")
async def get_instrumentos_criticos(
    usuario_actual = Depends(require_auth)
):
    """
    Obtener instrumentos que requieren atención crítica
    """
    try:
        instrumentos = await dashboard_controller.get_instrumentos_criticos()
        return instrumentos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/procedimientos-activos")
async def get_procedimientos_activos(
    usuario_actual = Depends(require_auth)
):
    """
    Obtener procedimientos quirúrgicos activos
    """
    try:
        procedimientos = await dashboard_controller.get_procedimientos_activos()
        return procedimientos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conteos-pendientes")
async def get_conteos_pendientes(
    usuario_actual = Depends(require_auth)
):
    """
    Obtener conteos de instrumentos pendientes de verificación
    """
    try:
        conteos = await dashboard_controller.get_conteos_pendientes()
        return conteos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estadisticas-uso")
async def get_estadisticas_uso(
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    usuario_actual = Depends(require_auth)
):
    """
    Obtener estadísticas de uso de instrumentos
    """
    try:
        estadisticas = await dashboard_controller.get_estadisticas_uso(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        return estadisticas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tendencias-mantenimiento")
async def get_tendencias_mantenimiento(
    meses: int = 6,
    usuario_actual = Depends(require_auth)
):
    """
    Obtener tendencias de mantenimiento de instrumentos
    """
    try:
        tendencias = await dashboard_controller.get_tendencias_mantenimiento(meses=meses)
        return tendencias
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/eficiencia-quirofanos")
async def get_eficiencia_quirofanos(
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    usuario_actual = Depends(require_admin)
):
    """
    Obtener métricas de eficiencia de quirófanos (solo administradores)
    """
    try:
        eficiencia = await dashboard_controller.get_eficiencia_quirofanos(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        return eficiencia
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/real-time-data")
async def get_real_time_data(
    usuario_actual = Depends(require_auth)
):
    """
    Obtener datos en tiempo real para el dashboard
    """
    try:
        data = await dashboard_controller.get_real_time_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
