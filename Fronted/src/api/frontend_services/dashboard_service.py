"""
Servicio de comunicación para endpoints de Dashboard
Maneja todas las operaciones relacionadas con estadísticas y métricas del dashboard
"""
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime, date
import json


class DashboardService:
    """
    Servicio para manejar comunicación con endpoints del dashboard
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/dashboard"
    
    async def obtener_estadisticas_dashboard(
        self, 
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Obtener estadísticas generales del dashboard
        """
        params = {}
        if fecha_inicio:
            params["fecha_inicio"] = fecha_inicio.isoformat()
        if fecha_fin:
            params["fecha_fin"] = fecha_fin.isoformat()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/stats",
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo estadísticas: {response.text}")
    
    async def obtener_resumen_alertas(self, limit: int = 5) -> Dict[str, Any]:
        """
        Obtener resumen de alertas para el dashboard
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/alertas-summary",
                params={"limit": limit}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo resumen de alertas: {response.text}")
    
    async def obtener_dashboard_completo(
        self, 
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Obtener todos los datos del dashboard en una sola llamada
        """
        params = {}
        if fecha_inicio:
            params["fecha_inicio"] = fecha_inicio.isoformat()
        if fecha_fin:
            params["fecha_fin"] = fecha_fin.isoformat()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/completo",
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo dashboard completo: {response.text}")
    
    async def obtener_instrumentos_criticos(self) -> List[Dict[str, Any]]:
        """
        Obtener instrumentos que requieren atención crítica
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/instrumentos-criticos")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo instrumentos críticos: {response.text}")
    
    async def obtener_procedimientos_activos(self) -> List[Dict[str, Any]]:
        """
        Obtener procedimientos quirúrgicos activos
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/procedimientos-activos")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo procedimientos activos: {response.text}")
    
    async def obtener_conteos_pendientes(self) -> List[Dict[str, Any]]:
        """
        Obtener conteos de instrumentos pendientes de verificación
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/conteos-pendientes")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo conteos pendientes: {response.text}")
    
    async def obtener_estadisticas_uso(
        self, 
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Obtener estadísticas de uso de instrumentos
        """
        params = {}
        if fecha_inicio:
            params["fecha_inicio"] = fecha_inicio.isoformat()
        if fecha_fin:
            params["fecha_fin"] = fecha_fin.isoformat()
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/estadisticas-uso",
                params=params
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo estadísticas de uso: {response.text}")
    
    async def obtener_tendencias_mantenimiento(self) -> Dict[str, Any]:
        """
        Obtener tendencias de mantenimiento de instrumentos
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/tendencias-mantenimiento")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo tendencias de mantenimiento: {response.text}")
