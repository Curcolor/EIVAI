# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\utils\background_tasks.py
"""
Tareas en segundo plano para el sistema EIVAI
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List

from ..services.alerta_service import AlertaService
from ..services.instrumento_service import InstrumentoService
from ..services.conteo_service import ConteoService
from ..config.database import get_db

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BackgroundTaskManager:
    """
    Gestor de tareas en segundo plano
    """
    
    def __init__(self):
        self.alerta_service = AlertaService()
        self.instrumento_service = InstrumentoService()
        self.conteo_service = ConteoService()
        self.running = False
        self.tasks = []
    
    async def start_background_tasks(self):
        """
        Iniciar todas las tareas en segundo plano
        """
        if self.running:
            logger.warning("Las tareas en segundo plano ya están ejecutándose")
            return
        
        self.running = True
        logger.info("Iniciando tareas en segundo plano...")
        
        # Crear tareas
        self.tasks = [
            asyncio.create_task(self._verificar_alertas_automaticas()),
            asyncio.create_task(self._verificar_mantenimiento_instrumentos()),
            asyncio.create_task(self._verificar_conteos_pendientes()),
            asyncio.create_task(self._limpiar_alertas_resueltas()),
        ]
        
        # Ejecutar tareas
        await asyncio.gather(*self.tasks, return_exceptions=True)
    
    async def stop_background_tasks(self):
        """
        Detener todas las tareas en segundo plano
        """
        self.running = False
        logger.info("Deteniendo tareas en segundo plano...")
        
        for task in self.tasks:
            if not task.done():
                task.cancel()
        
        # Esperar a que las tareas terminen
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()
        
        logger.info("Tareas en segundo plano detenidas")
    
    async def _verificar_alertas_automaticas(self):
        """
        Verificar y generar alertas automáticas cada 5 minutos
        """
        while self.running:
            try:
                logger.info("Verificando alertas automáticas...")
                
                async with get_db() as db:
                    # Verificar instrumentos que necesitan mantenimiento
                    await self._generar_alertas_mantenimiento(db)
                    
                    # Verificar conteos con discrepancias
                    await self._generar_alertas_discrepancias(db)
                    
                    # Verificar procedimientos con demoras
                    await self._generar_alertas_procedimientos(db)
                
                logger.info("Verificación de alertas automáticas completada")
                
            except Exception as e:
                logger.error(f"Error en verificación de alertas automáticas: {str(e)}")
            
            # Esperar 5 minutos antes de la siguiente verificación
            await asyncio.sleep(300)
    
    async def _verificar_mantenimiento_instrumentos(self):
        """
        Verificar instrumentos que requieren mantenimiento cada hora
        """
        while self.running:
            try:
                logger.info("Verificando mantenimiento de instrumentos...")
                
                async with get_db() as db:
                    # Obtener instrumentos con mantenimiento vencido
                    instrumentos_vencidos = await self.instrumento_service.obtener_instrumentos_mantenimiento_vencido()
                    
                    for instrumento in instrumentos_vencidos:
                        # Verificar si ya existe una alerta para este instrumento
                        alertas_existentes = await self.alerta_service.buscar_alertas({
                            'instrumento_id': instrumento.instrumento_id,
                            'tipo_alerta': 'MANTENIMIENTO_VENCIDO',
                            'resuelta': False
                        })
                        
                        if not alertas_existentes:
                            # Crear nueva alerta de mantenimiento
                            await self.alerta_service.crear_alerta({
                                'tipo_alerta': 'MANTENIMIENTO_VENCIDO',
                                'mensaje': f'El instrumento {instrumento.codigo_instrumento} tiene mantenimiento vencido',
                                'prioridad': 'ALTA',
                                'instrumento_id': instrumento.instrumento_id
                            })
                            
                            logger.info(f"Alerta de mantenimiento creada para instrumento {instrumento.codigo_instrumento}")
                
                logger.info("Verificación de mantenimiento completada")
                
            except Exception as e:
                logger.error(f"Error en verificación de mantenimiento: {str(e)}")
            
            # Esperar 1 hora antes de la siguiente verificación
            await asyncio.sleep(3600)
    
    async def _verificar_conteos_pendientes(self):
        """
        Verificar conteos pendientes de resolución cada 15 minutos
        """
        while self.running:
            try:
                logger.info("Verificando conteos pendientes...")
                
                async with get_db() as db:
                    # Obtener conteos con discrepancias sin resolver hace más de 30 minutos
                    tiempo_limite = datetime.now() - timedelta(minutes=30)
                    
                    conteos_pendientes = await self.conteo_service.obtener_conteos_discrepancia_sin_resolver(
                        tiempo_limite
                    )
                    
                    for conteo in conteos_pendientes:
                        # Verificar si ya existe una alerta para este conteo
                        alertas_existentes = await self.alerta_service.buscar_alertas({
                            'procedimiento_id': conteo.procedimiento_id,
                            'tipo_alerta': 'CONTEO_PENDIENTE',
                            'resuelta': False
                        })
                        
                        if not alertas_existentes:
                            # Crear alerta de conteo pendiente
                            await self.alerta_service.crear_alerta({
                                'tipo_alerta': 'CONTEO_PENDIENTE',
                                'mensaje': f'Conteo con discrepancia pendiente de resolución desde hace más de 30 minutos',
                                'prioridad': 'CRITICA',
                                'procedimiento_id': conteo.procedimiento_id
                            })
                            
                            logger.info(f"Alerta de conteo pendiente creada para procedimiento {conteo.procedimiento_id}")
                
                logger.info("Verificación de conteos pendientes completada")
                
            except Exception as e:
                logger.error(f"Error en verificación de conteos pendientes: {str(e)}")
            
            # Esperar 15 minutos antes de la siguiente verificación
            await asyncio.sleep(900)
    
    async def _limpiar_alertas_resueltas(self):
        """
        Limpiar alertas resueltas antiguas cada 24 horas
        """
        while self.running:
            try:
                logger.info("Limpiando alertas resueltas antiguas...")
                
                async with get_db() as db:
                    # Eliminar alertas resueltas de hace más de 30 días
                    fecha_limite = datetime.now() - timedelta(days=30)
                    
                    alertas_eliminadas = await self.alerta_service.eliminar_alertas_antiguas(fecha_limite)
                    
                    if alertas_eliminadas > 0:
                        logger.info(f"Se eliminaron {alertas_eliminadas} alertas resueltas antiguas")
                
                logger.info("Limpieza de alertas completada")
                
            except Exception as e:
                logger.error(f"Error en limpieza de alertas: {str(e)}")
            
            # Esperar 24 horas antes de la siguiente limpieza
            await asyncio.sleep(86400)
    
    async def _generar_alertas_mantenimiento(self, db):
        """
        Generar alertas de mantenimiento
        """
        # Obtener instrumentos próximos a mantenimiento (7 días)
        fecha_limite = datetime.now() + timedelta(days=7)
        instrumentos_proximos = await self.instrumento_service.obtener_instrumentos_mantenimiento_proximo(
            fecha_limite
        )
        
        for instrumento in instrumentos_proximos:
            # Verificar si ya existe alerta
            alertas_existentes = await self.alerta_service.buscar_alertas({
                'instrumento_id': instrumento.instrumento_id,
                'tipo_alerta': 'MANTENIMIENTO_PROXIMO',
                'resuelta': False
            })
            
            if not alertas_existentes:
                await self.alerta_service.crear_alerta({
                    'tipo_alerta': 'MANTENIMIENTO_PROXIMO',
                    'mensaje': f'El instrumento {instrumento.codigo_instrumento} requiere mantenimiento próximamente',
                    'prioridad': 'MEDIA',
                    'instrumento_id': instrumento.instrumento_id
                })
    
    async def _generar_alertas_discrepancias(self, db):
        """
        Generar alertas por discrepancias en conteos
        """
        # Obtener conteos recientes con discrepancias
        tiempo_limite = datetime.now() - timedelta(hours=1)
        conteos_discrepancia = await self.conteo_service.obtener_conteos_con_discrepancia(
            fecha_desde=tiempo_limite
        )
        
        for conteo in conteos_discrepancia:
            # Verificar si ya existe alerta
            alertas_existentes = await self.alerta_service.buscar_alertas({
                'procedimiento_id': conteo.procedimiento_id,
                'tipo_alerta': 'DISCREPANCIA_CONTEO',
                'resuelta': False
            })
            
            if not alertas_existentes:
                await self.alerta_service.crear_alerta({
                    'tipo_alerta': 'DISCREPANCIA_CONTEO',
                    'mensaje': f'Discrepancia detectada en conteo de {conteo.instrumento.nombre_instrumento}',
                    'prioridad': 'ALTA',
                    'procedimiento_id': conteo.procedimiento_id
                })
    
    async def _generar_alertas_procedimientos(self, db):
        """
        Generar alertas por procedimientos con demoras
        """
        # Obtener procedimientos activos con más de 4 horas
        tiempo_limite = datetime.now() - timedelta(hours=4)
        
        from ..services.procedimiento_service import ProcedimientoService
        procedimiento_service = ProcedimientoService()
        
        procedimientos_largos = await procedimiento_service.obtener_procedimientos_activos_largos(
            tiempo_limite
        )
        
        for procedimiento in procedimientos_largos:
            # Verificar si ya existe alerta
            alertas_existentes = await self.alerta_service.buscar_alertas({
                'procedimiento_id': procedimiento.procedimiento_id,
                'tipo_alerta': 'PROCEDIMIENTO_LARGO',
                'resuelta': False
            })
            
            if not alertas_existentes:
                await self.alerta_service.crear_alerta({
                    'tipo_alerta': 'PROCEDIMIENTO_LARGO',
                    'mensaje': f'Procedimiento {procedimiento.tipo_cirugia} lleva más de 4 horas activo',
                    'prioridad': 'MEDIA',
                    'procedimiento_id': procedimiento.procedimiento_id
                })


# Instancia global del gestor de tareas
background_manager = BackgroundTaskManager()


async def start_background_tasks():
    """
    Función para iniciar las tareas en segundo plano
    """
    await background_manager.start_background_tasks()


async def stop_background_tasks():
    """
    Función para detener las tareas en segundo plano
    """
    await background_manager.stop_background_tasks()
