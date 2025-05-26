"""
Rutas específicas para EIVAI Assistant API.
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional, List

from src.api.controllers.eivai_controller import EIVAIAssistantController
from src.api.models.eivai_models import (
    ConteoInstrumentosRequest, ConteoInstrumentosResponse,
    ReporteQuirurgicoRequest, ReporteQuirurgicoResponse,
    ConsultaNaturalRequest, ConsultaNaturalResponse,
    AnalisisPatronesRequest, AnalisisPatronesResponse,
    AlertaInteligente, AlertaInteligenteResponse,
    EstadoEIVAIResponse, ErrorEIVAI
)
from src.services.deepseek_service import DeepSeekException
from datetime import datetime

router = APIRouter(tags=["EIVAI Assistant"])

@router.get("/estado", 
          summary="Verificar estado del sistema EIVAI",
          response_model=EstadoEIVAIResponse)
async def verificar_estado_eivai():
    """
    Verifica el estado del sistema EIVAI Assistant y sus servicios.
    
    Returns:
        Estado completo del sistema EIVAI y servicios de IA disponibles
    """
    try:
        controller = EIVAIAssistantController()
        estado = await controller.verificar_estado_eivai()
        return JSONResponse(status_code=200, content=estado)
    except Exception as e:
        error_response = {
            "error": "Error verificando estado de EIVAI",
            "codigo": 500,
            "detalle": str(e),
            "tipo_error": "ESTADO_ERROR",
            "timestamp": datetime.now().isoformat()
        }
        return JSONResponse(status_code=500, content=error_response)

@router.post("/analizar-conteos",
           summary="Analizar conteos de instrumentos quirúrgicos",
           response_model=ConteoInstrumentosResponse,
           responses={
               400: {"model": ErrorEIVAI, "description": "Error en los datos de conteo"},
               500: {"model": ErrorEIVAI, "description": "Error en el análisis de IA"}
           })
async def analizar_conteos_instrumentos(request: ConteoInstrumentosRequest):
    """
    Analiza conteos de instrumentos quirúrgicos y detecta discrepancias.
    
    Funcionalidades:
    - Comparación automática entre conteo inicial y final
    - Detección de instrumentos faltantes o sobrantes
    - Evaluación de criticidad de discrepancias
    - Recomendaciones específicas para resolución
    - Análisis de riesgo para seguridad del paciente
    
    Args:
        request: Datos de conteos inicial y final con información del procedimiento
        
    Returns:
        Análisis detallado con discrepancias, nivel de riesgo y recomendaciones
    """
    try:
        controller = EIVAIAssistantController()
        
        # Convertir modelos Pydantic a diccionarios
        conteo_inicial = [item.dict() for item in request.conteo_inicial]
        conteo_final = [item.dict() for item in request.conteo_final]
        
        resultado = await controller.analizar_conteos(
            conteo_inicial=conteo_inicial,
            conteo_final=conteo_final,
            tipo_cirugia=request.tipo_cirugia,
            procedimiento_id=request.procedimiento_id,
            incluir_recomendaciones=request.incluir_recomendaciones
        )
        
        return JSONResponse(status_code=200, content=resultado)
        
    except DeepSeekException as e:
        error_response = {
            "error": "Error en el servicio de IA para análisis de conteos",
            "codigo": 500,
            "detalle": str(e),
            "tipo_error": "IA_ERROR",
            "timestamp": datetime.now().isoformat(),
            "sugerencias": [
                "Verificar conectividad con el servicio de IA",
                "Intentar nuevamente en unos momentos",
                "Contactar soporte técnico si el problema persiste"
            ]
        }
        return JSONResponse(status_code=500, content=error_response)
    except ValueError as e:
        error_response = {
            "error": "Datos de conteo inválidos",
            "codigo": 400,
            "detalle": str(e),
            "tipo_error": "VALIDATION_ERROR",
            "timestamp": datetime.now().isoformat(),
            "sugerencias": [
                "Verificar que los conteos inicial y final contengan datos",
                "Asegurar que el tipo de cirugía esté especificado",
                "Revisar el formato de los datos de instrumentos"
            ]
        }
        return JSONResponse(status_code=400, content=error_response)
    except Exception as e:
        error_response = {
            "error": "Error inesperado en análisis de conteos",
            "codigo": 500,
            "detalle": str(e),
            "tipo_error": "INTERNAL_ERROR",
            "timestamp": datetime.now().isoformat()
        }
        return JSONResponse(status_code=500, content=error_response)

@router.post("/generar-reporte",
           summary="Generar reporte quirúrgico inteligente",
           response_model=ReporteQuirurgicoResponse,
           responses={
               400: {"model": ErrorEIVAI, "description": "Datos de procedimiento inválidos"},
               500: {"model": ErrorEIVAI, "description": "Error generando reporte"}
           })
async def generar_reporte_quirurgico(request: ReporteQuirurgicoRequest):
    """
    Genera un reporte profesional de procedimiento quirúrgico usando IA.
    
    Funcionalidades:
    - Resumen ejecutivo del procedimiento
    - Análisis de conteos y estado de instrumentos
    - Evaluación de calidad y seguridad
    - Recomendaciones para mejora continua
    - Documentación profesional para expedientes
    
    Args:
        request: Datos completos del procedimiento quirúrgico
        
    Returns:
        Reporte profesional generado por IA con análisis y recomendaciones
    """
    try:
        controller = EIVAIAssistantController()
        
        resultado = await controller.generar_reporte_quirurgico(
            procedimiento_data=request.procedimiento_data.dict(),
            incluir_recomendaciones=request.incluir_recomendaciones,
            incluir_analisis_detallado=request.incluir_analisis_detallado
        )
        
        return JSONResponse(status_code=200, content=resultado)
        
    except DeepSeekException as e:
        error_response = {
            "error": "Error en el servicio de IA para generación de reporte",
            "codigo": 500,
            "detalle": str(e),
            "tipo_error": "IA_ERROR",
            "timestamp": datetime.now().isoformat()
        }
        return JSONResponse(status_code=500, content=error_response)
    except ValueError as e:
        error_response = {
            "error": "Datos de procedimiento inválidos",
            "codigo": 400,
            "detalle": str(e),
            "tipo_error": "VALIDATION_ERROR",
            "timestamp": datetime.now().isoformat(),
            "sugerencias": [
                "Verificar que todos los campos requeridos estén presentes",
                "Comprobar el formato de fechas y IDs",
                "Asegurar que los datos del procedimiento sean completos"
            ]
        }
        return JSONResponse(status_code=400, content=error_response)
    except Exception as e:
        error_response = {
            "error": "Error inesperado generando reporte",
            "codigo": 500,
            "detalle": str(e),
            "tipo_error": "INTERNAL_ERROR",
            "timestamp": datetime.now().isoformat()
        }
        return JSONResponse(status_code=500, content=error_response)

@router.post("/consulta-natural",
           summary="Procesar consulta en lenguaje natural",
           response_model=ConsultaNaturalResponse,
           responses={
               400: {"model": ErrorEIVAI, "description": "Consulta inválida"},
               500: {"model": ErrorEIVAI, "description": "Error procesando consulta"}
           })
async def procesar_consulta_natural(request: ConsultaNaturalRequest):
    """
    Procesa consultas en lenguaje natural sobre el sistema EIVAI.
    
    Funcionalidades:
    - Respuestas a preguntas sobre instrumentos quirúrgicos
    - Información sobre procedimientos y protocolos
    - Consultas sobre estados y conteos
    - Orientación sobre mejores prácticas
    - Información sobre normativas de seguridad
    
    Ejemplos de consultas:
    - "¿Cuántos instrumentos debe tener un set de laparoscopia?"
    - "¿Qué hacer si falta un instrumento en el conteo final?"
    - "¿Cada cuánto se debe esterilizar el instrumental?"
    - "¿Cuáles son los protocolos para conteo de gasas?"
    
    Args:
        request: Consulta en lenguaje natural del usuario
        
    Returns:
        Respuesta estructurada y contextualizada sobre EIVAI
    """
    try:
        controller = EIVAIAssistantController()
        
        resultado = await controller.procesar_consulta_natural(
            consulta=request.consulta,
            contexto_adicional=request.contexto_adicional,
            incluir_referencias=request.incluir_referencias
        )
        
        return JSONResponse(status_code=200, content=resultado)
        
    except DeepSeekException as e:
        error_response = {
            "error": "Error en el servicio de IA para consulta natural",
            "codigo": 500,
            "detalle": str(e),
            "tipo_error": "IA_ERROR",
            "timestamp": datetime.now().isoformat()
        }
        return JSONResponse(status_code=500, content=error_response)
    except ValueError as e:
        error_response = {
            "error": "Consulta inválida",
            "codigo": 400,
            "detalle": str(e),
            "tipo_error": "VALIDATION_ERROR",
            "timestamp": datetime.now().isoformat(),
            "sugerencias": [
                "La consulta no puede estar vacía",
                "Formular la pregunta de manera clara y específica",
                "Incluir contexto relevante si es necesario"
            ]
        }
        return JSONResponse(status_code=400, content=error_response)
    except Exception as e:
        error_response = {
            "error": "Error inesperado procesando consulta",
            "codigo": 500,
            "detalle": str(e),
            "tipo_error": "INTERNAL_ERROR",
            "timestamp": datetime.now().isoformat()
        }
        return JSONResponse(status_code=500, content=error_response)

@router.post("/analizar-patrones",
           summary="Analizar patrones de uso de instrumentos",
           response_model=AnalisisPatronesResponse,
           responses={
               400: {"model": ErrorEIVAI, "description": "Datos históricos inválidos"},
               500: {"model": ErrorEIVAI, "description": "Error en análisis de patrones"}
           })
async def analizar_patrones_uso(request: AnalisisPatronesRequest):
    """
    Analiza patrones de uso de instrumentos quirúrgicos para optimización.
    
    Funcionalidades:
    - Identificación de patrones de uso por tipo de cirugía
    - Análisis de instrumentos con mayor/menor utilización
    - Detección de tendencias temporales
    - Identificación de oportunidades de optimización
    - Recomendaciones para gestión de inventario
    - Predicciones de demanda futura
    
    Args:
        request: Datos históricos de uso de instrumentos y período de análisis
        
    Returns:
        Insights detallados, patrones identificados y recomendaciones de optimización
    """
    try:
        controller = EIVAIAssistantController()
        
        # Convertir datos históricos a formato de diccionarios
        datos_historicos = [item.dict() for item in request.datos_historicos]
        
        resultado = await controller.analizar_patrones_uso(
            datos_historicos=datos_historicos,
            periodo_analisis=request.periodo_analisis,
            tipo_analisis=request.tipo_analisis
        )
        
        return JSONResponse(status_code=200, content=resultado)
        
    except DeepSeekException as e:
        error_response = {
            "error": "Error en el servicio de IA para análisis de patrones",
            "codigo": 500,
            "detalle": str(e),
            "tipo_error": "IA_ERROR",
            "timestamp": datetime.now().isoformat()
        }
        return JSONResponse(status_code=500, content=error_response)
    except ValueError as e:
        error_response = {
            "error": "Datos históricos inválidos",
            "codigo": 400,
            "detalle": str(e),
            "tipo_error": "VALIDATION_ERROR",
            "timestamp": datetime.now().isoformat(),
            "sugerencias": [
                "Proporcionar al menos algunos datos históricos",
                "Verificar el formato de fechas y cantidades",
                "Asegurar que el período de análisis esté especificado"
            ]
        }
        return JSONResponse(status_code=400, content=error_response)
    except Exception as e:
        error_response = {
            "error": "Error inesperado en análisis de patrones",
            "codigo": 500,
            "detalle": str(e),
            "tipo_error": "INTERNAL_ERROR",
            "timestamp": datetime.now().isoformat()
        }
        return JSONResponse(status_code=500, content=error_response)

@router.post("/generar-alerta",
           summary="Generar alerta inteligente",
           response_model=AlertaInteligenteResponse,
           responses={
               400: {"model": ErrorEIVAI, "description": "Datos de alerta inválidos"},
               500: {"model": ErrorEIVAI, "description": "Error generando alerta"}
           })
async def generar_alerta_inteligente(request: AlertaInteligente):
    """
    Genera alertas inteligentes contextualizadas para el sistema EIVAI.
    
    Funcionalidades:
    - Alertas por instrumentos faltantes o sobrantes
    - Notificaciones de mantenimiento requerido
    - Alertas de calidad y seguridad
    - Avisos de esterilización vencida
    - Alertas de auditoría y cumplimiento
    
    Tipos de alerta soportados:
    - INSTRUMENTO_FALTANTE: Instrumento no encontrado en conteo final
    - DISCREPANCIA_CONTEO: Diferencias en cantidades de instrumentos
    - MANTENIMIENTO_REQUERIDO: Instrumentos que requieren mantenimiento
    - ESTERILIZACION_VENCIDA: Instrumentos con esterilización expirada
    - PROCEDIMIENTO_INCOMPLETO: Procedimientos sin completar conteos
    
    Args:
        request: Datos para generar la alerta inteligente
        
    Returns:
        Alerta estructurada con mensaje, nivel de urgencia y acciones recomendadas
    """
    try:
        controller = EIVAIAssistantController()
        
        resultado = await controller.generar_alerta_inteligente(
            tipo_alerta=request.tipo_alerta,
            datos_contexto=request.datos_contexto.dict(),
            prioridad=request.prioridad.value
        )
        
        return JSONResponse(status_code=200, content=resultado)
        
    except DeepSeekException as e:
        error_response = {
            "error": "Error en el servicio de IA para generación de alerta",
            "codigo": 500,
            "detalle": str(e),
            "tipo_error": "IA_ERROR",
            "timestamp": datetime.now().isoformat()
        }
        return JSONResponse(status_code=500, content=error_response)
    except Exception as e:
        error_response = {
            "error": "Error inesperado generando alerta",
            "codigo": 500,
            "detalle": str(e),
            "tipo_error": "INTERNAL_ERROR",
            "timestamp": datetime.now().isoformat()
        }
        return JSONResponse(status_code=500, content=error_response)

# Endpoint adicional para obtener información sobre capacidades del sistema
@router.get("/capacidades",
          summary="Obtener capacidades del sistema EIVAI",
          response_model=Dict[str, Any])
async def obtener_capacidades_sistema():
    """
    Obtiene información detallada sobre las capacidades del sistema EIVAI.
    
    Returns:
        Información completa sobre funcionalidades, tipos de análisis y características
    """
    capacidades = {
        "sistema": "EIVAI Assistant API",
        "version": "1.0.0",
        "descripcion": "Asistente de IA para Sistema de Gestión de Instrumental Quirúrgico",
        "funcionalidades_principales": {
            "analisis_conteos": {
                "descripcion": "Análisis inteligente de conteos de instrumentos",
                "capacidades": [
                    "Detección de discrepancias",
                    "Evaluación de criticidad",
                    "Recomendaciones de resolución",
                    "Análisis de riesgo"
                ]
            },
            "reportes_quirurgicos": {
                "descripcion": "Generación de reportes profesionales de procedimientos",
                "capacidades": [
                    "Resumen ejecutivo",
                    "Análisis de calidad",
                    "Métricas de seguridad",
                    "Recomendaciones de mejora"
                ]
            },
            "consultas_naturales": {
                "descripcion": "Procesamiento de consultas en lenguaje natural",
                "capacidades": [
                    "Información sobre instrumentos",
                    "Protocolos y procedimientos",
                    "Mejores prácticas",
                    "Normativas de seguridad"
                ]
            },
            "analisis_patrones": {
                "descripcion": "Análisis de patrones de uso para optimización",
                "capacidades": [
                    "Tendencias de uso",
                    "Optimización de inventario",
                    "Predicciones de demanda",
                    "Identificación de eficiencias"
                ]
            },
            "alertas_inteligentes": {
                "descripcion": "Generación de alertas contextualizadas",
                "capacidades": [
                    "Alertas de seguridad",
                    "Notificaciones de mantenimiento",
                    "Avisos de cumplimiento",
                    "Alertas de calidad"
                ]
            }
        },
        "tipos_analisis_soportados": [
            "Conteos de instrumentos",
            "Patrones de uso histórico",
            "Calidad de procedimientos",
            "Eficiencia operacional",
            "Cumplimiento de normativas"
        ],
        "integraciones": [
            "Base de datos EIVAI",
            "Sistema de alertas",
            "Módulo de reportes",
            "Sistema de auditoría"
        ],
        "timestamp": datetime.now().isoformat()
    }
    
    return JSONResponse(status_code=200, content=capacidades)
