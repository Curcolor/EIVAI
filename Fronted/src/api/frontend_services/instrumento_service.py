"""
Servicio de comunicación para endpoints de Instrumentos
Maneja todas las operaciones relacionadas con instrumentos quirúrgicos
"""
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class InstrumentoService:
    """
    Servicio para manejar comunicación con endpoints de instrumentos
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/instrumentos"
    
    async def crear_instrumento(self, instrumento_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear un nuevo instrumento
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.endpoint,
                json=instrumento_data
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(f"Error creando instrumento: {response.text}")
    
    async def obtener_instrumentos(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtener lista de instrumentos con paginación
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.endpoint,
                params={"skip": skip, "limit": limit}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo instrumentos: {response.text}")
    
    async def obtener_estadisticas_uso(self) -> List[Dict[str, Any]]:
        """
        Obtener estadísticas de uso de instrumentos
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/estadisticas")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo estadísticas: {response.text}")
    
    async def obtener_instrumentos_mantenimiento(self) -> List[Dict[str, Any]]:
        """
        Obtener instrumentos que requieren mantenimiento
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/mantenimiento")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo instrumentos en mantenimiento: {response.text}")
    
    async def obtener_instrumento(self, instrumento_id: int) -> Dict[str, Any]:
        """
        Obtener instrumento específico por ID
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/{instrumento_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo instrumento: {response.text}")
    
    async def actualizar_instrumento(self, instrumento_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar información de instrumento
        """
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.endpoint}/{instrumento_id}",
                json=datos
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error actualizando instrumento: {response.text}")
    
    async def eliminar_instrumento(self, instrumento_id: int) -> Dict[str, Any]:
        """
        Eliminar instrumento del sistema
        """
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.endpoint}/{instrumento_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error eliminando instrumento: {response.text}")
    
    async def buscar_instrumentos(self, termino: str) -> List[Dict[str, Any]]:
        """
        Buscar instrumentos por término
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/buscar",
                params={"q": termino}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error buscando instrumentos: {response.text}")
    
    async def obtener_instrumentos_activos(self) -> List[Dict[str, Any]]:
        """
        Obtener instrumentos activos disponibles
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/activos")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo instrumentos activos: {response.text}")
    
    async def obtener_instrumentos_por_estado(self, estado: str) -> List[Dict[str, Any]]:
        """
        Obtener instrumentos filtrados por estado
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/estado/{estado}"
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo instrumentos por estado: {response.text}")
