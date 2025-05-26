import pytest
from fastapi import status
import io
from unittest.mock import patch

class TestYOLOAPI:
    """Tests para la API de YOLO"""
    
    def test_root_endpoint(self, client):
        """Test del endpoint raíz"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
    
    def test_status_endpoint(self, client):
        """Test del endpoint de estado"""
        response = client.get("/status")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"
    
    def test_health_check(self, client):
        """Test del health check"""
        response = client.get("/api/v1/yolo/health")
        # Puede ser 200 o 503 dependiendo del estado del modelo
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_503_SERVICE_UNAVAILABLE]
        
        data = response.json()
        assert "status" in data
        assert "message" in data
    
    def test_get_model_info(self, client):
        """Test de obtención de información del modelo"""
        response = client.get("/api/v1/yolo/model/info")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        # Puede contener error si el modelo no está cargado
        assert isinstance(data, dict)
    
    def test_get_supported_instruments(self, client):
        """Test de obtención de instrumentos soportados"""
        response = client.get("/api/v1/yolo/instruments")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "supported_instruments" in data
        assert "total_instruments" in data
        assert data["total_instruments"] == 10
        assert "BISP-001" in data["supported_instruments"]
    
    def test_detect_instruments_no_file(self, client):
        """Test de detección sin archivo"""
        response = client.post("/api/v1/yolo/detect")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_detect_instruments_invalid_file_type(self, client):
        """Test de detección con tipo de archivo inválido"""
        # Crear archivo de texto
        file_content = b"Este es un archivo de texto, no una imagen"
        
        files = {
            "file": ("test.txt", io.BytesIO(file_content), "text/plain")
        }
        
        response = client.post("/api/v1/yolo/detect", files=files)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        
        data = response.json()
        assert "detail" in data
        assert "no soportado" in data["detail"].lower()
    
    @patch('src.api.controllers.yolo_controller.yolo_service')
    def test_detect_instruments_valid_image(self, mock_yolo_service, client, sample_image_bytes):
        """Test de detección con imagen válida"""
        # Mock del servicio YOLO
        mock_yolo_service.validate_image.return_value = True
        mock_yolo_service.detect_instruments.return_value = {
            "success": True,
            "total_objects": 2,
            "detections": [
                {
                    "id": 1,
                    "class_id": 0,
                    "confidence": 0.8,
                    "bbox": {"x1": 10, "y1": 20, "x2": 30, "y2": 40},
                    "instrument": {
                        "codigo": "BISP-001",
                        "nombre": "Bisturí #11",
                        "descripcion": "Bisturí hoja número 11"
                    }
                }
            ],
            "summary": {
                "BISP-001": {
                    "nombre": "Bisturí #11",
                    "cantidad": 1,
                    "confianza_promedio": 0.8
                }
            }
        }
        
        files = {
            "file": ("test.jpg", sample_image_bytes, "image/jpeg")
        }
        
        response = client.post("/api/v1/yolo/detect", files=files)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["success"] is True
        assert "detections" in data
        assert "summary" in data
        assert "file_info" in data
    
    def test_detect_instruments_with_parameters(self, client, sample_image_bytes):
        """Test de detección con parámetros personalizados"""
        files = {
            "file": ("test.jpg", sample_image_bytes, "image/jpeg")
        }
        
        params = {
            "confidence_threshold": 0.7,
            "iou_threshold": 0.5
        }
        
        response = client.post("/api/v1/yolo/detect", files=files, params=params)
        # El resultado depende del modelo cargado, pero no debería dar error 422
        assert response.status_code != status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_invalid_confidence_threshold(self, client, sample_image_bytes):
        """Test con umbral de confianza inválido"""
        files = {
            "file": ("test.jpg", sample_image_bytes, "image/jpeg")
        }
        
        # Umbral fuera de rango
        params = {
            "confidence_threshold": 1.5
        }
        
        response = client.post("/api/v1/yolo/detect", files=files, params=params)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_invalid_iou_threshold(self, client, sample_image_bytes):
        """Test con umbral de IoU inválido"""
        files = {
            "file": ("test.jpg", sample_image_bytes, "image/jpeg")
        }
        
        # Umbral negativo
        params = {
            "iou_threshold": -0.1
        }
        
        response = client.post("/api/v1/yolo/detect", files=files, params=params)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_openapi_documentation(self, client):
        """Test de documentación OpenAPI"""
        response = client.get("/openapi.json")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
        
        # Verificar que los endpoints están documentados
        assert "/api/v1/yolo/detect" in data["paths"]
        assert "/api/v1/yolo/health" in data["paths"]
        assert "/api/v1/yolo/instruments" in data["paths"]
    
    def test_swagger_documentation(self, client):
        """Test de acceso a Swagger UI"""
        response = client.get("/docs")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]
    
    def test_redoc_documentation(self, client):
        """Test de acceso a ReDoc"""
        response = client.get("/redoc")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]
