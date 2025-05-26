"""
Rutas para la API de DeepSeek.
"""
from fastapi import APIRouter, Body, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional

from src.api.controllers.deepseek_controller import DeepSeekController
from src.api.models.deepseek_models import ProcesamientoRequest, ProcesamientoResponse, ErrorResponse
from src.services.deepseek_service import DeepSeekException

router = APIRouter(tags=["DeepSeek"])

@router.get("/estado", 
          summary="Verificar estado del servicio",
          response_model=Dict[str, Any])
async def verificar_estado():
    """
    Verifica el estado actual del servicio de procesamiento de texto.
    
    Returns:
        Información sobre el estado del servicio
    """
    return DeepSeekController.verificar_estado()

@router.post("/procesar",
           summary="Procesar texto con DeepSeek", 
           response_model=ProcesamientoResponse,
           responses={
               400: {"model": ErrorResponse, "description": "Error en la solicitud"},
               500: {"model": ErrorResponse, "description": "Error interno del servidor"}
           })
async def procesar_texto(request: ProcesamientoRequest):
    """
    Procesa texto utilizando la API de DeepSeek.
    
    Args:
        request: Objeto con el texto a procesar y parámetros opcionales
        
    Returns:
        Respuesta con el texto procesado y metadatos
        
    Raises:
        HTTPException: Si ocurre un error en el procesamiento
    """
    try:
        resultado = DeepSeekController.procesar_texto(
            texto=request.texto,
            temperatura=request.temperatura,
            max_tokens=request.max_tokens,
            modelo=request.modelo
        )
        
        return ProcesamientoResponse(
            texto_procesado=resultado["texto_procesado"],
            modelo_usado=resultado["modelo_usado"],
            tokens_entrada=resultado["tokens_entrada"],
            tokens_salida=resultado["tokens_salida"],
            tiempo_proceso=resultado["tiempo_proceso"]
        )
    except DeepSeekException as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Error en el servicio DeepSeek", "detalle": str(e), "codigo": 500}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Error interno del servidor", "detalle": str(e), "codigo": 500}
        )
