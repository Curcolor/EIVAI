"""
Utilidades generales para la aplicación.
"""
import logging
from typing import Dict, Any

logger = logging.getLogger("deepseek_api")

def format_error_response(error_message: str, status_code: int, detail: str = None) -> Dict[str, Any]:
    """
    Formatea una respuesta de error de manera consistente.
    
    Args:
        error_message: Mensaje principal de error
        status_code: Código HTTP de error
        detail: Detalle opcional del error
        
    Returns:
        Diccionario con la estructura de error estandarizada
    """
    response = {
        "error": error_message,
        "codigo": status_code
    }
    
    if detail:
        response["detalle"] = detail
        
    return response
