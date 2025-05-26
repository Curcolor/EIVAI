# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\services\set_service.py
"""
Servicio para gestión de sets quirúrgicos
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import and_, desc, func
from src.services.base_service import BaseService
from src.api.models.set_quirurgico import SetQuirurgico
from src.api.models.set_instrumento import SetInstrumento
from src.api.models.instrumento import Instrumento

class SetService(BaseService):
    """
    Servicio para gestión de sets quirúrgicos
    """
    
    def __init__(self):
        super().__init__(SetQuirurgico)
    
    def crear_set(self, data: Dict[str, Any]) -> SetQuirurgico:
        """
        Crear un nuevo set quirúrgico
        """
        set_quirurgico = SetQuirurgico(**data)
        return self.create(set_quirurgico)
    
    def obtener_set_con_instrumentos(self, set_id: int) -> Optional[SetQuirurgico]:
        """
        Obtener un set con todos sus instrumentos
        """
        return self.session.query(SetQuirurgico)\
            .options(
                joinedload(SetQuirurgico.instrumentos).joinedload(SetInstrumento.instrumento)
            )\
            .filter(SetQuirurgico.set_id == set_id)\
            .first()
    
    def agregar_instrumento_a_set(self, set_id: int, instrumento_id: int, cantidad: int = 1, obligatorio: bool = True) -> Optional[SetInstrumento]:
        """
        Agregar un instrumento a un set quirúrgico
        """
        # Verificar que el set existe
        set_quirurgico = self.get_by_id(set_id)
        if not set_quirurgico:
            return None
        
        # Verificar que el instrumento existe
        instrumento = self.session.query(Instrumento).filter(Instrumento.instrumento_id == instrumento_id).first()
        if not instrumento:
            return None
        
        # Verificar si ya existe la relación
        relacion_existente = self.session.query(SetInstrumento)\
            .filter(
                and_(
                    SetInstrumento.set_id == set_id,
                    SetInstrumento.instrumento_id == instrumento_id
                )
            ).first()
        
        if relacion_existente:
            # Actualizar cantidad si ya existe
            relacion_existente.cantidad = cantidad
            relacion_existente.obligatorio = obligatorio
            self.session.commit()
            return relacion_existente
        
        # Crear nueva relación
        set_instrumento = SetInstrumento(
            set_id=set_id,
            instrumento_id=instrumento_id,
            cantidad=cantidad,
            obligatorio=obligatorio
        )
        
        self.session.add(set_instrumento)
        self.session.commit()
        return set_instrumento
    
    def remover_instrumento_de_set(self, set_id: int, instrumento_id: int) -> bool:
        """
        Remover un instrumento de un set quirúrgico
        """
        relacion = self.session.query(SetInstrumento)\
            .filter(
                and_(
                    SetInstrumento.set_id == set_id,
                    SetInstrumento.instrumento_id == instrumento_id
                )
            ).first()
        
        if relacion:
            self.session.delete(relacion)
            self.session.commit()
            return True
        return False
    
    def actualizar_set(self, set_id: int, data: Dict[str, Any]) -> Optional[SetQuirurgico]:
        """
        Actualizar información de un set quirúrgico
        """
        set_quirurgico = self.get_by_id(set_id)
        if not set_quirurgico:
            return None
        
        for key, value in data.items():
            if hasattr(set_quirurgico, key) and key != 'set_id':
                setattr(set_quirurgico, key, value)
        
        return self.update(set_quirurgico)
    
    def obtener_sets_activos(self) -> List[SetQuirurgico]:
        """
        Obtener todos los sets quirúrgicos activos
        """
        return self.session.query(SetQuirurgico)\
            .options(joinedload(SetQuirurgico.instrumentos))\
            .filter(SetQuirurgico.activo == True)\
            .order_by(SetQuirurgico.nombre)\
            .all()
    
    def obtener_sets_por_especialidad(self, especialidad: str) -> List[SetQuirurgico]:
        """
        Obtener sets quirúrgicos por especialidad
        """
        return self.session.query(SetQuirurgico)\
            .options(joinedload(SetQuirurgico.instrumentos))\
            .filter(
                and_(
                    SetQuirurgico.especialidad == especialidad,
                    SetQuirurgico.activo == True
                )
            )\
            .order_by(SetQuirurgico.nombre)\
            .all()
    
    def verificar_disponibilidad_set(self, set_id: int) -> Dict[str, Any]:
        """
        Verificar disponibilidad de todos los instrumentos de un set
        """
        set_quirurgico = self.obtener_set_con_instrumentos(set_id)
        if not set_quirurgico:
            return {'disponible': False, 'error': 'Set no encontrado'}
        
        instrumentos_disponibles = []
        instrumentos_no_disponibles = []
        instrumentos_insuficientes = []
        
        for relacion in set_quirurgico.instrumentos:
            instrumento = relacion.instrumento
            cantidad_requerida = relacion.cantidad
            cantidad_disponible = instrumento.cantidad_disponible or 0
            
            info_instrumento = {
                'id': instrumento.instrumento_id,
                'nombre': instrumento.nombre,
                'cantidad_requerida': cantidad_requerida,
                'cantidad_disponible': cantidad_disponible,
                'obligatorio': relacion.obligatorio
            }
            
            if not instrumento.activo:
                instrumentos_no_disponibles.append({**info_instrumento, 'razon': 'Instrumento inactivo'})
            elif cantidad_disponible < cantidad_requerida:
                if relacion.obligatorio:
                    instrumentos_insuficientes.append(info_instrumento)
                else:
                    instrumentos_disponibles.append({**info_instrumento, 'nota': 'Opcional - cantidad insuficiente'})
            else:
                instrumentos_disponibles.append(info_instrumento)
        
        # El set está disponible si no hay instrumentos obligatorios faltantes o insuficientes
        disponible = len(instrumentos_no_disponibles) == 0 and len(instrumentos_insuficientes) == 0
        
        return {
            'disponible': disponible,
            'set_id': set_id,
            'nombre_set': set_quirurgico.nombre,
            'instrumentos_disponibles': instrumentos_disponibles,
            'instrumentos_no_disponibles': instrumentos_no_disponibles,
            'instrumentos_insuficientes': instrumentos_insuficientes,
            'total_instrumentos': len(set_quirurgico.instrumentos)
        }
    
    def duplicar_set(self, set_id: int, nuevo_nombre: str) -> Optional[SetQuirurgico]:
        """
        Duplicar un set quirúrgico existente
        """
        set_original = self.obtener_set_con_instrumentos(set_id)
        if not set_original:
            return None
        
        # Crear nuevo set
        nuevo_set = SetQuirurgico(
            nombre=nuevo_nombre,
            descripcion=f"Copia de: {set_original.descripcion or set_original.nombre}",
            especialidad=set_original.especialidad,
            activo=True
        )
        
        nuevo_set = self.create(nuevo_set)
        
        # Copiar instrumentos
        for relacion in set_original.instrumentos:
            self.agregar_instrumento_a_set(
                set_id=nuevo_set.set_id,
                instrumento_id=relacion.instrumento_id,
                cantidad=relacion.cantidad,
                obligatorio=relacion.obligatorio
            )
        
        return nuevo_set
    
    def obtener_estadisticas_sets(self) -> Dict[str, Any]:
        """
        Obtener estadísticas de sets quirúrgicos
        """
        # Total de sets
        total_sets = self.session.query(SetQuirurgico).count()
        sets_activos = self.session.query(SetQuirurgico).filter(SetQuirurgico.activo == True).count()
        
        # Sets por especialidad
        sets_por_especialidad = self.session.query(
            SetQuirurgico.especialidad,
            func.count(SetQuirurgico.set_id)
        ).filter(SetQuirurgico.activo == True)\
         .group_by(SetQuirurgico.especialidad)\
         .all()
        
        # Promedio de instrumentos por set
        avg_instrumentos = self.session.query(
            func.avg(func.count(SetInstrumento.instrumento_id))
        ).join(SetQuirurgico)\
         .filter(SetQuirurgico.activo == True)\
         .group_by(SetInstrumento.set_id)\
         .scalar()
        
        # Sets más utilizados (esto requeriría una tabla de uso que no está implementada)
        # Por ahora, mostraremos los sets con más instrumentos
        sets_mas_completos = self.session.query(
            SetQuirurgico.nombre,
            func.count(SetInstrumento.instrumento_id).label('total_instrumentos')
        ).join(SetInstrumento)\
         .filter(SetQuirurgico.activo == True)\
         .group_by(SetQuirurgico.set_id, SetQuirurgico.nombre)\
         .order_by(desc('total_instrumentos'))\
         .limit(10).all()
        
        return {
            'total_sets': total_sets,
            'sets_activos': sets_activos,
            'sets_inactivos': total_sets - sets_activos,
            'sets_por_especialidad': dict(sets_por_especialidad),
            'promedio_instrumentos_por_set': round(avg_instrumentos or 0, 2),
            'sets_mas_completos': [
                {'nombre': nombre, 'instrumentos': total}
                for nombre, total in sets_mas_completos
            ]
        }
    
    def buscar_sets(self, termino: str = None, especialidad: str = None, activo: bool = None) -> List[SetQuirurgico]:
        """
        Buscar sets quirúrgicos con filtros
        """
        query = self.session.query(SetQuirurgico)\
            .options(joinedload(SetQuirurgico.instrumentos))
        
        if termino:
            query = query.filter(
                SetQuirurgico.nombre.contains(termino) |
                SetQuirurgico.descripcion.contains(termino)
            )
        
        if especialidad:
            query = query.filter(SetQuirurgico.especialidad == especialidad)
        
        if activo is not None:
            query = query.filter(SetQuirurgico.activo == activo)
        
        return query.order_by(SetQuirurgico.nombre).all()
