"""
Servicio base para operaciones CRUD
"""
from typing import Generic, TypeVar, Type, List, Optional, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.api.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseService(Generic[ModelType]):
    """
    Servicio base genérico para operaciones CRUD
    """
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        """
        Obtener un registro por ID
        """
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error al obtener registro: {str(e)}")
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Obtener todos los registros con paginación
        """
        try:
            return db.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error al obtener registros: {str(e)}")
    
    def get_by_filters(self, db: Session, filters: Dict[str, Any], 
                      skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        Obtener registros filtrados
        """
        try:
            query = db.query(self.model)
            for key, value in filters.items():
                if hasattr(self.model, key):
                    query = query.filter(getattr(self.model, key) == value)
            return query.offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error al filtrar registros: {str(e)}")
    
    def create(self, db: Session, obj_data: Dict[str, Any]) -> ModelType:
        """
        Crear un nuevo registro
        """
        try:
            db_obj = self.model(**obj_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error al crear registro: {str(e)}")
    
    def update(self, db: Session, id: int, obj_data: Dict[str, Any]) -> Optional[ModelType]:
        """
        Actualizar un registro existente
        """
        try:
            db_obj = self.get_by_id(db, id)
            if not db_obj:
                return None
            
            for key, value in obj_data.items():
                if hasattr(db_obj, key):
                    setattr(db_obj, key, value)
            
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error al actualizar registro: {str(e)}")
    
    def delete(self, db: Session, id: int) -> bool:
        """
        Eliminar un registro
        """
        try:
            db_obj = self.get_by_id(db, id)
            if not db_obj:
                return False
            
            db.delete(db_obj)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error al eliminar registro: {str(e)}")
    
    def count(self, db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Contar registros
        """
        try:
            query = db.query(self.model)
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key):
                        query = query.filter(getattr(self.model, key) == value)
            return query.count()
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error al contar registros: {str(e)}")
