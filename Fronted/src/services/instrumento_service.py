"""
Servicio para la gestión de instrumentos
"""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from src.services.base_service import BaseService
from src.api.models.instrumento import Instrumento
from src.api.models.estado_instrumento import EstadoInstrumento

class InstrumentoService(BaseService[Instrumento]):
    """
    Servicio para la gestión de instrumentos
    """
    
    def __init__(self):
        super().__init__(Instrumento)
    
    def get_by_codigo(self, db: Session, codigo: str) -> Optional[Instrumento]:
        """
        Obtener un instrumento por código
        """
        return db.query(Instrumento).filter(Instrumento.codigo_instrumento == codigo).first()
    
    def get_with_estado(self, db: Session, instrumento_id: int) -> Optional[Instrumento]:
        """
        Obtener un instrumento con su estado cargado
        """
        return db.query(Instrumento).options(
            joinedload(Instrumento.estado)
        ).filter(Instrumento.instrumento_id == instrumento_id).first()
    
    def get_by_estado(self, db: Session, estado_id: int) -> List[Instrumento]:
        """
        Obtener instrumentos por estado
        """
        return db.query(Instrumento).filter(Instrumento.estado_id == estado_id).all()
    
    def get_que_requieren_mantenimiento(self, db: Session) -> List[Instrumento]:
        """
        Obtener instrumentos que requieren mantenimiento
        """
        return db.query(Instrumento).join(EstadoInstrumento).filter(
            EstadoInstrumento.requiere_mantenimiento == True
        ).all()
    
    def incrementar_uso(self, db: Session, instrumento_id: int) -> bool:
        """
        Incrementar el contador de uso de un instrumento
        """
        instrumento = self.get_by_id(db, instrumento_id)
        if instrumento:
            instrumento.contador_uso += 1
            db.commit()
            return True
        return False
    
    def actualizar_esterilizacion(self, db: Session, instrumento_id: int, fecha_esterilizacion) -> bool:
        """
        Actualizar la fecha de última esterilización
        """
        return self.update(db, instrumento_id, {
            'ultima_esterilizacion': fecha_esterilizacion
        }) is not None
    
    def buscar_por_nombre(self, db: Session, termino: str) -> List[Instrumento]:
        """
        Buscar instrumentos por nombre (búsqueda parcial)
        """
        return db.query(Instrumento).filter(
            Instrumento.nombre_instrumento.ilike(f"%{termino}%")
        ).all()
