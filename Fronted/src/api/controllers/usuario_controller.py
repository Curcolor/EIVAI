"""
Controlador para la gestión de usuarios y autenticación
"""
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.api.schemas import (
    UsuarioCreate, UsuarioUpdate, UsuarioResponse, 
    LoginRequest, LoginResponse, ResponseMessage
)
from src.services.usuario_service import UsuarioService
from src.api.models.usuario import Usuario

class UsuarioController:
    def __init__(self):
        self.usuario_service = UsuarioService()
    
    async def login(self, db: Session, login_data: LoginRequest) -> LoginResponse:
        """Autenticar usuario"""
        try:
            usuario = self.usuario_service.authenticate(
                db, login_data.username, login_data.password
            )
            
            if not usuario:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales incorrectas"
                )
            
            if not usuario.activo:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Usuario inactivo"
                )
            
            # Token simple (en producción usar JWT)
            token = f"token_{usuario.usuario_id}_{usuario.nombre_usuario}"
            
            return LoginResponse(
                usuario=UsuarioResponse.from_orm(usuario),
                token=token,
                message="Login exitoso"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno: {str(e)}"
            )
    
    async def create_usuario(self, db: Session, usuario_data: UsuarioCreate) -> UsuarioResponse:
        """Crear nuevo usuario"""
        try:
            # Verificar si el usuario ya existe
            existing_user = self.usuario_service.get_by_username(db, usuario_data.nombre_usuario)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de usuario ya existe"
                )
            
            existing_email = self.usuario_service.get_by_email(db, usuario_data.email)
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El email ya está registrado"
                )
            
            # Crear usuario
            usuario = self.usuario_service.create_user(
                db=db,
                username=usuario_data.nombre_usuario,
                nombre_completo=usuario_data.nombre_completo,
                email=usuario_data.email,
                password=usuario_data.password
            )
            
            return UsuarioResponse.from_orm(usuario)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear usuario: {str(e)}"
            )
    
    async def get_usuarios(self, db: Session, skip: int = 0, limit: int = 100) -> List[UsuarioResponse]:
        """Obtener lista de usuarios"""
        try:
            usuarios = self.usuario_service.get_all(db, skip=skip, limit=limit)
            return [UsuarioResponse.from_orm(usuario) for usuario in usuarios]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener usuarios: {str(e)}"
            )
    
    async def get_usuario(self, db: Session, usuario_id: int) -> UsuarioResponse:
        """Obtener usuario por ID"""
        try:
            usuario = self.usuario_service.get_by_id(db, usuario_id)
            if not usuario:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            return UsuarioResponse.from_orm(usuario)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener usuario: {str(e)}"
            )
    
    async def update_usuario(self, db: Session, usuario_id: int, usuario_data: UsuarioUpdate) -> UsuarioResponse:
        """Actualizar usuario"""
        try:
            # Verificar que el usuario existe
            usuario_existente = self.usuario_service.get_by_id(db, usuario_id)
            if not usuario_existente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Preparar datos para actualizar
            update_data = {}
            if usuario_data.nombre_completo is not None:
                update_data['nombre_completo'] = usuario_data.nombre_completo
            if usuario_data.email is not None:
                update_data['email'] = usuario_data.email
            if usuario_data.activo is not None:
                update_data['activo'] = usuario_data.activo
            
            # Actualizar usuario
            usuario = self.usuario_service.update(db, usuario_id, update_data)
            return UsuarioResponse.from_orm(usuario)
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar usuario: {str(e)}"
            )
    
    async def get_usuarios_activos(self, db: Session) -> List[UsuarioResponse]:
        """Obtener usuarios activos"""
        try:
            usuarios = self.usuario_service.get_active_users(db)
            return [UsuarioResponse.from_orm(usuario) for usuario in usuarios]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener usuarios activos: {str(e)}"
            )
