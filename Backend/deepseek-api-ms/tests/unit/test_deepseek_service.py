"""
Tests para el servicio DeepSeek.
"""
import pytest
import requests
import time
from unittest.mock import patch, MagicMock
from src.services.deepseek_service import DeepSeekService, DeepSeekException

class TestDeepSeekService:
    """
    Clase para probar el servicio DeepSeek.
    """
    
    @patch("src.services.deepseek_service.requests.post")
    def test_procesar_texto_exitoso(self, mock_post):
        """Test para el método procesar_texto cuando es exitoso."""
        # Configurar el mock de respuesta
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Texto procesado de prueba"
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 10
            }
        }
        mock_post.return_value = mock_response
        
        # Crear instancia del servicio
        servicio = DeepSeekService()
        
        # Llamar al método bajo prueba
        resultado = servicio.procesar_texto("Texto de prueba")
        
        # Verificar que se llamó al método post con los parámetros correctos
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert f"{servicio.api_url}/v1/chat/completions" == args[0]
        assert kwargs["headers"]["Authorization"] == f"Bearer {servicio.api_key}"
        assert kwargs["json"]["messages"][0]["content"] == "Texto de prueba"
        
        # Verificar el resultado
        assert resultado["texto_procesado"] == "Texto procesado de prueba"
        assert resultado["modelo_usado"] == servicio.default_model
        assert resultado["tokens_entrada"] == 5
        assert resultado["tokens_salida"] == 10
        assert "tiempo_proceso" in resultado
    
    @patch("src.services.deepseek_service.requests.post")
    def test_procesar_texto_error_api(self, mock_post):
        """Test para el método procesar_texto cuando la API devuelve un error."""
        # Configurar el mock para devolver un error
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Error de API"}
        mock_post.return_value = mock_response
        
        # Crear instancia del servicio
        servicio = DeepSeekService()
        
        # Verificar que se lanza la excepción correcta
        with pytest.raises(DeepSeekException) as excinfo:
            servicio.procesar_texto("Texto de prueba")
        
        assert "Error en la API de DeepSeek: 400" in str(excinfo.value)
    
    @patch("src.services.deepseek_service.requests.post")
    def test_procesar_texto_parametros_personalizados(self, mock_post):
        """Test para el método procesar_texto con parámetros personalizados."""
        # Configurar el mock de respuesta
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "Texto procesado de prueba"
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 5,
                "completion_tokens": 10
            }
        }
        mock_post.return_value = mock_response
        
        # Crear instancia del servicio
        servicio = DeepSeekService()
        
        # Parámetros personalizados
        temperatura = 0.3
        max_tokens = 50
        modelo = "modelo-personalizado"
        
        # Llamar al método bajo prueba
        resultado = servicio.procesar_texto(
            "Texto de prueba",
            temperatura=temperatura,
            max_tokens=max_tokens,
            modelo=modelo
        )
        
        # Verificar que se llamó al método post con los parámetros correctos
        args, kwargs = mock_post.call_args
        assert kwargs["json"]["temperature"] == temperatura
        assert kwargs["json"]["max_tokens"] == max_tokens
        assert kwargs["json"]["model"] == modelo
        
        # Verificar el resultado
        assert resultado["modelo_usado"] == modelo
    
    @patch("src.services.deepseek_service.requests.post")
    def test_procesar_texto_connection_error(self, mock_post):
        """Test para manejar errores de conexión."""
        # Configurar el mock para lanzar un error de conexión
        mock_post.side_effect = requests.exceptions.ConnectionError("Error de conexión")
        
        # Crear instancia del servicio con reintentos mínimos para acelerar el test
        servicio = DeepSeekService()
        
        # Verificar que se lanza la excepción correcta
        with pytest.raises(DeepSeekException) as excinfo:
            servicio.procesar_texto("Texto de prueba")
        
        assert "Error de conexión con la API de DeepSeek" in str(excinfo.value)
    
    @patch("src.services.deepseek_service.requests.post")
    def test_procesar_texto_timeout(self, mock_post):
        """Test para manejar errores de timeout."""
        # Configurar el mock para lanzar un error de timeout
        mock_post.side_effect = requests.exceptions.Timeout("Timeout")
        
        # Crear instancia del servicio con reintentos mínimos para acelerar el test
        servicio = DeepSeekService()
        
        # Verificar que se lanza la excepción correcta
        with pytest.raises(DeepSeekException) as excinfo:
            servicio.procesar_texto("Texto de prueba")
        
        assert "Timeout en la conexión con la API de DeepSeek" in str(excinfo.value)
