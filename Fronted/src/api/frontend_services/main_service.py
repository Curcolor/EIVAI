"""
Servicio principal de Frontend que integra todos los servicios de comunicación
Maneja la lógica de comunicación entre el frontend y backend
"""
from .usuario_service import UsuarioService
from .instrumento_service import InstrumentoService
from .conteo_service import ConteoService
from .alerta_service import AlertaService
from .dashboard_service import DashboardService
from .procedimiento_service import ProcedimientoService
from .set_service import SetService
from typing import Dict, Any, Optional
import asyncio


class FrontendAPIService:
    """
    Servicio principal que coordina todos los servicios de comunicación
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        
        # Inicializar todos los servicios
        self.usuarios = UsuarioService(base_url)
        self.instrumentos = InstrumentoService(base_url)
        self.conteos = ConteoService(base_url)
        self.alertas = AlertaService(base_url)
        self.dashboard = DashboardService(base_url)
        self.procedimientos = ProcedimientoService(base_url)
        self.sets = SetService(base_url)
    
    async def obtener_datos_dashboard_completo(self) -> Dict[str, Any]:
        """
        Obtener todos los datos necesarios para el dashboard principal
        """
        try:
            # Ejecutar todas las consultas en paralelo para mejor rendimiento
            resultados = await asyncio.gather(
                self.dashboard.obtener_estadisticas_dashboard(),
                self.alertas.obtener_alertas_criticas(),
                self.procedimientos.obtener_procedimientos_activos(),
                self.conteos.obtener_conteos_pendientes(),
                self.instrumentos.obtener_instrumentos_mantenimiento(),
                self.alertas.obtener_resumen_alertas(),
                return_exceptions=True
            )
            
            # Procesar resultados
            dashboard_data = {
                "estadisticas_generales": resultados[0] if not isinstance(resultados[0], Exception) else {},
                "alertas_criticas": resultados[1] if not isinstance(resultados[1], Exception) else [],
                "procedimientos_activos": resultados[2] if not isinstance(resultados[2], Exception) else [],
                "conteos_pendientes": resultados[3] if not isinstance(resultados[3], Exception) else [],
                "instrumentos_mantenimiento": resultados[4] if not isinstance(resultados[4], Exception) else [],
                "resumen_alertas": resultados[5] if not isinstance(resultados[5], Exception) else {},
                "timestamp": str(asyncio.get_event_loop().time())
            }
            
            return dashboard_data
            
        except Exception as e:
            return {
                "error": f"Error obteniendo datos del dashboard: {str(e)}",
                "estadisticas_generales": {},
                "alertas_criticas": [],
                "procedimientos_activos": [],
                "conteos_pendientes": [],
                "instrumentos_mantenimiento": [],
                "resumen_alertas": {}
            }
    
    async def obtener_estadisticas_instrumentos(self) -> Dict[str, Any]:
        """
        Obtener estadísticas completas de instrumentos
        """
        try:
            resultados = await asyncio.gather(
                self.instrumentos.obtener_estadisticas_uso(),
                self.instrumentos.obtener_instrumentos_mantenimiento(),
                self.instrumentos.obtener_instrumentos_activos(),
                return_exceptions=True
            )
            
            return {
                "estadisticas_uso": resultados[0] if not isinstance(resultados[0], Exception) else [],
                "instrumentos_mantenimiento": resultados[1] if not isinstance(resultados[1], Exception) else [],
                "instrumentos_activos": resultados[2] if not isinstance(resultados[2], Exception) else [],
            }
            
        except Exception as e:
            return {"error": f"Error obteniendo estadísticas de instrumentos: {str(e)}"}
    
    async def obtener_resumen_alertas_completo(self) -> Dict[str, Any]:
        """
        Obtener resumen completo de alertas
        """
        try:
            resultados = await asyncio.gather(
                self.alertas.obtener_alertas_criticas(),
                self.alertas.obtener_resumen_alertas(),
                self.alertas.obtener_estadisticas_alertas(),
                return_exceptions=True
            )
            
            return {
                "alertas_criticas": resultados[0] if not isinstance(resultados[0], Exception) else [],
                "resumen": resultados[1] if not isinstance(resultados[1], Exception) else {},
                "estadisticas": resultados[2] if not isinstance(resultados[2], Exception) else {},
            }
            
        except Exception as e:
            return {"error": f"Error obteniendo resumen de alertas: {str(e)}"}
    
    async def obtener_datos_conteos(self) -> Dict[str, Any]:
        """
        Obtener datos completos de conteos
        """
        try:
            resultados = await asyncio.gather(
                self.conteos.obtener_conteos_pendientes(),
                self.conteos.obtener_estadisticas_discrepancias(),
                return_exceptions=True
            )
            
            return {
                "conteos_pendientes": resultados[0] if not isinstance(resultados[0], Exception) else [],
                "estadisticas_discrepancias": resultados[1] if not isinstance(resultados[1], Exception) else {},
            }
            
        except Exception as e:
            return {"error": f"Error obteniendo datos de conteos: {str(e)}"}
    
    async def obtener_datos_sets(self) -> Dict[str, Any]:
        """
        Obtener datos completos de sets quirúrgicos
        """
        try:
            resultados = await asyncio.gather(
                self.sets.obtener_sets_activos(),
                self.sets.obtener_estadisticas_sets(),
                return_exceptions=True
            )
            
            return {
                "sets_activos": resultados[0] if not isinstance(resultados[0], Exception) else [],
                "estadisticas_sets": resultados[1] if not isinstance(resultados[1], Exception) else {},
            }
            
        except Exception as e:
            return {"error": f"Error obteniendo datos de sets: {str(e)}"}


# Instancia global del servicio
frontend_api = FrontendAPIService()
