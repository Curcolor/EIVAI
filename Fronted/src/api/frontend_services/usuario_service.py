"""
Servicio de comunicación para endpoints de Usuarios
Maneja todas las operaciones relacionadas con usuarios y autenticación
"""
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class UsuarioService:
    """
    Servicio para manejar comunicación con endpoints de usuarios
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/usuarios"
    
    async def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Autenticar usuario en el sistema
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.endpoint}/login",
                json={
                    "username": username,
                    "password": password
                }
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error en login: {response.text}")
    
    async def crear_usuario(self, usuario_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear un nuevo usuario en el sistema
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.endpoint,
                json=usuario_data
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(f"Error creando usuario: {response.text}")
    
    async def obtener_usuarios(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtener lista de usuarios con paginación
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.endpoint,
                params={"skip": skip, "limit": limit}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo usuarios: {response.text}")
    
    async def obtener_usuarios_activos(self) -> List[Dict[str, Any]]:
        """
        Obtener usuarios activos
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/activos")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo usuarios activos: {response.text}")
    
    async def obtener_usuario(self, usuario_id: int) -> Dict[str, Any]:
        """
        Obtener usuario específico por ID
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/{usuario_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo usuario: {response.text}")
    
    async def actualizar_usuario(self, usuario_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar información de usuario
        """
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.endpoint}/{usuario_id}",
                json=datos
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error actualizando usuario: {response.text}")
    
    async def eliminar_usuario(self, usuario_id: int) -> Dict[str, Any]:
        """
        Eliminar usuario del sistema
        """
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.endpoint}/{usuario_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error eliminando usuario: {response.text}")
