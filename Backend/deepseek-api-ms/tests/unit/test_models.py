"""
Tests para los modelos de datos.
"""
import pytest
from pydantic import ValidationError
from src.api.models.deepseek_models import ProcesamientoRequest, ProcesamientoResponse, ErrorResponse

class TestProcesamientoRequest:
    """
    Clase para probar el modelo ProcesamientoRequest.
    """
    
    def test_modelo_valido(self):
        """Test para un modelo válido con todos los campos."""
        datos = {
            "texto": "Texto de prueba",
            "temperatura": 0.7,
            "max_tokens": 100,
            "modelo": "modelo-test"
        }
        
        modelo = ProcesamientoRequest(**datos)
        
        assert modelo.texto == datos["texto"]
        assert modelo.temperatura == datos["temperatura"]
        assert modelo.max_tokens == datos["max_tokens"]
        assert modelo.modelo == datos["modelo"]
    
    def test_modelo_minimo(self):
        """Test para un modelo con solo los campos requeridos."""
        datos = {
            "texto": "Texto de prueba"
        }
        
        modelo = ProcesamientoRequest(**datos)
        
        assert modelo.texto == datos["texto"]
        assert modelo.temperatura is None
        assert modelo.max_tokens is None
        assert modelo.modelo is None
    
    def test_texto_vacio(self):
        """Test para validar que el texto no puede estar vacío."""
        datos = {
            "texto": ""
        }
        
        with pytest.raises(ValidationError):
            ProcesamientoRequest(**datos)
    
    def test_temperatura_invalida(self):
        """Test para validar el rango de temperatura."""
        # Temperatura muy alta
        datos_alta = {
            "texto": "Texto de prueba",
            "temperatura": 1.5
        }
        
        with pytest.raises(ValidationError):
            ProcesamientoRequest(**datos_alta)
        
        # Temperatura muy baja
        datos_baja = {
            "texto": "Texto de prueba",
            "temperatura": -0.5
        }
        
        with pytest.raises(ValidationError):
            ProcesamientoRequest(**datos_baja)
    
    def test_max_tokens_invalido(self):
        """Test para validar que max_tokens debe ser positivo."""
        datos = {
            "texto": "Texto de prueba",
            "max_tokens": 0
        }
        
        with pytest.raises(ValidationError):
            ProcesamientoRequest(**datos)

class TestProcesamientoResponse:
    """
    Clase para probar el modelo ProcesamientoResponse.
    """
    
    def test_modelo_valido(self):
        """Test para un modelo de respuesta válido."""
        datos = {
            "texto_procesado": "Texto procesado de prueba",
            "modelo_usado": "modelo-test",
            "tokens_entrada": 5,
            "tokens_salida": 10,
            "tiempo_proceso": 0.5
        }
        
        modelo = ProcesamientoResponse(**datos)
        
        assert modelo.texto_procesado == datos["texto_procesado"]
        assert modelo.modelo_usado == datos["modelo_usado"]
        assert modelo.tokens_entrada == datos["tokens_entrada"]
        assert modelo.tokens_salida == datos["tokens_salida"]
        assert modelo.tiempo_proceso == datos["tiempo_proceso"]
    
    def test_validacion_campos_requeridos(self):
        """Test para verificar que todos los campos son requeridos."""
        datos_incompletos = {
            "texto_procesado": "Texto procesado de prueba",
            "modelo_usado": "modelo-test"
            # Faltan campos
        }
        
        with pytest.raises(ValidationError):
            ProcesamientoResponse(**datos_incompletos)

class TestErrorResponse:
    """
    Clase para probar el modelo ErrorResponse.
    """
    
    def test_modelo_valido(self):
        """Test para un modelo de error válido."""
        datos = {
            "error": "Mensaje de error",
            "detalle": "Detalles adicionales",
            "codigo": 400
        }
        
        modelo = ErrorResponse(**datos)
        
        assert modelo.error == datos["error"]
        assert modelo.detalle == datos["detalle"]
        assert modelo.codigo == datos["codigo"]
    
    def test_modelo_sin_detalle(self):
        """Test para un modelo de error sin detalle."""
        datos = {
            "error": "Mensaje de error",
            "codigo": 500
        }
        
        modelo = ErrorResponse(**datos)
        
        assert modelo.error == datos["error"]
        assert modelo.detalle is None
        assert modelo.codigo == datos["codigo"]
