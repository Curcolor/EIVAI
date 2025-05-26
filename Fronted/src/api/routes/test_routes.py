"""
Rutas de prueba sin autenticación para testing
"""
from typing import Optional
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...config.database import get_db
from ..controllers.dashboard_controller import DashboardController

# Router para pruebas (sin autenticación)
test_router = APIRouter(prefix="/api/test", tags=["Testing"])
dashboard_controller = DashboardController()


@test_router.get("/dashboard/stats")
async def test_dashboard_stats(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio para estadísticas"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin para estadísticas"),
    db: Session = Depends(get_db)
):
    """
    Obtener estadísticas generales del dashboard - ENDPOINT DE PRUEBA SIN AUTH
    """
    try:
        return await dashboard_controller.get_dashboard_stats(
            db=db,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
    except Exception as e:
        return {
            "error": str(e),
            "success": False,
            "data": None
        }


@test_router.get("/dashboard/completo")
async def test_dashboard_completo(
    fecha_inicio: Optional[date] = Query(None, description="Fecha de inicio para estadísticas"),
    fecha_fin: Optional[date] = Query(None, description="Fecha de fin para estadísticas"),
    db: Session = Depends(get_db)
):
    """
    Obtener dashboard completo - ENDPOINT DE PRUEBA SIN AUTH
    """
    try:
        return await dashboard_controller.get_dashboard_completo(
            db=db,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
    except Exception as e:
        return {
            "error": str(e),
            "success": False,
            "data": None
        }


@test_router.get("/usuarios")
async def test_usuarios():
    """
    Endpoint de prueba para usuarios - SIN AUTH
    """
    return {
        "success": True,
        "data": [
            {"id": 1, "nombre": "Usuario Test 1", "activo": True},
            {"id": 2, "nombre": "Usuario Test 2", "activo": True},
        ]
    }


@test_router.get("/instrumentos/estadisticas")
async def test_instrumentos():
    """
    Endpoint de prueba para instrumentos - SIN AUTH
    """
    return {
        "success": True,
        "data": {
            "total": 125,
            "disponibles": 100,
            "en_uso": 20,
            "mantenimiento": 5
        }
    }


@test_router.get("/alertas/activas")
async def test_alertas():
    """
    Endpoint de prueba para alertas - SIN AUTH
    """
    return {
        "success": True,
        "data": [
            {"id": 1, "tipo": "critica", "mensaje": "Instrumento requiere mantenimiento"},
            {"id": 2, "tipo": "info", "mensaje": "Conteo completado"}
        ]
    }


@test_router.get("/procedimientos/estadisticas")
async def test_procedimientos():
    """
    Endpoint de prueba para procedimientos - SIN AUTH
    """
    return {
        "success": True,
        "data": {
            "total": 45,
            "activos": 10,
            "completados": 35
        }
    }


@test_router.get("/conteos")
async def test_conteos():
    """
    Endpoint de prueba para conteos - SIN AUTH
    """
    return {
        "success": True,
        "data": [
            {"id": 1, "procedimiento": "Cirugía 1", "estado": "completado"},
            {"id": 2, "procedimiento": "Cirugía 2", "estado": "pendiente"}
        ]
    }


@test_router.get("/sets/activos")
async def test_sets():
    """
    Endpoint de prueba para sets - SIN AUTH
    """
    return {
        "success": True,
        "data": [
            {"id": 1, "nombre": "Set Básico", "categoria": "General"},
            {"id": 2, "nombre": "Set Cardiología", "categoria": "Especializado"}
        ]
    }
