import os
import tempfile
import shutil
from typing import Optional, Dict, Any
from fastapi import UploadFile, HTTPException
import logging

from ...services.yolo_service import yolo_service
from ...config.settings import settings

logger = logging.getLogger(__name__)

class YOLOController:
    """Controlador para operaciones de detección YOLO"""
    
    def __init__(self):
        """Inicializar el controlador"""
        self.yolo_service = yolo_service
        # Crear directorio de subidas si no existe
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    async def detect_instruments_from_file(
        self,
        file: UploadFile,
        confidence_threshold: Optional[float] = None,
        iou_threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Detectar instrumentos en una imagen subida
        
        Args:
            file: Archivo de imagen subido
            confidence_threshold: Umbral de confianza
            iou_threshold: Umbral de IoU
            
        Returns:
            Resultados de la detección
        """
        temp_file_path = None
        
        try:
            # Validar el archivo
            self._validate_uploaded_file(file)
            
            # Guardar archivo temporal
            temp_file_path = await self._save_temp_file(file)
            
            # Validar que la imagen es válida
            if not self.yolo_service.validate_image(temp_file_path):
                raise HTTPException(
                    status_code=400,
                    detail="El archivo no es una imagen válida"
                )
            
            # Realizar la detección
            results = self.yolo_service.detect_instruments(
                image_path=temp_file_path,
                confidence_threshold=confidence_threshold,
                iou_threshold=iou_threshold
            )
            
            # Agregar información del archivo procesado
            results["file_info"] = {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": file.size
            }
            
            return results
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error procesando archivo {file.filename}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error interno procesando la imagen: {str(e)}"
            )
        finally:
            # Limpiar archivo temporal
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.unlink(temp_file_path)
                except Exception as e:
                    logger.warning(f"No se pudo eliminar archivo temporal {temp_file_path}: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Obtener información del modelo
        
        Returns:
            Información del modelo YOLO
        """
        try:
            return self.yolo_service.get_model_info()
        except Exception as e:
            logger.error(f"Error obteniendo información del modelo: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error obteniendo información del modelo: {str(e)}"
            )
    
    def get_supported_instruments(self) -> Dict[str, Any]:
        """
        Obtener lista de instrumentos soportados
        
        Returns:
            Lista de instrumentos quirúrgicos soportados
        """
        return {
            "supported_instruments": settings.SURGICAL_INSTRUMENTS_MAP,
            "total_instruments": len(settings.SURGICAL_INSTRUMENTS_MAP)
        }
    
    def health_check(self) -> Dict[str, str]:
        """
        Verificar el estado del servicio
        
        Returns:
            Estado del servicio
        """
        try:
            # Verificar que el modelo está cargado
            model_info = self.yolo_service.get_model_info()
            
            if "error" in model_info:
                return {
                    "status": "unhealthy",
                    "message": "Modelo YOLO no está cargado correctamente"
                }
            
            return {
                "status": "healthy",
                "message": "Servicio funcionando correctamente",
                "version": settings.APP_VERSION
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Error en el servicio: {str(e)}"
            }
    
    def _validate_uploaded_file(self, file: UploadFile) -> None:
        """
        Validar archivo subido
        
        Args:
            file: Archivo subido
            
        Raises:
            HTTPException: Si el archivo no es válido
        """
        # Verificar que se subió un archivo
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No se proporcionó ningún archivo"
            )
        
        # Verificar extensión del archivo
        file_extension = file.filename.split('.')[-1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de archivo no soportado. Extensiones permitidas: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # Verificar tamaño del archivo
        if file.size and file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Archivo demasiado grande. Tamaño máximo: {settings.MAX_FILE_SIZE / (1024*1024):.1f}MB"
            )
    
    async def _save_temp_file(self, file: UploadFile) -> str:
        """
        Guardar archivo temporal
        
        Args:
            file: Archivo subido
            
        Returns:
            Ruta del archivo temporal
        """
        # Crear archivo temporal
        file_extension = file.filename.split('.')[-1].lower()
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=f".{file_extension}",
            dir=settings.UPLOAD_DIR
        )
        
        try:
            # Copiar contenido del archivo
            shutil.copyfileobj(file.file, temp_file)
            temp_file.close()
            return temp_file.name
        except Exception as e:
            # Limpiar archivo temporal en caso de error
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
            raise e

# Instancia global del controlador
yolo_controller = YOLOController()
