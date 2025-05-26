"""
Middleware para la autenticación mediante API Key.
"""
import logging
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.config.settings import get_settings

settings = get_settings()
logger = logging.getLogger("deepseek_api")

class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    Middleware para validar la API Key en las solicitudes.
    
    Verifica que la API Key proporcionada coincida con la configurada.
    Las rutas de salud y la raíz están exentas de autenticación.
    """
    
    async def dispatch(self, request: Request, call_next):
        # Rutas públicas que no requieren autenticación
        ruta_actual = request.url.path
        rutas_publicas = ["/", "/salud", "/docs", "/redoc", "/openapi.json"]
        
        if any(ruta_actual.startswith(ruta) for ruta in rutas_publicas):
            return await call_next(request)
        
        # Verificar API Key
        api_key = request.headers.get("X-API-Key")
        
        if not api_key:
            logger.warning(f"Intento de acceso sin API Key: {request.method} {request.url}")
            return Response(
                content="{'error': 'Se requiere API Key para acceder a este recurso'}", 
                status_code=401,
                media_type="application/json"
            )
        
        if api_key != settings.DEFAULT_API_KEY:
            logger.warning(f"Intento de acceso con API Key inválida: {request.method} {request.url}")
            return Response(
                content="{'error': 'API Key inválida'}", 
                status_code=403,
                media_type="application/json"
            )
        
        # API Key válida, continuar con la solicitud
        return await call_next(request)
