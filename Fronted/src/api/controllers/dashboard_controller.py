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
                    for alerta in alertas_activas[:3]
                ]
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
            
            return {
                'stats_generales': stats_generales,
                'alertas': alertas_summary,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
