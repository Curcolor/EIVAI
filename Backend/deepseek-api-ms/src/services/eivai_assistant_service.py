"""
Servicio especializado de IA para el Sistema EIVAI.
"""
import time
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from src.services.deepseek_service import DeepSeekService, DeepSeekException

logger = logging.getLogger("eivai_assistant")

class EIVAIAssistantService:
    """
    Servicio de asistente de IA especializado para EIVAI.
    
    Proporciona funcionalidades de IA específicas para el Sistema de Gestión 
    de Instrumental Quirúrgico EIVAI, utilizando DeepSeek como motor subyacente.
    """
    
    def __init__(self):
        """Inicializa el servicio con el contexto de EIVAI."""
        self.deepseek_service = DeepSeekService()
        self.contexto_sistema = self._get_contexto_sistema()
    
    def _get_contexto_sistema(self) -> str:
        """
        Obtiene el contexto del sistema EIVAI para todas las consultas.
        """
        return """
        CONTEXTO DEL SISTEMA EIVAI:
        
        EIVAI es un Sistema de Gestión de Instrumental Quirúrgico que incluye:
        
        ENTIDADES PRINCIPALES:
        - Usuarios: Instrumentadores quirúrgicos responsables del conteo
        - SetsQuirurgicos: Conjuntos de instrumentos para procedimientos específicos
        - Instrumentos: Herramientas quirúrgicas individuales con códigos únicos
        - EstadosInstrumento: Estados como 'Disponible', 'En Uso', 'Mantenimiento', 'Esterilización'
        - ProcedimientosQuirurgicos: Cirugías que requieren conteo de instrumentos
        - ConteosInstrumentos: Conteos inicial y final de instrumentos durante cirugías
        - CiclosEsterilizacion: Procesos de esterilización de instrumentos
        - Alertas: Notificaciones sobre discrepancias o problemas
        - AuditoriaAcciones: Registro de todas las acciones del sistema
        
        PROCESOS CLAVE:
        1. Conteo Inicial: Verificar instrumentos antes de la cirugía
        2. Conteo Final: Verificar instrumentos después de la cirugía
        3. Esterilización: Procesos de limpieza y esterilización
        4. Alertas: Notificaciones por instrumentos faltantes o discrepancias
        5. Auditoría: Trazabilidad de todas las acciones
        
        OBJETIVOS DEL SISTEMA:
        - Garantizar la seguridad del paciente
        - Prevenir retención de objetos extraños
        - Optimizar el uso de instrumental quirúrgico
        - Mantener trazabilidad completa
        - Cumplir con normativas de calidad hospitalaria
        """
    
    def analizar_conteo_instrumentos(
        self, 
        conteo_inicial: List[Dict],
        conteo_final: List[Dict],
        tipo_cirugia: str,
        incluir_recomendaciones: bool = True
    ) -> Dict[str, Any]:
        """
        Analiza conteos de instrumentos y detecta discrepancias.
        
        Args:
            conteo_inicial: Lista de instrumentos del conteo inicial
            conteo_final: Lista de instrumentos del conteo final
            tipo_cirugia: Tipo de procedimiento quirúrgico
            incluir_recomendaciones: Si incluir recomendaciones automáticas
            
        Returns:
            Análisis completo con discrepancias y recomendaciones
        """
        texto_analisis = f"""
        {self.contexto_sistema}
        
        TAREA: Analizar conteos de instrumentos quirúrgicos
        
        CONTEO INICIAL:
        {self._formatear_conteo(conteo_inicial)}
        
        CONTEO FINAL:
        {self._formatear_conteo(conteo_final)}
        
        TIPO DE CIRUGÍA: {tipo_cirugia}
        
        ANÁLISIS REQUERIDO:
        1. Identificar discrepancias entre conteo inicial y final
        2. Evaluar la criticidad de cada discrepancia
        3. Determinar posibles causas de las diferencias
        4. {"Generar recomendaciones específicas para resolución" if incluir_recomendaciones else "Solo reportar discrepancias"}
        5. Clasificar el nivel de riesgo para el paciente
        
        Formato de respuesta esperado:
        - Resumen ejecutivo
        - Lista de discrepancias encontradas
        - Nivel de riesgo (BAJO/MEDIO/ALTO/CRÍTICO)
        - Acciones recomendadas inmediatas
        """
        
        try:
            resultado = self.deepseek_service.procesar_texto(
                texto=texto_analisis,
                temperatura=0.1,  # Baja temperatura para análisis preciso
                max_tokens=800
            )
            
            return {
                "tipo_analisis": "conteo_instrumentos",
                "tipo_cirugia": tipo_cirugia,
                "timestamp": datetime.now().isoformat(),
                "discrepancias_detectadas": self._extraer_discrepancias(conteo_inicial, conteo_final),
                "analisis_ia": resultado["texto_procesado"],
                "nivel_confianza": "ALTO",
                "tokens_utilizados": resultado["tokens_salida"],
                "tiempo_proceso": resultado["tiempo_proceso"]
            }
        except DeepSeekException as e:
            logger.error(f"Error en análisis de conteos: {str(e)}")
            raise
    
    def generar_reporte_quirurgico(
        self,
        procedimiento_data: Dict,
        incluir_recomendaciones: bool = True
    ) -> Dict[str, Any]:
        """
        Genera un reporte inteligente de procedimiento quirúrgico.
        """
        texto_reporte = f"""
        {self.contexto_sistema}
        
        TAREA: Generar reporte profesional de procedimiento quirúrgico
        
        DATOS DEL PROCEDIMIENTO:
        {self._formatear_procedimiento(procedimiento_data)}
        
        GENERAR:
        1. Resumen ejecutivo del procedimiento
        2. Estado de conteos de instrumentos
        3. Observaciones relevantes
        4. {"Recomendaciones para mejora continua" if incluir_recomendaciones else "Conclusiones"}
        5. Indicadores de calidad y seguridad
        
        El reporte debe ser profesional, preciso y útil para el equipo quirúrgico.
        """
        
        try:
            resultado = self.deepseek_service.procesar_texto(
                texto=texto_reporte,
                temperatura=0.3,
                max_tokens=1000
            )
            
            return {
                "tipo_reporte": "procedimiento_quirurgico",
                "procedimiento_id": procedimiento_data.get("procedimiento_id"),
                "fecha_generacion": datetime.now().isoformat(),
                "reporte_generado": resultado["texto_procesado"],
                "modelo_utilizado": resultado["modelo_usado"],
                "tiempo_generacion": resultado["tiempo_proceso"]
            }
        except DeepSeekException as e:
            logger.error(f"Error generando reporte: {str(e)}")
            raise
    
    def consulta_natural_instrumentos(self, consulta: str) -> Dict[str, Any]:
        """
        Responde consultas en lenguaje natural sobre instrumentos y procedimientos.
        """
        texto_consulta = f"""
        {self.contexto_sistema}
        
        CONSULTA DEL USUARIO: {consulta}
        
        Responde la consulta proporcionando información precisa y útil sobre:
        - Instrumentos quirúrgicos
        - Procedimientos y protocolos
        - Estados y conteos
        - Mejores prácticas
        - Normativas de seguridad
        
        La respuesta debe ser clara, profesional y orientada a personal médico.
        """
        
        try:
            resultado = self.deepseek_service.procesar_texto(
                texto=texto_consulta,
                temperatura=0.4,
                max_tokens=600
            )
            
            return {
                "tipo_consulta": "lenguaje_natural",
                "consulta_original": consulta,
                "respuesta": resultado["texto_procesado"],
                "timestamp": datetime.now().isoformat(),
                "calidad_respuesta": "ESTÁNDAR"
            }
        except DeepSeekException as e:
            logger.error(f"Error en consulta natural: {str(e)}")
            raise
    
    def analizar_patrones_uso(self, datos_historicos: List[Dict]) -> Dict[str, Any]:
        """
        Analiza patrones de uso de instrumentos para optimización.
        """
        texto_analisis = f"""
        {self.contexto_sistema}
        
        TAREA: Análisis de patrones de uso de instrumental quirúrgico
        
        DATOS HISTÓRICOS:
        {self._formatear_datos_historicos(datos_historicos)}
        
        ANÁLISIS REQUERIDO:
        1. Identificar patrones de uso por tipo de cirugía
        2. Detectar instrumentos con mayor/menor utilización
        3. Analizar tendencias temporales
        4. Identificar oportunidades de optimización
        5. Recomendar mejoras en gestión de inventario
        
        Enfocarse en eficiencia operacional y seguridad del paciente.
        """
        
        try:
            resultado = self.deepseek_service.procesar_texto(
                texto=texto_analisis,
                temperatura=0.2,
                max_tokens=900
            )
            
            return {
                "tipo_analisis": "patrones_uso",
                "periodo_analizado": self._extraer_periodo(datos_historicos),
                "insights": resultado["texto_procesado"],
                "fecha_analisis": datetime.now().isoformat(),
                "recomendaciones_incluidas": True
            }
        except DeepSeekException as e:
            logger.error(f"Error en análisis de patrones: {str(e)}")
            raise
    
    def generar_alerta_inteligente(
        self,
        tipo_alerta: str,
        datos_contexto: Dict,
        prioridad: str = "MEDIA"
    ) -> Dict[str, Any]:
        """
        Genera alertas inteligentes con contexto y recomendaciones.
        """
        texto_alerta = f"""
        {self.contexto_sistema}
        
        TAREA: Generar alerta inteligente para el sistema EIVAI
        
        TIPO DE ALERTA: {tipo_alerta}
        PRIORIDAD: {prioridad}
        
        DATOS DE CONTEXTO:
        {self._formatear_contexto_alerta(datos_contexto)}
        
        GENERAR:
        1. Mensaje de alerta claro y específico
        2. Nivel de urgencia justificado
        3. Acciones recomendadas inmediatas
        4. Posibles consecuencias si no se actúa
        5. Protocolo sugerido de resolución
        
        La alerta debe ser precisa, actionable y orientada a seguridad del paciente.
        """
        
        try:
            resultado = self.deepseek_service.procesar_texto(
                texto=texto_alerta,
                temperatura=0.1,
                max_tokens=500
            )
            
            return {
                "tipo_alerta": tipo_alerta,
                "prioridad": prioridad,
                "mensaje_generado": resultado["texto_procesado"],
                "timestamp": datetime.now().isoformat(),
                "requiere_accion_inmediata": prioridad in ["ALTA", "CRITICA"],
                "contexto_proporcionado": datos_contexto
            }
        except DeepSeekException as e:
            logger.error(f"Error generando alerta: {str(e)}")
            raise
    
    # Métodos auxiliares de formateo
    def _formatear_conteo(self, conteo: List[Dict]) -> str:
        """Formatea una lista de conteos para análisis."""
        if not conteo:
            return "No hay datos de conteo"
        
        lineas = []
        for item in conteo:
            lineas.append(f"- {item.get('nombre_instrumento', 'N/A')}: "
                         f"Esperado: {item.get('cantidad_esperada', 0)}, "
                         f"Contado: {item.get('cantidad_contada', 0)}")
        return "\n".join(lineas)
    
    def _formatear_procedimiento(self, proc_data: Dict) -> str:
        """Formatea datos de procedimiento para reporte."""
        return f"""
        - ID Procedimiento: {proc_data.get('procedimiento_id', 'N/A')}
        - Tipo de Cirugía: {proc_data.get('tipo_cirugia', 'N/A')}
        - Paciente: {proc_data.get('paciente', 'N/A')}
        - Médico: {proc_data.get('medico', 'N/A')}
        - Fecha: {proc_data.get('fecha_procedimiento', 'N/A')}
        - Estado: {proc_data.get('estado_procedimiento', 'N/A')}
        - Set Utilizado: {proc_data.get('nombre_set', 'N/A')}
        """
    
    def _formatear_datos_historicos(self, datos: List[Dict]) -> str:
        """Formatea datos históricos para análisis."""
        if not datos:
            return "No hay datos históricos disponibles"
        
        resumen = f"Total de registros: {len(datos)}\n"
        # Agregar más detalles según los datos disponibles
        return resumen
    
    def _formatear_contexto_alerta(self, contexto: Dict) -> str:
        """Formatea contexto de alerta."""
        lineas = []
        for clave, valor in contexto.items():
            lineas.append(f"- {clave}: {valor}")
        return "\n".join(lineas)
    
    def _extraer_discrepancias(self, inicial: List[Dict], final: List[Dict]) -> List[Dict]:
        """Extrae discrepancias entre conteos inicial y final."""
        discrepancias = []
        
        # Crear mapas para comparación fácil
        inicial_map = {item.get('instrumento_id'): item for item in inicial}
        final_map = {item.get('instrumento_id'): item for item in final}
        
        # Buscar discrepancias
        for inst_id in inicial_map:
            inicial_item = inicial_map[inst_id]
            final_item = final_map.get(inst_id)
            
            if not final_item:
                discrepancias.append({
                    "instrumento_id": inst_id,
                    "nombre": inicial_item.get('nombre_instrumento'),
                    "tipo": "FALTANTE_EN_FINAL",
                    "esperado": inicial_item.get('cantidad_contada', 0),
                    "encontrado": 0
                })
            elif inicial_item.get('cantidad_contada') != final_item.get('cantidad_contada'):
                discrepancias.append({
                    "instrumento_id": inst_id,
                    "nombre": inicial_item.get('nombre_instrumento'),
                    "tipo": "CANTIDAD_DIFERENTE",
                    "esperado": inicial_item.get('cantidad_contada', 0),
                    "encontrado": final_item.get('cantidad_contada', 0)
                })
        
        return discrepancias
    
    def _extraer_periodo(self, datos: List[Dict]) -> str:
        """Extrae el período de tiempo de los datos históricos."""
        if not datos:
            return "Período no determinado"
        
        # Aquí podrías extraer fechas reales de los datos
        return f"Últimos {len(datos)} registros"
