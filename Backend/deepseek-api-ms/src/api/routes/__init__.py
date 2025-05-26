"""
Inicialización del paquete de rutas.

Define el router principal que incluye todas las subrutas.
"""
from fastapi import APIRouter

from src.api.routes.deepseek_routes import router as deepseek_router

# Crear router principal
router = APIRouter()

# Incluir todos los routers
router.include_router(deepseek_router)
