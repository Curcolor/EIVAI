"""
Tests para el controlador DeepSeek.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.api.controllers.deepseek_controller import DeepSeekController
from src.services.deepseek_service import DeepSeekException

class TestDeepSeekController:
    """
    Clase para probar el controlador DeepSeek.
    """
    
    def test_verificar_estado(self):
        """Test para el método verificar_estado."""
        resultado = DeepSeekController.verificar_estado()
        
        assert isinstance(resultado, dict)
        assert "estado" in resultado
        assert resultado["estado"] == "operativo"
        assert "modelo_predeterminado" in resultado
        assert "timestamp" in resultado
    
    @patch("src.api.controllers.deepseek_controller.DeepSeekService")
    def test_procesar_texto_exitoso(self, mock_service):
        """Test para el método procesar_texto cuando es exitoso."""
        # Configurar el mock
        mock_instance = MagicMock()
        mock_service.return_value = mock_instance
        
        mock_instance.procesar_texto.return_value = {
            "texto_procesado": "Texto procesado de prueba",
            "modelo_usado": "test-model",
            "tokens_entrada": 5,
            "tokens_salida": 10,
            "tiempo_proceso": 0.5
        }
        
        # Llamar al método bajo prueba
        resultado = DeepSeekController.procesar_texto(
            texto="Texto de prueba",
            temperatura=0.5,
            max_tokens=100,
            modelo="test-model"
        )
        
        # Verificar resultados
        assert resultado["texto_procesado"] == "Texto procesado de prueba"
        assert resultado["modelo_usado"] == "test-model"
        assert resultado["tokens_entrada"] == 5
        assert resultado["tokens_salida"] == 10
        assert resultado["tiempo_proceso"] == 0.5
        
        # Verificar que el mock fue llamado correctamente
        mock_instance.procesar_texto.assert_called_once_with(
            texto="Texto de prueba",
            temperatura=0.5,
            max_tokens=100,
            modelo="test-model"
        )
    
    @patch("src.api.controllers.deepseek_controller.DeepSeekService")
    def test_procesar_texto_error(self, mock_service):
        """Test para el método procesar_texto cuando hay un error."""
        # Configurar el mock para lanzar una excepción
        mock_instance = MagicMock()
        mock_service.return_value = mock_instance
        mock_instance.procesar_texto.side_effect = DeepSeekException("Error de prueba")
        
        # Verificar que se propaga la excepción
        with pytest.raises(DeepSeekException) as excinfo:
            DeepSeekController.procesar_texto(texto="Texto de prueba")
        
        assert "Error de prueba" in str(excinfo.value)
