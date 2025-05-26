"""
Servicio para la gestión de usuarios
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from src.services.base_service import BaseService
from src.api.models.usuario import Usuario
import hashlib

class UsuarioService(BaseService[Usuario]):
    """
    Servicio para la gestión de usuarios
    """
    
    def __init__(self):
        super().__init__(Usuario)
    
    def get_by_username(self, db: Session, username: str) -> Optional[Usuario]:
        """
        Obtener un usuario por nombre de usuario
        """
        return db.query(Usuario).filter(Usuario.nombre_usuario == username).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[Usuario]:
        """
        Obtener un usuario por email
        """
        return db.query(Usuario).filter(Usuario.email == email).first()
    
    def authenticate(self, db: Session, username: str, password: str) -> Optional[Usuario]:
        """
        Autenticar un usuario
        """
        user = self.get_by_username(db, username)
        if user and self.verify_password(password, user.password_hash):
            # Actualizar último acceso
            from datetime import datetime
            user.ultimo_acceso = datetime.utcnow()
            db.commit()
            return user
        return None
    
    def create_user(self, db: Session, username: str, nombre_completo: str, 
                   email: str, password: str) -> Usuario:
        """
        Crear un nuevo usuario
        """
        password_hash = self.hash_password(password)
        user_data = {
            'nombre_usuario': username,
            'nombre_completo': nombre_completo,
            'email': email,
            'password_hash': password_hash,
            'activo': True
        }
        return self.create(db, user_data)
    
    def change_password(self, db: Session, user_id: int, new_password: str) -> bool:
        """
        Cambiar la contraseña de un usuario
        """
        password_hash = self.hash_password(new_password)
        result = self.update(db, user_id, {'password_hash': password_hash})
        return result is not None
    
    def get_active_users(self, db: Session) -> List[Usuario]:
        """
        Obtener todos los usuarios activos
        """
        return db.query(Usuario).filter(Usuario.activo == True).all()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash de contraseña usando SHA256
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Verificar contraseña
        """
        return hashlib.sha256(password.encode()).hexdigest() == hashed
