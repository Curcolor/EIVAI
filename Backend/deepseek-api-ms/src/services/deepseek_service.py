"""
Servicio para interactuar con la API de DeepSeek.
"""
import requests
import logging
import time
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from src.config.settings import get_settings

settings = get_settings()
logger = logging.getLogger("deepseek_api")

class DeepSeekException(Exception):
    """Excepción personalizada para errores del servicio DeepSeek."""
    pass

class DeepSeekService:
    """
    Servicio para interactuar con la API de DeepSeek.
    
    Proporciona métodos para procesar texto utilizando los modelos de DeepSeek
    con manejo de errores y reintentos automáticos.
    """
    
    def __init__(self):
        """Inicializa el servicio con la configuración de la API."""
        self.api_url = settings.DEEPSEEK_API_URL
        self.api_key = settings.DEEPSEEK_API_KEY
        self.default_model = settings.DEEPSEEK_MODELO
        self.default_temperature = settings.TEMPERATURA_PREDETERMINADA
        self.default_max_tokens = settings.MAX_TOKENS_PREDETERMINADO
        self.timeout = settings.REQUEST_TIMEOUT
    
    @retry(
        retry=retry_if_exception_type((requests.exceptions.ConnectionError, requests.exceptions.Timeout)),
        stop=stop_after_attempt(settings.MAX_REINTENTOS),
        wait=wait_fixed(settings.TIEMPO_ENTRE_REINTENTOS),
        reraise=True
    )
    def procesar_texto(
        self, 
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
        # Usar valores por defecto si no se proporcionan
        temperatura_final = temperatura if temperatura is not None else self.default_temperature
        max_tokens_final = max_tokens if max_tokens is not None else self.default_max_tokens
        modelo_final = modelo if modelo is not None else self.default_model
        
        # Registrar inicio de la solicitud
        inicio = time.time()
        logger.info(f"Procesando texto con modelo {modelo_final}, temperatura {temperatura_final}")
        
        try:
            # Preparar la solicitud a DeepSeek
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": modelo_final,
                "messages": [{"role": "user", "content": texto}],
                "temperature": temperatura_final,
                "max_tokens": max_tokens_final
            }
            
            # Realizar la solicitud a la API
            response = requests.post(
                f"{self.api_url}/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            
            # Verificar respuesta
            if response.status_code != 200:
                error_detail = response.json() if response.content else "Sin detalles"
                logger.error(f"Error en la API de DeepSeek: {response.status_code} - {error_detail}")
                raise DeepSeekException(f"Error en la API de DeepSeek: {response.status_code}")
            
            # Procesar respuesta
            respuesta_json = response.json()
            texto_procesado = respuesta_json["choices"][0]["message"]["content"]
            tokens_entrada = respuesta_json["usage"]["prompt_tokens"]
            tokens_salida = respuesta_json["usage"]["completion_tokens"]
            
            # Calcular tiempo de proceso
            tiempo_proceso = time.time() - inicio
            
            # Registrar éxito
            logger.info(f"Texto procesado exitosamente en {tiempo_proceso:.2f}s - Tokens E/S: {tokens_entrada}/{tokens_salida}")
            
            return {
                "texto_procesado": texto_procesado,
                "modelo_usado": modelo_final,
                "tokens_entrada": tokens_entrada,
                "tokens_salida": tokens_salida,
                "tiempo_proceso": tiempo_proceso
            }
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Error de conexión con la API de DeepSeek: {str(e)}")
            raise DeepSeekException(f"Error de conexión con la API de DeepSeek: {str(e)}")
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout en la conexión con la API de DeepSeek: {str(e)}")
            raise DeepSeekException(f"Timeout en la conexión con la API de DeepSeek")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en la solicitud a la API de DeepSeek: {str(e)}")
            raise DeepSeekException(f"Error en la solicitud a la API de DeepSeek: {str(e)}")
        except Exception as e:
            logger.error(f"Error inesperado al procesar texto: {str(e)}")
            raise DeepSeekException(f"Error inesperado al procesar texto: {str(e)}")
