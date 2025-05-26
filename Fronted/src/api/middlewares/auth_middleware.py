# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\api\middlewares\auth_middleware.py
"""
Middleware de autenticación para el sistema EIVAI - FastAPI
"""
from typing import Optional
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.services.usuario_service import UsuarioService
from src.api.models.usuario import Usuario

# Esquema de seguridad Bearer Token
security = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """
    Obtener usuario actual a partir del token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        usuario_service = UsuarioService()
        
        # En un sistema real, aquí validarías el JWT token
        # Por ahora, simulamos con el token como user_id
        try:
            user_id = int(token.credentials)
        except ValueError:
            raise credentials_exception
        
        usuario = usuario_service.get_by_id(db, user_id)
        if usuario is None:
            raise credentials_exception
            
        if not usuario.activo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
            
        return usuario
        
    except Exception:
        raise credentials_exception


async def require_auth(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """
    Dependencia que requiere autenticación
    """
    return current_user


async def require_admin(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    """
    Dependencia que requiere privilegios de administrador
    """
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren privilegios de administrador"
        )
    return current_user


async def get_optional_user(
    token: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[Usuario]:
    """
    Obtener usuario opcional (para rutas que funcionan con o sin autenticación)
    """
    if not token:
        return None
    
    try:
        return await get_current_user(token, db)
    except HTTPException:
        return None


# Funciones de compatibilidad con el sistema existente
def cors_middleware():
    """
    Middleware de CORS (se configurará en la aplicación principal)
    """
    pass


def session_middleware():
    """
    Middleware de sesión (se configurará en la aplicación principal)
    """
    pass


# Decoradores legacy para compatibilidad (no usar en nuevas rutas)
def token_required(f):
    """
    Decorator legacy para compatibilidad
    """
    def wrapper(*args, **kwargs):
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Usar FastAPI dependencies en lugar de decoradores Flask"
        )
    return wrapper


def admin_required(f):
    """
    Decorator legacy para compatibilidad
    """
    def wrapper(*args, **kwargs):
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Usar FastAPI dependencies en lugar de decoradores Flask"
        )
    return wrapper
