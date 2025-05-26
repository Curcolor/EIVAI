"""
Servicio de comunicación para endpoints de Alertas
Maneja todas las operaciones relacionadas con alertas del sistema
"""
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class AlertaService:
    """
    Servicio para manejar comunicación con endpoints de alertas
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/alertas"
    
    async def crear_alerta(self, alerta_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear una nueva alerta
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.endpoint,
                json=alerta_data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error creando alerta: {response.text}")
    
    async def listar_alertas(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        prioridad: Optional[str] = None,
        resuelta: Optional[bool] = None,
        tipo_alerta: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Listar alertas con filtros opcionales
        """
        params = {"skip": skip, "limit": limit}
        if prioridad:
            params["prioridad"] = prioridad
        if resuelta is not None:
            params["resuelta"] = resuelta
        if tipo_alerta:
            params["tipo_alerta"] = tipo_alerta
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.endpoint, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo alertas: {response.text}")
    
    async def obtener_alerta(self, alerta_id: int) -> Dict[str, Any]:
        """
        Obtener alerta específica
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/{alerta_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo alerta: {response.text}")
    
    async def actualizar_alerta(self, alerta_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar una alerta
        """
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.endpoint}/{alerta_id}",
                json=datos
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error actualizando alerta: {response.text}")
    
    async def eliminar_alerta(self, alerta_id: int) -> Dict[str, Any]:
        """
        Eliminar una alerta
        """
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{self.endpoint}/{alerta_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error eliminando alerta: {response.text}")
    
    async def obtener_alertas_criticas(self) -> List[Dict[str, Any]]:
        """
        Obtener todas las alertas críticas sin resolver
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/criticas/lista")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo alertas críticas: {response.text}")
    
    async def resolver_alerta(self, alerta_id: int, observaciones: Optional[str] = None) -> Dict[str, Any]:
        """
        Marcar una alerta como resuelta
        """
        data = {}
        if observaciones:
            data["observaciones"] = observaciones
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.endpoint}/{alerta_id}/resolver",
                json=data if data else None
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error resolviendo alerta: {response.text}")
    
    async def obtener_estadisticas_alertas(
        self, 
        fecha_inicio: Optional[str] = None, 
        fecha_fin: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Obtener estadísticas de alertas
        """
        params = {}
        if fecha_inicio:
            params["fecha_inicio"] = fecha_inicio
        if fecha_fin:
            params["fecha_fin"] = fecha_fin
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/estadisticas/resumen",
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo estadísticas de alertas: {response.text}")
    
    async def obtener_alertas_activas(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Obtener alertas activas
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/activas",
                params={"limit": limit}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo alertas activas: {response.text}")
    
    async def obtener_alertas_por_tipo(self, tipo_alerta: str) -> List[Dict[str, Any]]:
        """
        Obtener alertas por tipo específico
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/tipo/{tipo_alerta}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo alertas por tipo: {response.text}")
    
    async def obtener_resumen_alertas(self) -> Dict[str, Any]:
        """
        Obtener resumen rápido de alertas para dashboard
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/resumen")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo resumen de alertas: {response.text}")
