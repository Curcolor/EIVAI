"""
Controlador para la API de DeepSeek.
"""
import time
import logging
from typing import Dict, Any, Optional

from src.services.deepseek_service import DeepSeekService, DeepSeekException
from src.config.settings import get_settings

settings = get_settings()
logger = logging.getLogger("deepseek_api")

class DeepSeekController:
    """
    Controlador para las operaciones de procesamiento de texto con DeepSeek.
    
    Actúa como intermediario entre las rutas de la API y el servicio DeepSeek,
    gestionando la lógica de negocio y el manejo de errores.
    """
    
    @staticmethod
    def verificar_estado() -> Dict[str, Any]:
        """
        Verifica el estado del servicio.
        
        Returns:
            Diccionario con información del estado del servicio
        """
        return {
            'estado': 'operativo',
            'mensaje': 'El servicio de procesamiento de texto con DeepSeek está funcionando correctamente',
            'modelo_predeterminado': settings.DEEPSEEK_MODELO,
            'timestamp': time.time()
        }
    
    @staticmethod
    def procesar_texto(
        texto: str, 
        temperatura: Optional[float] = settings.TEMPERATURA_PREDETERMINADA, 
        max_tokens: Optional[int] = settings.MAX_TOKENS_PREDETERMINADO, 
        modelo: Optional[str] = settings.DEEPSEEK_MODELO
    ) -> Dict[str, Any]:
        """
        Procesa texto utilizando la API de DeepSeek.
        
        Args:
            texto: Texto a procesar
            temperatura: Nivel de aleatoriedad (0.0 a 1.0)
            max_tokens: Número máximo de tokens a generar
            modelo: Modelo de DeepSeek a utilizar
            
        Returns:
            Diccionario con la respuesta procesada
            
        Raises:
            DeepSeekException: Si ocurre un error en la API
        """
        try:
            # Crear instancia del servicio
            servicio = DeepSeekService()
            
            # Procesar texto
            resultado = servicio.procesar_texto(
                texto=texto,
                temperatura=temperatura,
                max_tokens=max_tokens,
                modelo=modelo
            )
            
            return resultado
        except DeepSeekException as e:
            logger.error(f"Error en el procesamiento de texto: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error inesperado en el controlador: {str(e)}")
            raise DeepSeekException(f"Error interno del servidor: {str(e)}")
