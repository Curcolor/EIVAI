"""
Servicio de comunicación para endpoints de Conteos
Maneja todas las operaciones relacionadas con conteos de instrumentos
"""
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class ConteoService:
    """
    Servicio para manejar comunicación con endpoints de conteos
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.endpoint = f"{base_url}/api/conteos"
    
    async def crear_conteo(self, conteo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear un nuevo conteo de instrumento
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.endpoint,
                json=conteo_data
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error creando conteo: {response.text}")
    
    async def crear_conteo_con_fotos(self, conteo_data: Dict[str, Any], fotos: List[bytes]) -> Dict[str, Any]:
        """
        Crear conteo con fotos adjuntas
        """
        async with httpx.AsyncClient() as client:
            files = [("fotos", foto) for foto in fotos]
            
            response = await client.post(
                f"{self.endpoint}/with-photos",
                data=conteo_data,
                files=files
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error creando conteo con fotos: {response.text}")
    
    async def obtener_conteos(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Obtener lista de conteos con paginación
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.endpoint,
                params={"skip": skip, "limit": limit}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo conteos: {response.text}")
    
    async def obtener_conteo(self, conteo_id: int) -> Dict[str, Any]:
        """
        Obtener conteo específico por ID
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/{conteo_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo conteo: {response.text}")
    
    async def actualizar_conteo(self, conteo_id: int, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualizar información de conteo
        """
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.endpoint}/{conteo_id}",
                json=datos
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error actualizando conteo: {response.text}")
    
    async def verificar_conteo(self, conteo_id: int) -> Dict[str, Any]:
        """
        Verificar y procesar un conteo específico
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.endpoint}/{conteo_id}/verificar")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error verificando conteo: {response.text}")
    
    async def obtener_conteos_procedimiento(self, procedimiento_id: int) -> List[Dict[str, Any]]:
        """
        Obtener conteos de un procedimiento específico
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/procedimiento/{procedimiento_id}")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo conteos del procedimiento: {response.text}")
    
    async def obtener_resumen_conteos_procedimiento(self, procedimiento_id: int) -> Dict[str, Any]:
        """
        Obtener resumen de conteos para un procedimiento específico
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/procedimiento/{procedimiento_id}/resumen")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo resumen de conteos: {response.text}")
    
    async def obtener_conteos_pendientes(self) -> List[Dict[str, Any]]:
        """
        Obtener conteos pendientes de verificación
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/pendientes")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo conteos pendientes: {response.text}")
    
    async def obtener_estadisticas_discrepancias(self) -> Dict[str, Any]:
        """
        Obtener estadísticas de discrepancias en conteos
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.endpoint}/estadisticas/discrepancias")
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo estadísticas de discrepancias: {response.text}")
    
    async def obtener_conteos_por_fecha(self, fecha: str) -> List[Dict[str, Any]]:
        """
        Obtener conteos filtrados por fecha
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.endpoint}/fecha/{fecha}"
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error obteniendo conteos por fecha: {response.text}")
