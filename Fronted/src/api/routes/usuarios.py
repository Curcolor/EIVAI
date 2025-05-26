"""
Rutas API para usuarios y autenticación
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.api.schemas import (
    UsuarioCreate, UsuarioUpdate, UsuarioResponse, 
    LoginRequest, LoginResponse, ResponseMessage,
    PaginationParams
)
from src.api.controllers.usuario_controller import UsuarioController

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])
usuario_controller = UsuarioController()

@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Autenticar usuario en el sistema
    """
    return await usuario_controller.login(db, login_data)

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo usuario en el sistema
    """
    return await usuario_controller.create_usuario(db, usuario)

@router.get("/", response_model=List[UsuarioResponse])
async def get_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de usuarios con paginación
    """
    return await usuario_controller.get_usuarios(db, skip=skip, limit=limit)

@router.get("/activos", response_model=List[UsuarioResponse])
async def get_usuarios_activos(
    db: Session = Depends(get_db)
):
    """
    Obtener lista de usuarios activos
    """
    return await usuario_controller.get_usuarios_activos(db)

@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener usuario específico por ID
    """
    return await usuario_controller.get_usuario(db, usuario_id)

@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def update_usuario(
    usuario_id: int,
    usuario: UsuarioUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar información de usuario
    """
    return await usuario_controller.update_usuario(db, usuario_id, usuario)
