# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\services\alerta_service.py
"""
Servicio para gestión de alertas del sistema
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from sqlalchemy import and_, desc, func, or_
from src.services.base_service import BaseService
from src.api.models.alerta import Alerta
from src.api.models.instrumento import Instrumento
from src.api.models.procedimiento_quirurgico import ProcedimientoQuirurgico
from src.api.models.conteo_instrumento import ConteoInstrumento

class AlertaService(BaseService):
    """
    Servicio para gestión de alertas del sistema EIVAI
    """
    
    def __init__(self):
        super().__init__(Alerta)
    
    def crear_alerta(self, tipo_alerta: str, mensaje: str, prioridad: str = 'Media', 
                     instrumento_id: int = None, procedimiento_id: int = None) -> Alerta:
        """
        Crear una nueva alerta
        """
        alerta = Alerta(
            tipo_alerta=tipo_alerta,
            mensaje=mensaje,
            prioridad=prioridad,
            instrumento_id=instrumento_id,
            procedimiento_id=procedimiento_id,
            fecha_creacion=datetime.now(),
            activa=True
        )
        return self.create(alerta)
    
    def obtener_alertas_activas(self, limit: int = 50) -> List[Alerta]:
        """
        Obtener alertas activas ordenadas por prioridad y fecha
        """
        # Orden por prioridad: Alta > Media > Baja
        prioridad_orden = {
            'Alta': 1,
            'Media': 2,
            'Baja': 3
        }
        
        alertas = self.session.query(Alerta)\
            .options(
                joinedload(Alerta.instrumento),
                joinedload(Alerta.procedimiento)
            )\
            .filter(Alerta.activa == True)\
            .order_by(desc(Alerta.fecha_creacion))\
            .limit(limit)\
            .all()
        
        # Ordenar por prioridad en Python (más eficiente que en SQL para este caso)
        return sorted(alertas, key=lambda x: (prioridad_orden.get(x.prioridad, 4), -x.alerta_id))
    
    def obtener_alertas_por_tipo(self, tipo_alerta: str) -> List[Alerta]:
        """
        Obtener alertas por tipo específico
        """
        return self.session.query(Alerta)\
            .options(
                joinedload(Alerta.instrumento),
                joinedload(Alerta.procedimiento)
            )\
            .filter(
                and_(
                    Alerta.tipo_alerta == tipo_alerta,
                    Alerta.activa == True
                )
            )\
            .order_by(desc(Alerta.fecha_creacion))\
            .all()
    
    def resolver_alerta(self, alerta_id: int, resolucion: str = None) -> Optional[Alerta]:
        """
        Marcar una alerta como resuelta
        """
        alerta = self.get_by_id(alerta_id)
        if not alerta:
            return None
        
        alerta.activa = False
        alerta.fecha_resolucion = datetime.now()
        if resolucion:
            alerta.resolucion = resolucion
        
        return self.update(alerta)
    
    def verificar_alertas_instrumentos(self) -> List[Alerta]:
        """
        Verificar y crear alertas relacionadas con instrumentos
        """
        alertas_creadas = []
        
        # Verificar instrumentos con mantenimiento vencido
        fecha_limite = datetime.now() + timedelta(days=7)  # Alertar 7 días antes
        instrumentos_mantenimiento = self.session.query(Instrumento)\
            .filter(
                and_(
                    Instrumento.activo == True,
                    Instrumento.fecha_proximo_mantenimiento <= fecha_limite
                )
            ).all()
        
        for instrumento in instrumentos_mantenimiento:
            # Verificar si ya existe alerta para este instrumento
            alerta_existente = self.session.query(Alerta)\
                .filter(
                    and_(
                        Alerta.instrumento_id == instrumento.instrumento_id,
                        Alerta.tipo_alerta == 'Mantenimiento',
                        Alerta.activa == True
                    )
                ).first()
            
            if not alerta_existente:
                dias_restantes = (instrumento.fecha_proximo_mantenimiento - datetime.now().date()).days
                mensaje = f"Instrumento {instrumento.nombre} requiere mantenimiento en {dias_restantes} días"
                prioridad = 'Alta' if dias_restantes <= 3 else 'Media'
                
                alerta = self.crear_alerta(
                    tipo_alerta='Mantenimiento',
                    mensaje=mensaje,
                    prioridad=prioridad,
                    instrumento_id=instrumento.instrumento_id
                )
                alertas_creadas.append(alerta)
        
        # Verificar instrumentos con uso excesivo
        limite_uso_diario = 10  # Configurable
        fecha_hoy = datetime.now().date()
        
        instrumentos_uso_excesivo = self.session.query(Instrumento)\
            .filter(Instrumento.usos_hoy >= limite_uso_diario)\
            .all()
        
        for instrumento in instrumentos_uso_excesivo:
            alerta_existente = self.session.query(Alerta)\
                .filter(
                    and_(
                        Alerta.instrumento_id == instrumento.instrumento_id,
                        Alerta.tipo_alerta == 'Uso Excesivo',
                        Alerta.activa == True,
                        func.date(Alerta.fecha_creacion) == fecha_hoy
                    )
                ).first()
            
            if not alerta_existente:
                mensaje = f"Instrumento {instrumento.nombre} ha excedido el límite de uso diario ({instrumento.usos_hoy}/{limite_uso_diario})"
                alerta = self.crear_alerta(
                    tipo_alerta='Uso Excesivo',
                    mensaje=mensaje,
                    prioridad='Media',
                    instrumento_id=instrumento.instrumento_id
                )
                alertas_creadas.append(alerta)
        
        return alertas_creadas
    
    def verificar_alertas_conteos(self) -> List[Alerta]:
        """
        Verificar y crear alertas relacionadas con discrepancias en conteos
        """
        alertas_creadas = []
        
        # Buscar conteos con discrepancias no resueltas
        conteos_discrepancia = self.session.query(ConteoInstrumento)\
            .filter(ConteoInstrumento.discrepancia == True)\
            .join(ProcedimientoQuirurgico)\
            .filter(ProcedimientoQuirurgico.estado.in_(['En curso', 'Pausado']))\
            .all()
        
        for conteo in conteos_discrepancia:
            # Verificar si ya existe alerta para esta discrepancia
            alerta_existente = self.session.query(Alerta)\
                .filter(
                    and_(
                        Alerta.procedimiento_id == conteo.procedimiento_id,
                        Alerta.instrumento_id == conteo.instrumento_id,
                        Alerta.tipo_alerta == 'Discrepancia Conteo',
                        Alerta.activa == True
                    )
                ).first()
            
            if not alerta_existente:
                mensaje = f"Discrepancia en conteo de {conteo.instrumento.nombre} en procedimiento {conteo.procedimiento.nombre}"
                alerta = self.crear_alerta(
                    tipo_alerta='Discrepancia Conteo',
                    mensaje=mensaje,
                    prioridad='Alta',
                    instrumento_id=conteo.instrumento_id,
                    procedimiento_id=conteo.procedimiento_id
                )
                alertas_creadas.append(alerta)
        
        return alertas_creadas
    
    def obtener_estadisticas_alertas(self, fecha_inicio: datetime = None, fecha_fin: datetime = None) -> Dict[str, Any]:
        """
        Obtener estadísticas de alertas
        """
        query = self.session.query(Alerta)
        
        if fecha_inicio:
            query = query.filter(Alerta.fecha_creacion >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Alerta.fecha_creacion <= fecha_fin)
        
        # Estadísticas básicas
        total_alertas = query.count()
        alertas_activas = query.filter(Alerta.activa == True).count()
        alertas_resueltas = query.filter(Alerta.activa == False).count()
        
        # Alertas por tipo
        alertas_por_tipo = query.with_entities(
            Alerta.tipo_alerta,
            func.count(Alerta.alerta_id)
        ).group_by(Alerta.tipo_alerta).all()
        
        # Alertas por prioridad
        alertas_por_prioridad = query.filter(Alerta.activa == True)\
            .with_entities(
                Alerta.prioridad,
                func.count(Alerta.alerta_id)
            )\
            .group_by(Alerta.prioridad).all()
        
        # Tiempo promedio de resolución
        tiempo_resolucion = self.session.query(
            func.avg(
                func.julianday(Alerta.fecha_resolucion) - func.julianday(Alerta.fecha_creacion)
            )
        ).filter(Alerta.fecha_resolucion.isnot(None)).scalar()
        
        return {
            'total_alertas': total_alertas,
            'alertas_activas': alertas_activas,
            'alertas_resueltas': alertas_resueltas,
            'tasa_resolucion': round((alertas_resueltas / total_alertas * 100) if total_alertas > 0 else 0, 2),
            'alertas_por_tipo': dict(alertas_por_tipo),
            'alertas_por_prioridad': dict(alertas_por_prioridad),
            'tiempo_promedio_resolucion_dias': round(tiempo_resolucion or 0, 2)
        }
    
    def ejecutar_verificaciones_automaticas(self) -> Dict[str, Any]:
        """
        Ejecutar todas las verificaciones automáticas de alertas
        """
        alertas_instrumentos = self.verificar_alertas_instrumentos()
        alertas_conteos = self.verificar_alertas_conteos()
        
        return {
            'alertas_creadas': len(alertas_instrumentos) + len(alertas_conteos),
            'alertas_instrumentos': len(alertas_instrumentos),
            'alertas_conteos': len(alertas_conteos),
            'timestamp': datetime.now()
        }
