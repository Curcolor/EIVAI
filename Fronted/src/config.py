"""
Configuración de la aplicación
"""
import os
from typing import List


class Settings:
    """
    Configuración de la aplicación
    """
    APP_NAME: str = "Frontend Estático EIVAI"
    APP_DESCRIPTION: str = "Aplicación frontend estática con FastAPI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Rutas
    TEMPLATES_DIR: str = "src/templates"
    STATIC_DIR: str = "src/static"


settings = Settings()
