"""
Tests de integración para la API.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

class TestDeepSeekAPI:
    """
    Clase para los tests de integración de la API.
    """
    
    def test_health_check(self, client):
        """Test para el endpoint de health check."""
        response = client.get("/salud")
        
        assert response.status_code == 200
        assert response.json()["estado"] == "operativo"
    
    def test_root(self, client):
        """Test para el endpoint raíz."""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "servicio" in response.json()
        assert "documentación" in response.json()
    
    def test_api_estado(self, client):
        """Test para el endpoint de estado de la API."""
        # Agregar header de API Key
        headers = {"X-API-Key": "test_default_api_key"}
        response = client.get("/api/v1/estado", headers=headers)
        
        assert response.status_code == 200
        assert response.json()["estado"] == "operativo"
        assert "modelo_predeterminado" in response.json()
    
    def test_api_estado_sin_auth(self, client):
        """Test para el endpoint de estado sin autenticación."""
        response = client.get("/api/v1/estado")
        
        assert response.status_code == 401
    
    def test_api_estado_auth_invalida(self, client):
        """Test para el endpoint de estado con autenticación inválida."""
        headers = {"X-API-Key": "key_invalida"}
        response = client.get("/api/v1/estado", headers=headers)
        
        assert response.status_code == 403
    
    @patch("src.services.deepseek_service.requests.post")
    def test_procesar_texto(self, mock_post, client):
        """Test para el endpoint de procesamiento de texto."""
        # Configurar el mock
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
        
        # Preparar payload y headers
        payload = {
            "texto": "Texto de prueba",
            "temperatura": 0.7,
            "max_tokens": 100,
            "modelo": "test-model"
        }
        headers = {"X-API-Key": "test_default_api_key"}
        
        # Realizar la solicitud
        response = client.post("/api/v1/procesar", json=payload, headers=headers)
        
        # Verificar respuesta
        assert response.status_code == 200
        resultado = response.json()
        assert resultado["texto_procesado"] == "Texto procesado de prueba"
        assert resultado["modelo_usado"] == "test-model"
        assert resultado["tokens_entrada"] == 5
        assert resultado["tokens_salida"] == 10
        assert "tiempo_proceso" in resultado
    
    def test_procesar_texto_payload_invalido(self, client):
        """Test para el endpoint de procesamiento con payload inválido."""
        # Payload inválido (sin texto)
        payload = {
            "temperatura": 0.7
            # Falta campo 'texto'
        }
        headers = {"X-API-Key": "test_default_api_key"}
        
        # Realizar la solicitud
        response = client.post("/api/v1/procesar", json=payload, headers=headers)
        
        # Verificar respuesta de error
        assert response.status_code == 422  # Unprocessable Entity
    
    @patch("src.services.deepseek_service.requests.post")
    def test_procesar_texto_error_servicio(self, mock_post, client):
        """Test para el endpoint cuando el servicio falla."""
        # Configurar el mock para fallar
        mock_post.side_effect = Exception("Error interno simulado")
        
        # Preparar payload y headers
        payload = {"texto": "Texto de prueba"}
        headers = {"X-API-Key": "test_default_api_key"}
        
        # Realizar la solicitud
        response = client.post("/api/v1/procesar", json=payload, headers=headers)
        
        # Verificar respuesta de error
        assert response.status_code == 500
