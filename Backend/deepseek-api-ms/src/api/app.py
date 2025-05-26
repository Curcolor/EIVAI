"""
Punto de entrada principal para la API de DeepSeek.
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging

from src.api.routes import router as api_router
from src.api.middlewares.logging_middleware import LoggingMiddleware
from src.api.middlewares.auth_middleware import APIKeyMiddleware
from src.config.settings import get_settings

# Obtener configuración
settings = get_settings()

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="EIVAI IA Assistant API",
    description="API de Asistente de IA para el Sistema de Gestión de Instrumental Quirúrgico EIVAI",
    version="1.0.0",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar middleware de logging
app.add_middleware(LoggingMiddleware)

# Agregar middleware de autenticación
app.add_middleware(APIKeyMiddleware)

# Inclusión de rutas
app.include_router(api_router, prefix="/api/v1/ia")

@app.get("/salud", tags=["Salud"])
async def health_check():
    """Endpoint para comprobar el estado de la API."""
    return JSONResponse(status_code=200, content={"estado": "operativo"})

@app.get("/", tags=["Raíz"])
async def root():
    """
    Ruta raíz que proporciona información básica del servicio.
    """
    return {
        "servicio": "EIVAI IA Assistant API",
        "estado": "operativo",
        "versión": "1.0.0",
        "documentación": "/docs",
        "descripción": "Asistente de IA para el Sistema de Gestión de Instrumental Quirúrgico EIVAI",
        "funcionalidades": [
            "Análisis de conteos de instrumentos",
            "Generación de reportes quirúrgicos",
            "Recomendaciones de procedimientos",
            "Análisis de patrones de uso",
            "Alertas inteligentes",
            "Consultas en lenguaje natural sobre instrumentos"
        ]
    }

def main():
    """Punto de entrada para la ejecución de la API."""
    import uvicorn
    print(f"Servidor EIVAI IA Assistant iniciado en {settings.API_HOST}:{settings.API_PUERTO}")
    uvicorn.run("src.api.app:app", host=settings.API_HOST, port=settings.API_PUERTO)

if __name__ == "__main__":
    main()
