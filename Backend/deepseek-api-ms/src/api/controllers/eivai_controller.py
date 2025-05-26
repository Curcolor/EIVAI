"""
Controlador especializado para EIVAI Assistant API.
"""
import time
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from src.services.eivai_assistant_service import EIVAIAssistantService
from src.services.deepseek_service import DeepSeekException
from src.config.settings import get_settings

settings = get_settings()
logger = logging.getLogger("eivai_assistant")

class EIVAIAssistantController:
    """
    Controlador para el asistente de IA de EIVAI.
    
    Maneja todas las operaciones de IA específicas para el Sistema de 
    Gestión de Instrumental Quirúrgico EIVAI.
    """
    
    def __init__(self):
        """Inicializa el controlador con el servicio EIVAI."""
        self.assistant_service = EIVAIAssistantService()
        
    async def verificar_estado_eivai(self) -> Dict[str, Any]:
        """
        Verifica el estado del sistema EIVAI Assistant.
        
        Returns:
            Estado del sistema y servicios disponibles
        """
        try:
            estado_respuesta = {
                "estado": "operativo",
                "mensaje": "EIVAI Assistant está funcionando correctamente",
                "sistema_eivai": {
                    "sistema_activo": True,
                    "version": "1.0.0",
                    "funcionalidades_disponibles": [
                        "Análisis de conteos de instrumentos",
                        "Generación de reportes quirúrgicos",
                        "Consultas en lenguaje natural",
                        "Análisis de patrones de uso",
                        "Alertas inteligentes"
                    ],
                    "ultimo_mantenimiento": datetime.now().strftime("%Y-%m-%d")
                },
                "timestamp": datetime.now().isoformat(),
                "servicios_ia_activos": True
            }
            
            logger.info("Estado de EIVAI Assistant verificado exitosamente")
            return estado_respuesta
            
        except Exception as e:
            logger.error(f"Error verificando estado de EIVAI: {str(e)}")
            return {
                "estado": "error",
                "mensaje": f"Error en el sistema EIVAI: {str(e)}",
                "timestamp": datetime.now().isoformat(),
                "servicios_ia_activos": False
            }
    
    async def analizar_conteos(
        self,
        conteo_inicial: list,
        conteo_final: list,
        tipo_cirugia: str,
        procedimiento_id: Optional[int] = None,
        incluir_recomendaciones: bool = True
    ) -> Dict[str, Any]:
        """
        Analiza conteos de instrumentos quirúrgicos.
        
        Args:
            conteo_inicial: Lista de instrumentos del conteo inicial
            conteo_final: Lista de instrumentos del conteo final
            tipo_cirugia: Tipo de procedimiento quirúrgico
            procedimiento_id: ID del procedimiento (opcional)
            incluir_recomendaciones: Si incluir recomendaciones
            
        Returns:
            Análisis detallado con discrepancias y recomendaciones
            
        Raises:
            DeepSeekException: Si hay error en el procesamiento de IA
        """
        inicio = time.time()
        
        try:
            logger.info(f"Iniciando análisis de conteos para cirugía: {tipo_cirugia}")
            
            # Validar datos de entrada
            if not conteo_inicial or not conteo_final:
                raise ValueError("Los conteos inicial y final son requeridos")
            
            # Procesar análisis con el servicio especializado
            resultado = self.assistant_service.analizar_conteo_instrumentos(
                conteo_inicial=conteo_inicial,
                conteo_final=conteo_final,
                tipo_cirugia=tipo_cirugia,
                incluir_recomendaciones=incluir_recomendaciones
            )
            
            # Agregar metadatos adicionales
            resultado["procedimiento_id"] = procedimiento_id
            resultado["tiempo_total_proceso"] = time.time() - inicio
            
            logger.info(f"Análisis de conteos completado en {resultado['tiempo_total_proceso']:.2f}s")
            
            return resultado
            
        except DeepSeekException as e:
            logger.error(f"Error de IA en análisis de conteos: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado en análisis de conteos: {str(e)}")
            raise
    
    async def generar_reporte_quirurgico(
        self,
        procedimiento_data: Dict[str, Any],
        incluir_recomendaciones: bool = True,
        incluir_analisis_detallado: bool = False
    ) -> Dict[str, Any]:
        """
        Genera un reporte inteligente de procedimiento quirúrgico.
        
        Args:
            procedimiento_data: Datos del procedimiento quirúrgico
            incluir_recomendaciones: Si incluir recomendaciones
            incluir_analisis_detallado: Si incluir análisis detallado
            
        Returns:
            Reporte profesional generado por IA
            
        Raises:
            DeepSeekException: Si hay error en la generación
        """
        inicio = time.time()
        
        try:
            logger.info(f"Generando reporte para procedimiento {procedimiento_data.get('procedimiento_id')}")
            
            # Validar datos requeridos
            campos_requeridos = ['procedimiento_id', 'tipo_cirugia', 'fecha_procedimiento']
            for campo in campos_requeridos:
                if campo not in procedimiento_data:
                    raise ValueError(f"Campo requerido faltante: {campo}")
            
            # Generar reporte con el servicio
            resultado = self.assistant_service.generar_reporte_quirurgico(
                procedimiento_data=procedimiento_data,
                incluir_recomendaciones=incluir_recomendaciones
            )
            
            # Agregar información adicional si se solicita
            if incluir_analisis_detallado:
                resultado["analisis_detallado"] = True
                resultado["metricas_calidad"] = self._calcular_metricas_calidad(procedimiento_data)
            
            resultado["tiempo_total_generacion"] = time.time() - inicio
            
            logger.info(f"Reporte generado exitosamente en {resultado['tiempo_total_generacion']:.2f}s")
            
            return resultado
            
        except DeepSeekException as e:
            logger.error(f"Error de IA generando reporte: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado generando reporte: {str(e)}")
            raise
    
    async def procesar_consulta_natural(
        self,
        consulta: str,
        contexto_adicional: Optional[Dict[str, Any]] = None,
        incluir_referencias: bool = True
    ) -> Dict[str, Any]:
        """
        Procesa consultas en lenguaje natural sobre EIVAI.
        
        Args:
            consulta: Pregunta o consulta del usuario
            contexto_adicional: Contexto adicional para la consulta
            incluir_referencias: Si incluir referencias y enlaces
            
        Returns:
            Respuesta estructurada a la consulta
            
        Raises:
            DeepSeekException: Si hay error en el procesamiento
        """
        inicio = time.time()
        
        try:
            logger.info(f"Procesando consulta natural: {consulta[:50]}...")
            
            if not consulta.strip():
                raise ValueError("La consulta no puede estar vacía")
            
            # Procesar con el servicio de asistente
            resultado = self.assistant_service.consulta_natural_instrumentos(consulta)
            
            # Agregar contexto adicional si se proporciona
            if contexto_adicional:
                resultado["contexto_utilizado"] = contexto_adicional
            
            # Agregar referencias si se solicitan
            if incluir_referencias:
                resultado["referencias_incluidas"] = self._generar_referencias_eivai()
            
            resultado["tiempo_total_proceso"] = time.time() - inicio
            
            logger.info(f"Consulta procesada en {resultado['tiempo_total_proceso']:.2f}s")
            
            return resultado
            
        except DeepSeekException as e:
            logger.error(f"Error de IA procesando consulta: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado procesando consulta: {str(e)}")
            raise
    
    async def analizar_patrones_uso(
        self,
        datos_historicos: list,
        periodo_analisis: str,
        tipo_analisis: str = "uso_instrumentos"
    ) -> Dict[str, Any]:
        """
        Analiza patrones de uso de instrumentos quirúrgicos.
        
        Args:
            datos_historicos: Datos históricos de uso
            periodo_analisis: Período de tiempo analizado
            tipo_analisis: Tipo de análisis a realizar
            
        Returns:
            Insights y recomendaciones basados en patrones
            
        Raises:
            DeepSeekException: Si hay error en el análisis
        """
        inicio = time.time()
        
        try:
            logger.info(f"Iniciando análisis de patrones para período: {periodo_analisis}")
            
            if not datos_historicos:
                raise ValueError("Se requieren datos históricos para el análisis")
            
            # Procesar análisis de patrones
            resultado = self.assistant_service.analizar_patrones_uso(datos_historicos)
            
            # Agregar metadatos del análisis
            resultado["tipo_analisis_solicitado"] = tipo_analisis
            resultado["total_registros_analizados"] = len(datos_historicos)
            resultado["tiempo_total_analisis"] = time.time() - inicio
            
            logger.info(f"Análisis de patrones completado en {resultado['tiempo_total_analisis']:.2f}s")
            
            return resultado
            
        except DeepSeekException as e:
            logger.error(f"Error de IA en análisis de patrones: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado en análisis de patrones: {str(e)}")
            raise
    
    async def generar_alerta_inteligente(
        self,
        tipo_alerta: str,
        datos_contexto: Dict[str, Any],
        prioridad: str = "MEDIA"
    ) -> Dict[str, Any]:
        """
        Genera alertas inteligentes contextualizadas.
        
        Args:
            tipo_alerta: Tipo de alerta a generar
            datos_contexto: Contexto para la alerta
            prioridad: Nivel de prioridad de la alerta
            
        Returns:
            Alerta estructurada con recomendaciones
            
        Raises:
            DeepSeekException: Si hay error en la generación
        """
        inicio = time.time()
        
        try:
            logger.info(f"Generando alerta inteligente tipo: {tipo_alerta}, prioridad: {prioridad}")
            
            # Validar prioridad
            prioridades_validas = ["BAJA", "MEDIA", "ALTA", "CRITICA"]
            if prioridad not in prioridades_validas:
                prioridad = "MEDIA"
            
            # Generar alerta con el servicio
            resultado = self.assistant_service.generar_alerta_inteligente(
                tipo_alerta=tipo_alerta,
                datos_contexto=datos_contexto,
                prioridad=prioridad
            )
            
            # Agregar metadatos de generación
            resultado["tiempo_generacion"] = time.time() - inicio
            resultado["version_sistema"] = "1.0.0"
            
            logger.info(f"Alerta generada en {resultado['tiempo_generacion']:.2f}s")
            
            return resultado
            
        except DeepSeekException as e:
            logger.error(f"Error de IA generando alerta: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado generando alerta: {str(e)}")
            raise
    
    def _calcular_metricas_calidad(self, procedimiento_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula métricas de calidad para un procedimiento.
        
        Args:
            procedimiento_data: Datos del procedimiento
            
        Returns:
            Diccionario con métricas calculadas
        """
        metricas = {
            "conteo_inicial_completado": procedimiento_data.get("conteo_inicial_completo", False),
            "conteo_final_completado": procedimiento_data.get("conteo_final_completo", False),
            "tiene_observaciones": bool(procedimiento_data.get("observaciones")),
            "estado_procedimiento": procedimiento_data.get("estado_procedimiento", "DESCONOCIDO")
        }
        
        # Calcular puntuación de calidad
        puntuacion = 0
        if metricas["conteo_inicial_completado"]:
            puntuacion += 25
        if metricas["conteo_final_completado"]:
            puntuacion += 25
        if metricas["estado_procedimiento"] == "FINALIZADO":
            puntuacion += 30
        if metricas["tiene_observaciones"]:
            puntuacion += 20
        
        metricas["puntuacion_calidad"] = puntuacion
        metricas["nivel_calidad"] = self._clasificar_calidad(puntuacion)
        
        return metricas
    
    def _clasificar_calidad(self, puntuacion: int) -> str:
        """Clasifica el nivel de calidad basado en la puntuación."""
        if puntuacion >= 90:
            return "EXCELENTE"
        elif puntuacion >= 70:
            return "BUENA"
        elif puntuacion >= 50:
            return "ACEPTABLE"
        else:
            return "DEFICIENTE"
    
    def _generar_referencias_eivai(self) -> list:
        """
        Genera referencias útiles para el sistema EIVAI.
        
        Returns:
            Lista de referencias y enlaces útiles
        """
        return [
            "Manual de Usuario EIVAI - Gestión de Instrumentos",
            "Protocolos de Conteo Quirúrgico",
            "Normativas de Seguridad en Quirófano",
            "Guía de Esterilización de Instrumentos",
            "Procedimientos de Emergencia - Instrumentos Faltantes"
        ]
