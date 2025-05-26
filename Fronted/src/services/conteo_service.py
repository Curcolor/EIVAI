# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\services\conteo_service.py
"""
Servicio para gestión de conteos de instrumentos
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import and_, desc, func
from src.services.base_service import BaseService
from src.api.models.conteo_instrumento import ConteoInstrumento
from src.api.models.instrumento import Instrumento
from src.api.models.procedimiento_quirurgico import ProcedimientoQuirurgico
from src.api.models.usuario import Usuario
from src.api.models.fotografia import Fotografia

class ConteoService(BaseService):
    """
    Servicio para gestión de conteos de instrumentos quirúrgicos
    """
    
    def __init__(self):
        super().__init__(ConteoInstrumento)
    
    def crear_conteo(self, data: Dict[str, Any]) -> ConteoInstrumento:
        """
        Crear un nuevo conteo de instrumento
        """
        conteo = ConteoInstrumento(**data)
        return self.create(conteo)
    
    def obtener_conteos_por_procedimiento(self, procedimiento_id: int) -> List[ConteoInstrumento]:
        """
        Obtener todos los conteos de un procedimiento específico
        """
        return self.session.query(ConteoInstrumento)\
            .options(
                joinedload(ConteoInstrumento.instrumento),
                joinedload(ConteoInstrumento.usuario_contador),
                joinedload(ConteoInstrumento.fotografias)
            )\
            .filter(ConteoInstrumento.procedimiento_id == procedimiento_id)\
            .order_by(desc(ConteoInstrumento.fecha_conteo))\
            .all()
    
    def obtener_conteos_por_instrumento(self, instrumento_id: int) -> List[ConteoInstrumento]:
        """
        Obtener historial de conteos de un instrumento específico
        """
        return self.session.query(ConteoInstrumento)\
            .options(
                joinedload(ConteoInstrumento.procedimiento),
                joinedload(ConteoInstrumento.usuario_contador)
            )\
            .filter(ConteoInstrumento.instrumento_id == instrumento_id)\
            .order_by(desc(ConteoInstrumento.fecha_conteo))\
            .all()
    
    def actualizar_conteo(self, conteo_id: int, data: Dict[str, Any]) -> Optional[ConteoInstrumento]:
        """
        Actualizar un conteo existente
        """
        conteo = self.get_by_id(conteo_id)
        if not conteo:
            return None
        
        for key, value in data.items():
            if hasattr(conteo, key):
                setattr(conteo, key, value)
        
        return self.update(conteo)
    
    def verificar_conteo_completo(self, procedimiento_id: int) -> Dict[str, Any]:
        """
        Verificar si el conteo de un procedimiento está completo
        """
        # Obtener conteos del procedimiento
        conteos = self.obtener_conteos_por_procedimiento(procedimiento_id)
        
        # Agrupar por instrumento y tipo de conteo
        conteos_por_instrumento = {}
        for conteo in conteos:
            key = (conteo.instrumento_id, conteo.tipo_conteo)
            if key not in conteos_por_instrumento:
                conteos_por_instrumento[key] = []
            conteos_por_instrumento[key].append(conteo)
        
        # Verificar completitud
        instrumentos_faltantes = []
        discrepancias = []
        
        for (instrumento_id, tipo_conteo), conteos_instrumento in conteos_por_instrumento.items():
            # Verificar si hay suficientes conteos (normalmente 2: inicial y final)
            if len(conteos_instrumento) < 2:
                instrumentos_faltantes.append({
                    'instrumento_id': instrumento_id,
                    'tipo_conteo': tipo_conteo,
                    'conteos_realizados': len(conteos_instrumento)
                })
            
            # Verificar discrepancias en cantidades
            if len(conteos_instrumento) >= 2:
                cantidades = [c.cantidad_contada for c in conteos_instrumento]
                if len(set(cantidades)) > 1:  # Hay diferencias
                    discrepancias.append({
                        'instrumento_id': instrumento_id,
                        'tipo_conteo': tipo_conteo,
                        'cantidades': cantidades
                    })
        
        return {
            'completo': len(instrumentos_faltantes) == 0 and len(discrepancias) == 0,
            'instrumentos_faltantes': instrumentos_faltantes,
            'discrepancias': discrepancias,
            'total_conteos': len(conteos)
        }
    
    def obtener_estadisticas_conteo(self, fecha_inicio: datetime = None, fecha_fin: datetime = None) -> Dict[str, Any]:
        """
        Obtener estadísticas de conteos
        """
        query = self.session.query(ConteoInstrumento)
        
        if fecha_inicio:
            query = query.filter(ConteoInstrumento.fecha_conteo >= fecha_inicio)
        if fecha_fin:
            query = query.filter(ConteoInstrumento.fecha_conteo <= fecha_fin)
        
        # Estadísticas básicas
        total_conteos = query.count()
        
        # Conteos por tipo
        conteos_por_tipo = query.with_entities(
            ConteoInstrumento.tipo_conteo,
            func.count(ConteoInstrumento.conteo_id)
        ).group_by(ConteoInstrumento.tipo_conteo).all()
        
        # Discrepancias detectadas
        discrepancias = query.filter(ConteoInstrumento.discrepancia == True).count()
        
        # Conteos por usuario
        conteos_por_usuario = query.join(Usuario)\
            .with_entities(
                Usuario.nombre_completo,
                func.count(ConteoInstrumento.conteo_id)
            )\
            .group_by(Usuario.nombre_completo)\
            .order_by(desc(func.count(ConteoInstrumento.conteo_id)))\
            .limit(10).all()
        
        return {
            'total_conteos': total_conteos,
            'conteos_por_tipo': dict(conteos_por_tipo),
            'discrepancias_detectadas': discrepancias,
            'tasa_discrepancia': round((discrepancias / total_conteos * 100) if total_conteos > 0 else 0, 2),
            'conteos_por_usuario': [
                {'usuario': nombre, 'conteos': cantidad}
                for nombre, cantidad in conteos_por_usuario
            ]
        }
    
    def buscar_conteos(self, filtros: Dict[str, Any] = None, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Buscar conteos con filtros
        """
        query = self.session.query(ConteoInstrumento)\
            .options(
                joinedload(ConteoInstrumento.instrumento),
                joinedload(ConteoInstrumento.procedimiento),
                joinedload(ConteoInstrumento.usuario_contador)
            )
        
        if filtros:
            if 'instrumento_id' in filtros:
                query = query.filter(ConteoInstrumento.instrumento_id == filtros['instrumento_id'])
            
            if 'procedimiento_id' in filtros:
                query = query.filter(ConteoInstrumento.procedimiento_id == filtros['procedimiento_id'])
            
            if 'tipo_conteo' in filtros:
                query = query.filter(ConteoInstrumento.tipo_conteo == filtros['tipo_conteo'])
            
            if 'discrepancia' in filtros:
                query = query.filter(ConteoInstrumento.discrepancia == filtros['discrepancia'])
            
            if 'fecha_inicio' in filtros:
                query = query.filter(ConteoInstrumento.fecha_conteo >= filtros['fecha_inicio'])
            
            if 'fecha_fin' in filtros:
                query = query.filter(ConteoInstrumento.fecha_conteo <= filtros['fecha_fin'])
        
        total = query.count()
        conteos = query.order_by(desc(ConteoInstrumento.fecha_conteo))\
            .offset(offset)\
            .limit(limit)\
            .all()
        
        return {
            'conteos': conteos,
            'total': total,
            'limit': limit,
            'offset': offset
        }
