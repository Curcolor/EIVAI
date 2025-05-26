"""
Configuración para pytest.
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient

# Añadir el directorio raíz al path para permitir importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Cargar variables de entorno de prueba
os.environ["DEEPSEEK_API_KEY"] = "test_api_key"
os.environ["DEEPSEEK_API_URL"] = "https://test.api.deepseek.com"
os.environ["DEEPSEEK_MODELO"] = "test-model"
os.environ["API_HOST"] = "0.0.0.0"
os.environ["API_PUERTO"] = "5003"
os.environ["NIVEL_LOG"] = "DEBUG"
os.environ["DEFAULT_API_KEY"] = "test_default_api_key"
os.environ["TEMPERATURA_PREDETERMINADA"] = "0.7"
os.environ["MAX_TOKENS_PREDETERMINADO"] = "200"
os.environ["REQUEST_TIMEOUT"] = "30"
os.environ["MAX_REINTENTOS"] = "3"
os.environ["TIEMPO_ENTRE_REINTENTOS"] = "1"

@pytest.fixture
def client():
    """
    Fixture para crear un cliente de prueba para la API.
    """
    from src.api.app import app
    return TestClient(app)
