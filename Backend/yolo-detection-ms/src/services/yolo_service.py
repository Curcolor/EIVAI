import os
import tempfile
import shutil
from typing import List, Dict, Any, Optional
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import logging

from ..config.settings import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YOLODetectionService:
    """Servicio para detección de objetos usando YOLO"""
    
    def __init__(self):
        """Inicializar el servicio de detección"""
        self.model = None
        self._load_model()
    
    def _load_model(self) -> None:
        """Cargar el modelo YOLO"""
        try:
            logger.info(f"Cargando modelo YOLO: {settings.YOLO_MODEL_PATH}")
            self.model = YOLO(settings.YOLO_MODEL_PATH)
            logger.info("Modelo YOLO cargado exitosamente")
        except Exception as e:
            logger.error(f"Error al cargar el modelo YOLO: {str(e)}")
            raise
    
    def detect_instruments(
        self, 
        image_path: str,
        confidence_threshold: Optional[float] = None,
        iou_threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Detectar instrumentos quirúrgicos en una imagen
        
        Args:
            image_path: Ruta de la imagen
            confidence_threshold: Umbral de confianza (opcional)
            iou_threshold: Umbral de IoU (opcional)
            
        Returns:
            Diccionario con los resultados de detección
        """
        try:
            if not self.model:
                raise ValueError("Modelo YOLO no está cargado")
            
            # Usar valores por defecto si no se proporcionan
            conf_threshold = confidence_threshold or settings.CONFIDENCE_THRESHOLD
            iou_threshold = iou_threshold or settings.IOU_THRESHOLD
            
            logger.info(f"Procesando imagen: {image_path}")
            
            # Realizar la detección
            results = self.model(
                image_path,
                conf=conf_threshold,
                iou=iou_threshold,
                verbose=False
            )
            
            # Procesar los resultados
            detections = self._process_results(results[0])
            
            # Generar resumen
            summary = self._generate_summary(detections)
            
            return {
                "success": True,
                "total_objects": len(detections),
                "detections": detections,
                "summary": summary,
                "confidence_threshold": conf_threshold,
                "iou_threshold": iou_threshold
            }
            
        except Exception as e:
            logger.error(f"Error en detección: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "detections": [],
                "summary": {}
            }
    
    def _process_results(self, result) -> List[Dict[str, Any]]:
        """
        Procesar los resultados de YOLO
        
        Args:
            result: Resultado de YOLO
            
        Returns:
            Lista de detecciones procesadas
        """
        detections = []
        
        if result.boxes is not None:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy().astype(int)
            
            for i, (box, confidence, class_id) in enumerate(zip(boxes, confidences, class_ids)):
                # Obtener información del instrumento
                instrument_info = self._get_instrument_info(class_id)
                
                detection = {
                    "id": i + 1,
                    "class_id": int(class_id),
                    "confidence": float(confidence),
                    "bbox": {
                        "x1": float(box[0]),
                        "y1": float(box[1]),
                        "x2": float(box[2]),
                        "y2": float(box[3])
                    },
                    "instrument": instrument_info
                }
                
                detections.append(detection)
        
        return detections
    
    def _get_instrument_info(self, class_id: int) -> Dict[str, str]:
        """
        Obtener información del instrumento basado en el class_id
        
        Args:
            class_id: ID de la clase detectada
            
        Returns:
            Información del instrumento
        """
        # En un modelo personalizado, mapearías los class_ids a instrumentos
        # Por ahora, usamos un mapeo simulado
        instrument_map = settings.SURGICAL_INSTRUMENTS_MAP
        
        if class_id in instrument_map:
            return instrument_map[class_id]
        else:
            return {
                "codigo": f"UNKNOWN-{class_id:03d}",
                "nombre": f"Objeto desconocido {class_id}",
                "descripcion": f"Objeto no identificado con class_id {class_id}"
            }
    
    def _generate_summary(self, detections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generar resumen de las detecciones
        
        Args:
            detections: Lista de detecciones
            
        Returns:
            Resumen de las detecciones
        """
        summary = {}
        
        # Contar instrumentos por tipo
        for detection in detections:
            instrument = detection["instrument"]
            codigo = instrument["codigo"]
            nombre = instrument["nombre"]
            
            if codigo not in summary:
                summary[codigo] = {
                    "nombre": nombre,
                    "descripcion": instrument["descripcion"],
                    "cantidad": 0,
                    "confianza_promedio": 0.0
                }
            
            summary[codigo]["cantidad"] += 1
            summary[codigo]["confianza_promedio"] += detection["confidence"]
        
        # Calcular confianza promedio
        for codigo in summary:
            if summary[codigo]["cantidad"] > 0:
                summary[codigo]["confianza_promedio"] /= summary[codigo]["cantidad"]
                summary[codigo]["confianza_promedio"] = round(summary[codigo]["confianza_promedio"], 3)
        
        return summary
    
    def validate_image(self, image_path: str) -> bool:
        """
        Validar que la imagen es válida
        
        Args:
            image_path: Ruta de la imagen
            
        Returns:
            True si la imagen es válida, False en caso contrario
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(image_path):
                return False
            
            # Intentar abrir la imagen con PIL
            with Image.open(image_path) as img:
                img.verify()
            
            # Intentar cargar con OpenCV
            image = cv2.imread(image_path)
            if image is None:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validando imagen {image_path}: {str(e)}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Obtener información del modelo cargado
        
        Returns:
            Información del modelo
        """
        if not self.model:
            return {"error": "Modelo no cargado"}
        
        return {
            "model_path": settings.YOLO_MODEL_PATH,
            "model_type": "YOLOv8",
            "confidence_threshold": settings.CONFIDENCE_THRESHOLD,
            "iou_threshold": settings.IOU_THRESHOLD,
            "supported_instruments": list(settings.SURGICAL_INSTRUMENTS_MAP.keys())
        }

# Instancia global del servicio
yolo_service = YOLODetectionService()
