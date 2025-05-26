"""
Servicio de comunicación para endpoints de Procedimientos
Maneja todas las operaciones relacionadas con procedimientos quirúrgicos
"""
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import json


class ProcedimientoService:
    """
    Servicio para manejar comunicación con endpoints de procedimientos
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/procedimientos"
    
    async def crear_procedimiento(self, procedimiento_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear un nuevo procedimiento quirúrgico
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.endpoint,
                json=procedimiento_data
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(f"Error creando procedimiento: {response.text}")
    
    async def obtener_procedimientos(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtener lista de procedimientos con paginación
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.endpoint,
                params={"skip": skip, "limit": limit}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo procedimientos: {response.text}")
    
    async def obtener_procedimientos_activos(self) -> List[Dict[str, Any]]:
        """
        Obtener procedimientos activos (INICIADO o EN_PROCESO)
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/activos")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo procedimientos activos: {response.text}")
    
    async def obtener_procedimientos_por_fecha(self, fecha: date) -> List[Dict[str, Any]]:
        """
        Obtener procedimientos por fecha específica
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/fecha/{fecha.isoformat()}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo procedimientos por fecha: {response.text}")
    
    async def obtener_procedimiento(self, procedimiento_id: int) -> Dict[str, Any]:
        """
        Obtener procedimiento específico por ID
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/{procedimiento_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo procedimiento: {response.text}")
    
    async def actualizar_procedimiento(self, procedimiento_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar información de procedimiento
        """
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.endpoint}/{procedimiento_id}",
                json=datos
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error actualizando procedimiento: {response.text}")
    
    async def finalizar_procedimiento(self, procedimiento_id: int) -> Dict[str, Any]:
        """
        Finalizar un procedimiento quirúrgico
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.endpoint}/{procedimiento_id}/finalizar")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error finalizando procedimiento: {response.text}")
    
    async def eliminar_procedimiento(self, procedimiento_id: int) -> Dict[str, Any]:
        """
        Eliminar procedimiento del sistema
        """
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.endpoint}/{procedimiento_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error eliminando procedimiento: {response.text}")
    
    async def obtener_estadisticas_procedimientos(self) -> Dict[str, Any]:
        """
        Obtener estadísticas de procedimientos
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/estadisticas")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo estadísticas de procedimientos: {response.text}")
    
    async def buscar_procedimientos(self, termino: str) -> List[Dict[str, Any]]:
        """
        Buscar procedimientos por término
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/buscar",
                params={"q": termino}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error buscando procedimientos: {response.text}")
