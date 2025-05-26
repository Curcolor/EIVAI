import pytest
import os
from unittest.mock import Mock, patch
from src.services.yolo_service import YOLODetectionService
from src.config.settings import settings

class TestYOLOService:
    """Tests para el servicio YOLO"""
    
    @pytest.fixture
    def yolo_service(self):
        """Fixture del servicio YOLO"""
        with patch('src.services.yolo_service.YOLO') as mock_yolo:
            # Mock del modelo YOLO
            mock_model = Mock()
            mock_yolo.return_value = mock_model
            
            service = YOLODetectionService()
            service.model = mock_model
            return service
    
    def test_model_initialization(self, yolo_service):
        """Test de inicialización del modelo"""
        assert yolo_service.model is not None
    
    def test_get_model_info(self, yolo_service):
        """Test de obtención de información del modelo"""
        info = yolo_service.get_model_info()
        
        assert "model_path" in info
        assert "model_type" in info
        assert "confidence_threshold" in info
        assert info["model_type"] == "YOLOv8"
    
    def test_get_instrument_info_known_class(self, yolo_service):
        """Test de obtención de información de instrumento conocido"""
        # Test con clase conocida
        info = yolo_service._get_instrument_info(0)
        
        assert "codigo" in info
        assert "nombre" in info
        assert "descripcion" in info
        assert info["codigo"] == "BISP-001"
    
    def test_get_instrument_info_unknown_class(self, yolo_service):
        """Test de obtención de información de instrumento desconocido"""
        # Test con clase desconocida
        info = yolo_service._get_instrument_info(999)
        
        assert "codigo" in info
        assert "nombre" in info
        assert "descripcion" in info
        assert info["codigo"].startswith("UNKNOWN-")
    
    def test_validate_image_valid(self, yolo_service, sample_image):
        """Test de validación de imagen válida"""
        is_valid = yolo_service.validate_image(sample_image)
        assert is_valid is True
        
        # Limpiar archivo temporal
        os.unlink(sample_image)
    
    def test_validate_image_invalid(self, yolo_service):
        """Test de validación de imagen inválida"""
        # Archivo que no existe
        is_valid = yolo_service.validate_image("archivo_inexistente.jpg")
        assert is_valid is False
    
    def test_generate_summary(self, yolo_service):
        """Test de generación de resumen"""
        # Detecciones de prueba
        detections = [
            {
                "confidence": 0.8,
                "instrument": {
                    "codigo": "BISP-001",
                    "nombre": "Bisturí #11",
                    "descripcion": "Bisturí hoja número 11"
                }
            },
            {
                "confidence": 0.9,
                "instrument": {
                    "codigo": "BISP-001",
                    "nombre": "Bisturí #11",
                    "descripcion": "Bisturí hoja número 11"
                }
            },
            {
                "confidence": 0.7,
                "instrument": {
                    "codigo": "PINZ-001",
                    "nombre": "Pinza Kelly",
                    "descripcion": "Pinza hemostática Kelly curva"
                }
            }
        ]
        
        summary = yolo_service._generate_summary(detections)
        
        # Verificar resumen
        assert "BISP-001" in summary
        assert "PINZ-001" in summary
        assert summary["BISP-001"]["cantidad"] == 2
        assert summary["PINZ-001"]["cantidad"] == 1
        assert summary["BISP-001"]["confianza_promedio"] == 0.85
    
    @patch('src.services.yolo_service.cv2.imread')
    @patch('src.services.yolo_service.Image.open')
    def test_detect_instruments_success(self, mock_pil_open, mock_cv2_imread, yolo_service, sample_image):
        """Test de detección exitosa de instrumentos"""
        # Mock de OpenCV
        mock_cv2_imread.return_value = Mock()  # Imagen válida
        
        # Mock de PIL
        mock_pil_image = Mock()
        mock_pil_open.return_value.__enter__.return_value = mock_pil_image
        
        # Mock del resultado de YOLO
        mock_result = Mock()
        mock_result.boxes = Mock()
        mock_result.boxes.xyxy.cpu.return_value.numpy.return_value = [[10, 20, 30, 40]]
        mock_result.boxes.conf.cpu.return_value.numpy.return_value = [0.8]
        mock_result.boxes.cls.cpu.return_value.numpy.return_value.astype.return_value = [0]
        
        yolo_service.model.return_value = [mock_result]
        
        # Ejecutar detección
        result = yolo_service.detect_instruments(sample_image)
        
        # Verificar resultado
        assert result["success"] is True
        assert "detections" in result
        assert "summary" in result
        assert len(result["detections"]) == 1
        
        # Limpiar archivo temporal
        os.unlink(sample_image)
    
    def test_detect_instruments_model_not_loaded(self):
        """Test de detección sin modelo cargado"""
        service = YOLODetectionService()
        service.model = None
        
        result = service.detect_instruments("test_image.jpg")
        
        assert result["success"] is False
        assert "error" in result
