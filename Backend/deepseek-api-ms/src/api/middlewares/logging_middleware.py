"""
Middleware para el registro de solicitudes y respuestas.
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import os

from src.config.settings import get_settings

settings = get_settings()

# Asegurar que existe el directorio de logs
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configurar logging
logging.basicConfig(
    level=getattr(logging, settings.NIVEL_LOG),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/app.log')
    ]
)

logger = logging.getLogger("deepseek_api")

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para registrar solicitudes y respuestas HTTP.
    Proporciona información detallada sobre cada solicitud procesada.
    """
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Registrar la solicitud entrante
        logger.info(f"Solicitud: {request.method} {request.url}")
        
        # Procesar la solicitud
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Registrar la respuesta
            logger.info(
                f"Respuesta: {request.method} {request.url} - Estado: {response.status_code} - Tiempo: {process_time:.4f}s"
            )
            
            # Añadir el tiempo de procesamiento como header
            response.headers["X-Process-Time"] = f"{process_time:.4f}"
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Error: {request.method} {request.url} - Error: {str(e)} - Tiempo: {process_time:.4f}s"
            )
            raise
