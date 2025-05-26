"""
Servicio de comunicación para endpoints de Sets Quirúrgicos
Maneja todas las operaciones relacionadas con sets de instrumentos
"""
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class SetService:
    """
    Servicio para manejar comunicación con endpoints de sets quirúrgicos
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/sets"
    
    async def crear_set(self, set_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear un nuevo set quirúrgico
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.endpoint,
                json=set_data
            )
            
            if response.status_code == 201:
                return response.json()
            else:
                raise Exception(f"Error creando set: {response.text}")
    
    async def obtener_sets_activos(self) -> List[Dict[str, Any]]:
        """
        Obtener todos los sets quirúrgicos activos
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(self.endpoint)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo sets activos: {response.text}")
    
    async def obtener_set(self, set_id: int) -> Dict[str, Any]:
        """
        Obtener set específico por ID
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/{set_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo set: {response.text}")
    
    async def actualizar_set(self, set_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar información de un set quirúrgico
        """
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.endpoint}/{set_id}",
                json=datos
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error actualizando set: {response.text}")
    
    async def agregar_instrumento(self, set_id: int, instrumento_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agregar instrumento a un set
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.endpoint}/{set_id}/instrumentos",
                json=instrumento_data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error agregando instrumento al set: {response.text}")
    
    async def remover_instrumento(self, set_id: int, instrumento_id: int) -> Dict[str, Any]:
        """
        Remover instrumento de un set
        """
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.endpoint}/{set_id}/instrumentos/{instrumento_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error removiendo instrumento del set: {response.text}")
    
    async def obtener_sets_por_especialidad(self, especialidad: str) -> List[Dict[str, Any]]:
        """
        Obtener sets filtrados por especialidad
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/especialidad/{especialidad}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo sets por especialidad: {response.text}")
    
    async def verificar_disponibilidad(self, set_id: int) -> Dict[str, Any]:
        """
        Verificar disponibilidad de todos los instrumentos de un set
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/{set_id}/disponibilidad")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error verificando disponibilidad del set: {response.text}")
    
    async def duplicar_set(self, set_id: int, nuevo_nombre: str) -> Dict[str, Any]:
        """
        Duplicar un set existente
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.endpoint}/{set_id}/duplicar",
                json={"nuevo_nombre": nuevo_nombre}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error duplicando set: {response.text}")
    
    async def buscar_sets(self, termino: str) -> List[Dict[str, Any]]:
        """
        Buscar sets por término
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/buscar",
                params={"q": termino}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error buscando sets: {response.text}")
    
    async def obtener_estadisticas_sets(self) -> Dict[str, Any]:
        """
        Obtener estadísticas de sets quirúrgicos
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/estadisticas")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo estadísticas de sets: {response.text}")
    
    async def eliminar_set(self, set_id: int) -> Dict[str, Any]:
        """
        Eliminar set del sistema
        """
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.endpoint}/{set_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error eliminando set: {response.text}")
