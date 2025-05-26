"""
Inicialización del paquete de rutas.

Define el router principal que incluye todas las subrutas para EIVAI.
"""
from fastapi import APIRouter

from src.api.routes.deepseek_routes import router as deepseek_router
from src.api.routes.eivai_routes import router as eivai_router

# Crear router principal
router = APIRouter()

# Incluir routers con prefijos específicos
router.include_router(deepseek_router, prefix="/deepseek")  # Mantener funcionalidad original
router.include_router(eivai_router, prefix="/eivai")        # Nuevas funcionalidades EIVAI
