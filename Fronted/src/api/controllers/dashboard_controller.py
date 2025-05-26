"""
Controlador para el dashboard del sistema EIVAI
"""
from typing import Dict, Any, Optional, List
from datetime import date, datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.services.dashboard_service import DashboardService


class DashboardController:
    """
    Controlador para operaciones del dashboard
    """
    
    def __init__(self):
        self.dashboard_service = DashboardService()
    
    async def get_dashboard_stats(
        self,
        db: Session,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Obtener estadísticas generales del dashboard
        """
        try:
            stats = await self.dashboard_service.obtener_resumen_general(
                db=db,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            return stats
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_alertas_summary(
        self,
        db: Session,
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Obtener resumen de alertas para el dashboard
        """
        try:
            from src.services.alerta_service import AlertaService
            alerta_service = AlertaService()
            
            # Obtener alertas activas
            alertas_activas = await alerta_service.obtener_alertas_activas(db, limit)
            
            # Categorizar por prioridad
            alertas_por_prioridad = {
                'alta': 0,
                'media': 0,
                'baja': 0,
                'critica': 0
            }
            
            for alerta in alertas_activas:
                if alerta.prioridad.lower() in alertas_por_prioridad:
                    alertas_por_prioridad[alerta.prioridad.lower()] += 1
            
            return {
                'total_activas': len(alertas_activas),
                'por_prioridad': alertas_por_prioridad,
                'alertas_criticas': alertas_por_prioridad['critica'] + alertas_por_prioridad['alta'],
                'alertas_recientes': [
                    {
                        'id': alerta.alerta_id,
                        'tipo': alerta.tipo_alerta,
                        'mensaje': alerta.mensaje,
                        'prioridad': alerta.prioridad,
                        'fecha_creacion': alerta.fecha_creacion.isoformat() if alerta.fecha_creacion else None
                    }
                    for alerta in alertas_activas[:3]                ]
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_dashboard_completo(
        self,
        db: Session,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Obtener todos los datos del dashboard en una sola llamada
        """
        try:
            # Obtener estadísticas básicas
            stats_generales = await self.get_dashboard_stats(db, fecha_inicio, fecha_fin)
            alertas_summary = await self.get_alertas_summary(db)
            
            # Obtener datos adicionales del sistema
            instrumentos_stats = await self._get_instrumentos_stats(db)
            procedimientos_stats = await self._get_procedimientos_stats(db)
            conteos_recientes = await self._get_conteos_recientes(db)
            sets_activos = await self._get_sets_activos(db)
            
            return {
                'stats_generales': stats_generales,
                'alertas': alertas_summary,
                'instrumentos': instrumentos_stats,
                'procedimientos': procedimientos_stats,
                'conteos_recientes': conteos_recientes,
                'sets_quirurgicos': sets_activos,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def _get_instrumentos_stats(self, db: Session) -> Dict[str, Any]:
        """
        Obtener estadísticas de instrumentos
        """
        try:
            from src.services.instrumento_service import InstrumentoService
            instrumento_service = InstrumentoService()
            
            stats = await instrumento_service.obtener_estadisticas_completas(db)
            return stats
            
        except Exception as e:
            return {
                'total': 0,
                'categorias': [],
                'por_estado': {},
                'error': str(e)
            }

    async def _get_procedimientos_stats(self, db: Session) -> Dict[str, Any]:
        """
        Obtener estadísticas de procedimientos
        """
        try:
            from src.services.procedimiento_service import ProcedimientoService
            procedimiento_service = ProcedimientoService()
            
            stats = await procedimiento_service.obtener_estadisticas(db)
            return stats
            
        except Exception as e:
            return {
                'total': 0,
                'activos': 0,
                'completados': 0,
                'error': str(e)
            }

    async def _get_conteos_recientes(self, db: Session, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Obtener conteos recientes
        """
        try:
            from src.services.conteo_service import ConteoService
            conteo_service = ConteoService()
            
            conteos = await conteo_service.obtener_conteos_recientes(db, limit)
            return [
                {
                    'id': conteo.conteo_id,
                    'procedimiento_nombre': getattr(conteo.procedimiento, 'nombre', 'Sin nombre') if conteo.procedimiento else 'Sin procedimiento',
                    'estado': conteo.estado,
                    'total_instrumentos': conteo.total_instrumentos,
                    'fecha_creacion': conteo.fecha_creacion.isoformat() if conteo.fecha_creacion else None,
                    'usuario': getattr(conteo.usuario, 'nombre', 'Desconocido') if conteo.usuario else 'Sin usuario'
                }
                for conteo in conteos
            ]
            
        except Exception as e:
            return []

    async def _get_sets_activos(self, db: Session, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Obtener sets quirúrgicos activos
        """
        try:
            from src.services.set_service import SetService
            set_service = SetService()
            
            sets = await set_service.obtener_sets_activos(db, limit)
            return [
                {
                    'id': set_item.set_id,
                    'nombre': set_item.nombre,
                    'categoria': set_item.categoria,
                    'activo': set_item.activo,
                    'total_instrumentos': len(set_item.instrumentos) if hasattr(set_item, 'instrumentos') else 0,
                    'descripcion': set_item.descripcion
                }
                for set_item in sets
            ]
            
        except Exception as e:
            return []
