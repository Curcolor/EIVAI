# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\api\routes\__init__.py
"""
Módulo de rutas de la API
"""

from .usuarios import router as usuarios_router
from .instrumentos import router as instrumentos_router
from .procedimientos import router as procedimientos_router
from .conteos import router as conteos_router
from .alertas import router as alertas_router
from .sets import router as sets_router
from .dashboard import router as dashboard_router
from .routes import main_router

__all__ = [
    'usuarios_router',
    'instrumentos_router', 
    'procedimientos_router',
    'conteos_router',
    'alertas_router',
    'sets_router',
    'dashboard_router',
    'main_router'
]