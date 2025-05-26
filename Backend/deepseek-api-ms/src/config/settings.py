"""
Configuraciones de la aplicación.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Settings(BaseSettings):
    """
    Configuración de la aplicación basada en variables de entorno.
    
    No se incluyen valores por defecto para garantizar que todas
    las configuraciones sean explícitamente definidas.
    """
    # Servidor
    API_HOST: str = os.getenv("API_HOST")
    API_PUERTO: int = os.getenv("API_PUERTO")
    NIVEL_LOG: str = os.getenv("NIVEL_LOG")
    
    # Seguridad
    DEFAULT_API_KEY: str = os.getenv("DEFAULT_API_KEY")
    API_KEY_NAME: str = os.getenv("API_KEY_NAME")
    
    # DeepSeek
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_URL: str = os.getenv("DEEPSEEK_API_URL")
    DEEPSEEK_MODELO: str = os.getenv("DEEPSEEK_MODELO")
    
    # Parámetros del modelo
    TEMPERATURA_PREDETERMINADA: float = os.getenv("TEMPERATURA_PREDETERMINADA")
    MAX_TOKENS_PREDETERMINADO: int = os.getenv("MAX_TOKENS_PREDETERMINADO")
    
    # Timeout y reintentos
    REQUEST_TIMEOUT: int = os.getenv("REQUEST_TIMEOUT")
    MAX_REINTENTOS: int = os.getenv("MAX_REINTENTOS")
    TIEMPO_ENTRE_REINTENTOS: int = os.getenv("TIEMPO_ENTRE_REINTENTOS")
    
    model_config = {
        "env_file": ".env",
        "env_prefix": "",
        "extra": "ignore"  # Ignorar variables de entorno adicionales
    }

@lru_cache()
def get_settings() -> Settings:
    """
    Carga las configuraciones desde variables de entorno o archivo .env
    con caché LRU para optimizar el rendimiento.
    
    Returns:
        Objeto Settings con la configuración
    """
    return Settings()
