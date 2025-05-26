"""
Configuración de la aplicación FastAPI
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from ..config.config import settings
from .routes.routes import main_router
from .routes.usuarios import router as usuarios_router
from .routes.instrumentos import router as instrumentos_router
from .routes.procedimientos import router as procedimientos_router
from .routes.conteos import router as conteos_router
from .routes.alertas import router as alertas_router
from .routes.sets import router as sets_router
from .routes.dashboard import router as dashboard_router
from .routes.test_routes import test_router  # Habilitado para pruebas
# from .middlewares.auth_middleware import AuthMiddleware  # Ya no es necesario


def create_app() -> FastAPI:
    """
    Crear y configurar la aplicación FastAPI
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        debug=settings.DEBUG    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # El middleware de autenticación ahora se maneja como dependencias en las rutas    
    # Montar archivos estáticos
    app.mount("/static", StaticFiles(directory="src/static"), name="static")
    
    # Incluir rutas principales (templates)
    app.include_router(main_router)
    
    # Incluir rutas API
    app.include_router(usuarios_router)
    app.include_router(instrumentos_router)
    app.include_router(procedimientos_router)
    app.include_router(conteos_router)
    app.include_router(alertas_router)
    app.include_router(sets_router)
    app.include_router(dashboard_router)
    app.include_router(test_router)  # Habilitado para pruebas
    
    return app


# Crear la instancia de la aplicación
app = create_app()
