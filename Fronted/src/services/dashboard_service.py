# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\services\dashboard_service.py
"""
Servicio para el dashboard del sistema EIVAI
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy import func, and_, desc
from sqlalchemy.orm import joinedload
from src.config.database import SessionLocal
from src.api.models.instrumento import Instrumento
from src.api.models.procedimiento_quirurgico import ProcedimientoQuirurgico
from src.api.models.conteo_instrumento import ConteoInstrumento
from src.api.models.alerta import Alerta
from src.api.models.usuario import Usuario
from src.api.models.set_quirurgico import SetQuirurgico
from src.services.alerta_service import AlertaService
from src.services.instrumento_service import InstrumentoService
from src.services.conteo_service import ConteoService

class DashboardService:
    """
    Servicio para generar datos del dashboard
    """
    def __init__(self):
        self.session = SessionLocal()
        self.alerta_service = AlertaService()
        self.instrumento_service = InstrumentoService()
        self.conteo_service = ConteoService()
    
    def obtener_resumen_general(self) -> Dict[str, Any]:
        """
        Obtener resumen general del sistema
        """
        # Estadísticas básicas
        total_instrumentos = self.session.query(Instrumento).filter(Instrumento.activo == True).count()
        total_sets = self.session.query(SetQuirurgico).filter(SetQuirurgico.activo == True).count()
        total_usuarios = self.session.query(Usuario).filter(Usuario.activo == True).count()
        
        # Procedimientos
        procedimientos_activos = self.session.query(ProcedimientoQuirurgico)\
            .filter(ProcedimientoQuirurgico.estado.in_(['En curso', 'Pausado']))\
            .count()
        
        procedimientos_hoy = self.session.query(ProcedimientoQuirurgico)\
            .filter(func.date(ProcedimientoQuirurgico.fecha_inicio) == datetime.now().date())\
            .count()
        
        # Alertas
        alertas_activas = self.session.query(Alerta).filter(Alerta.activa == True).count()
        alertas_criticas = self.session.query(Alerta)\
            .filter(and_(Alerta.activa == True, Alerta.prioridad == 'Alta'))\
            .count()
        
        # Instrumentos con problemas
        instrumentos_mantenimiento = self.session.query(Instrumento)\
            .filter(
                and_(
                    Instrumento.activo == True,
                    Instrumento.fecha_proximo_mantenimiento <= datetime.now().date() + timedelta(days=7)
                )
            ).count()
        
        instrumentos_bajo_stock = self.session.query(Instrumento)\
            .filter(
                and_(
                    Instrumento.activo == True,
                    Instrumento.cantidad_disponible <= 5  # Umbral configurable
                )
            ).count()
        
        return {
            'instrumentos': {
                'total': total_instrumentos,
                'mantenimiento_pendiente': instrumentos_mantenimiento,
                'bajo_stock': instrumentos_bajo_stock
            },
            'sets': {
                'total': total_sets
            },
            'usuarios': {
                'total': total_usuarios,
                'activos_hoy': self._usuarios_activos_hoy()
            },
            'procedimientos': {
                'activos': procedimientos_activos,
                'hoy': procedimientos_hoy
            },
            'alertas': {
                'total': alertas_activas,
                'criticas': alertas_criticas
            }
        }
    
    def obtener_actividad_reciente(self, limit: int = 10) -> Dict[str, Any]:
        """
        Obtener actividad reciente del sistema
        """
        # Procedimientos recientes
        procedimientos_recientes = self.session.query(ProcedimientoQuirurgico)\
            .options(joinedload(ProcedimientoQuirurgico.usuario_responsable))\
            .order_by(desc(ProcedimientoQuirurgico.fecha_inicio))\
            .limit(limit)\
            .all()
        
        # Conteos recientes
        conteos_recientes = self.session.query(ConteoInstrumento)\
            .options(
                joinedload(ConteoInstrumento.instrumento),
                joinedload(ConteoInstrumento.procedimiento),
                joinedload(ConteoInstrumento.usuario_contador)
            )\
            .order_by(desc(ConteoInstrumento.fecha_conteo))\
            .limit(limit)\
            .all()
        
        # Alertas recientes
        alertas_recientes = self.session.query(Alerta)\
            .options(
                joinedload(Alerta.instrumento),
                joinedload(Alerta.procedimiento)
            )\
            .filter(Alerta.activa == True)\
            .order_by(desc(Alerta.fecha_creacion))\
            .limit(limit)\
            .all()
        
        return {
            'procedimientos': [
                {
                    'id': p.procedimiento_id,
                    'nombre': p.nombre,
                    'estado': p.estado,
                    'fecha_inicio': p.fecha_inicio.isoformat() if p.fecha_inicio else None,
                    'responsable': p.usuario_responsable.nombre_completo if p.usuario_responsable else None
                }
                for p in procedimientos_recientes
            ],
            'conteos': [
                {
                    'id': c.conteo_id,
                    'instrumento': c.instrumento.nombre if c.instrumento else None,
                    'procedimiento': c.procedimiento.nombre if c.procedimiento else None,
                    'tipo_conteo': c.tipo_conteo,
                    'cantidad': c.cantidad_contada,
                    'fecha': c.fecha_conteo.isoformat() if c.fecha_conteo else None,
                    'discrepancia': c.discrepancia
                }
                for c in conteos_recientes
            ],
            'alertas': [
                {
                    'id': a.alerta_id,
                    'tipo': a.tipo_alerta,
                    'mensaje': a.mensaje,
                    'prioridad': a.prioridad,
                    'fecha': a.fecha_creacion.isoformat() if a.fecha_creacion else None
                }
                for a in alertas_recientes
            ]
        }
    
    def obtener_estadisticas_uso(self, dias: int = 30) -> Dict[str, Any]:
        """
        Obtener estadísticas de uso en los últimos días
        """
        fecha_inicio = datetime.now() - timedelta(days=dias)
        
        # Procedimientos por día
        procedimientos_por_dia = self.session.query(
            func.date(ProcedimientoQuirurgico.fecha_inicio).label('fecha'),
            func.count(ProcedimientoQuirurgico.procedimiento_id).label('total')
        ).filter(
            ProcedimientoQuirurgico.fecha_inicio >= fecha_inicio
        ).group_by(func.date(ProcedimientoQuirurgico.fecha_inicio))\
         .order_by('fecha')\
         .all()
        
        # Instrumentos más utilizados
        instrumentos_mas_usados = self.session.query(
            Instrumento.nombre,
            func.sum(ConteoInstrumento.cantidad_contada).label('total_uso')
        ).join(ConteoInstrumento)\
         .filter(ConteoInstrumento.fecha_conteo >= fecha_inicio)\
         .group_by(Instrumento.instrumento_id, Instrumento.nombre)\
         .order_by(desc('total_uso'))\
         .limit(10)\
         .all()
        
        # Tipos de alertas más frecuentes
        alertas_frecuentes = self.session.query(
            Alerta.tipo_alerta,
            func.count(Alerta.alerta_id).label('total')
        ).filter(Alerta.fecha_creacion >= fecha_inicio)\
         .group_by(Alerta.tipo_alerta)\
         .order_by(desc('total'))\
         .all()
        
        # Usuarios más activos
        usuarios_activos = self.session.query(
            Usuario.nombre_completo,
            func.count(ConteoInstrumento.conteo_id).label('conteos')
        ).join(ConteoInstrumento, Usuario.usuario_id == ConteoInstrumento.usuario_contador_id)\
         .filter(ConteoInstrumento.fecha_conteo >= fecha_inicio)\
         .group_by(Usuario.usuario_id, Usuario.nombre_completo)\
         .order_by(desc('conteos'))\
         .limit(10)\
         .all()
        
        return {
            'periodo_dias': dias,
            'procedimientos_por_dia': [
                {'fecha': fecha.isoformat(), 'total': total}
                for fecha, total in procedimientos_por_dia
            ],
            'instrumentos_mas_usados': [
                {'instrumento': nombre, 'uso_total': total}
                for nombre, total in instrumentos_mas_usados
            ],
            'alertas_frecuentes': [
                {'tipo': tipo, 'total': total}
                for tipo, total in alertas_frecuentes
            ],
            'usuarios_mas_activos': [
                {'usuario': nombre, 'conteos': conteos}
                for nombre, conteos in usuarios_activos
            ]
        }
    
    def obtener_metricas_rendimiento(self) -> Dict[str, Any]:
        """
        Obtener métricas de rendimiento del sistema
        """
        # Tiempo promedio de procedimientos
        procedimientos_completados = self.session.query(ProcedimientoQuirurgico)\
            .filter(
                and_(
                    ProcedimientoQuirurgico.estado == 'Completado',
                    ProcedimientoQuirurgico.fecha_fin.isnot(None)
                )
            ).all()
        
        duraciones = []
        for proc in procedimientos_completados:
            if proc.fecha_inicio and proc.fecha_fin:
                duracion = (proc.fecha_fin - proc.fecha_inicio).total_seconds() / 3600  # horas
                duraciones.append(duracion)
        
        tiempo_promedio_procedimiento = sum(duraciones) / len(duraciones) if duraciones else 0
        
        # Tasa de discrepancias en conteos
        total_conteos = self.session.query(ConteoInstrumento).count()
        conteos_con_discrepancia = self.session.query(ConteoInstrumento)\
            .filter(ConteoInstrumento.discrepancia == True).count()
        
        tasa_discrepancia = (conteos_con_discrepancia / total_conteos * 100) if total_conteos > 0 else 0
        
        # Tiempo promedio de resolución de alertas
        alertas_resueltas = self.session.query(Alerta)\
            .filter(Alerta.fecha_resolucion.isnot(None)).all()
        
        tiempos_resolucion = []
        for alerta in alertas_resueltas:
            if alerta.fecha_creacion and alerta.fecha_resolucion:
                tiempo = (alerta.fecha_resolucion - alerta.fecha_creacion).total_seconds() / 3600  # horas
                tiempos_resolucion.append(tiempo)
        
        tiempo_promedio_resolucion = sum(tiempos_resolucion) / len(tiempos_resolucion) if tiempos_resolucion else 0
        
        # Disponibilidad de instrumentos
        instrumentos_totales = self.session.query(Instrumento).filter(Instrumento.activo == True).count()
        instrumentos_disponibles = self.session.query(Instrumento)\
            .filter(
                and_(
                    Instrumento.activo == True,
                    Instrumento.estado == 'Disponible'
                )
            ).count()
        
        tasa_disponibilidad = (instrumentos_disponibles / instrumentos_totales * 100) if instrumentos_totales > 0 else 0
        
        return {
            'tiempo_promedio_procedimiento_horas': round(tiempo_promedio_procedimiento, 2),
            'tasa_discrepancia_conteos_pct': round(tasa_discrepancia, 2),
            'tiempo_promedio_resolucion_alertas_horas': round(tiempo_promedio_resolucion, 2),
            'tasa_disponibilidad_instrumentos_pct': round(tasa_disponibilidad, 2),
            'total_procedimientos_completados': len(procedimientos_completados),
            'total_conteos_realizados': total_conteos,
            'total_alertas_resueltas': len(alertas_resueltas)
        }
    
    def _usuarios_activos_hoy(self) -> int:
        """
        Contar usuarios que han tenido actividad hoy
        """
        fecha_hoy = datetime.now().date()
        
        # Usuarios que han hecho conteos hoy
        usuarios_conteos = self.session.query(func.distinct(ConteoInstrumento.usuario_contador_id))\
            .filter(func.date(ConteoInstrumento.fecha_conteo) == fecha_hoy)\
            .count()
        
        # Usuarios que han iniciado procedimientos hoy
        usuarios_procedimientos = self.session.query(func.distinct(ProcedimientoQuirurgico.usuario_responsable_id))\
            .filter(func.date(ProcedimientoQuirurgico.fecha_inicio) == fecha_hoy)\
            .count()
        
        # Aproximación - en un sistema real tendríamos un log de actividad
        return max(usuarios_conteos, usuarios_procedimientos)
    
    def obtener_datos_completos_dashboard(self) -> Dict[str, Any]:
        """
        Obtener todos los datos del dashboard en una sola llamada
        """
        return {
            'resumen_general': self.obtener_resumen_general(),
            'actividad_reciente': self.obtener_actividad_reciente(),
            'estadisticas_uso': self.obtener_estadisticas_uso(),
            'metricas_rendimiento': self.obtener_metricas_rendimiento(),
            'timestamp': datetime.now().isoformat()
        }
