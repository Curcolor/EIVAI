from typing import Optional, Dict, Any
from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from fastapi.responses import JSONResponse

from ..controllers.yolo_controller import yolo_controller

# Crear router para las rutas de YOLO
router = APIRouter(prefix="/api/v1/yolo", tags=["YOLO Detection"])

@router.post("/detect", response_model=Dict[str, Any])
async def detect_instruments(
    file: UploadFile = File(..., description="Imagen para analizar"),
    confidence_threshold: Optional[float] = Query(
        None, 
        ge=0.0, 
        le=1.0, 
        description="Umbral de confianza para las detecciones (0.0-1.0)"
    ),
    iou_threshold: Optional[float] = Query(
        None, 
        ge=0.0, 
        le=1.0, 
        description="Umbral de IoU para eliminación de detecciones duplicadas (0.0-1.0)"
    )
):
    """
    Detectar instrumentos quirúrgicos en una imagen
    
    - **file**: Imagen en formato JPG, PNG, BMP, TIFF o WEBP
    - **confidence_threshold**: Umbral de confianza (opcional, por defecto 0.5)
    - **iou_threshold**: Umbral de IoU (opcional, por defecto 0.45)
    
    Retorna:
    - Lista de instrumentos detectados con sus posiciones y confianza
    - Resumen con cantidad de cada tipo de instrumento
    - Información del archivo procesado
    """
    try:
        results = await yolo_controller.detect_instruments_from_file(
            file=file,
            confidence_threshold=confidence_threshold,
            iou_threshold=iou_threshold
        )
        return JSONResponse(content=results, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model/info", response_model=Dict[str, Any])
async def get_model_info():
    """
    Obtener información del modelo YOLO cargado
    
    Retorna información sobre:
    - Tipo y versión del modelo
    - Configuración de umbrales
    - Instrumentos soportados
    """
    try:
        info = yolo_controller.get_model_info()
        return JSONResponse(content=info, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/instruments", response_model=Dict[str, Any])
async def get_supported_instruments():
    """
    Obtener lista de instrumentos quirúrgicos soportados
    
    Retorna:
    - Mapeo completo de instrumentos con códigos y descripciones
    - Total de instrumentos soportados
    """
    try:
        instruments = yolo_controller.get_supported_instruments()
        return JSONResponse(content=instruments, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=Dict[str, str])
async def health_check():
    """
    Verificar el estado de salud del servicio
    
    Retorna:
    - Estado del servicio (healthy/unhealthy)
    - Mensaje descriptivo
    - Versión del servicio
    """
    try:
        health = yolo_controller.health_check()
        status_code = 200 if health["status"] == "healthy" else 503
        return JSONResponse(content=health, status_code=status_code)
    except Exception as e:
        return JSONResponse(
            content={
                "status": "unhealthy",
                "message": f"Error en health check: {str(e)}"
            },
            status_code=503
        )
