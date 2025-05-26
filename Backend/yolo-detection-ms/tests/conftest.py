import pytest
import os
import sys
from fastapi.testclient import TestClient

# Agregar el directorio src al path para importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.api.app import app

@pytest.fixture
def client():
    """Cliente de prueba para FastAPI"""
    return TestClient(app)

@pytest.fixture
def sample_image():
    """Imagen de muestra para testing"""
    # Crear una imagen simple para testing
    from PIL import Image
    import tempfile
    
    # Crear imagen RGB simple
    img = Image.new('RGB', (100, 100), color='red')
    
    # Guardar en archivo temporal
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        img.save(tmp.name, 'JPEG')
        return tmp.name

@pytest.fixture
def sample_image_bytes():
    """Bytes de imagen para testing"""
    from PIL import Image
    import io
    
    # Crear imagen RGB simple
    img = Image.new('RGB', (100, 100), color='blue')
    
    # Convertir a bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes
