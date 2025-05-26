import os
import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from ..config.settings import settings
from .routes.yolo_routes import router as yolo_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    logger.info("Iniciando microservicio YOLO Detection...")
    
    # Crear directorios necesarios
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    logger.info(f"Directorio de uploads: {settings.UPLOAD_DIR}")
    logger.info(f"Modelo YOLO: {settings.YOLO_MODEL_PATH}")
    logger.info("Microservicio YOLO Detection iniciado correctamente")
    
    yield
    
    # Shutdown
    logger.info("Cerrando microservicio YOLO Detection...")

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para loggear requests"""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    # Procesar request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.4f}s")
    
    return response

# Incluir routers
app.include_router(yolo_router)

# Rutas básicas
@app.get("/", tags=["Root"])
async def read_root():
    """Endpoint raíz del microservicio"""
    return {
        "message": f"Bienvenido a {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "docs": "/docs",
        "health": "/api/v1/yolo/health"
    }

@app.get("/status", tags=["Root"])
async def get_status():
    """Obtener estado básico del microservicio"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "model": settings.YOLO_MODEL_PATH,
        "upload_dir": settings.UPLOAD_DIR
    }

# Manejador de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Manejador global de excepciones"""
    logger.error(f"Error no manejado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "message": "Ocurrió un error inesperado",
            "detail": str(exc) if settings.DEBUG else None
        }
    )

# Configurar OpenAPI personalizado
def custom_openapi():
    """Configuración personalizada de OpenAPI"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=f"""
        {settings.APP_DESCRIPTION}
        
        ## Funcionalidades
        
        - **Detección de instrumentos**: Detecta y cuenta instrumentos quirúrgicos en imágenes
        - **Múltiples formatos**: Soporta JPG, PNG, BMP, TIFF, WEBP
        - **Configuración flexible**: Umbrales de confianza e IoU ajustables
        - **Respuesta detallada**: Coordenadas, confianza y resumen por tipo
        
        ## Instrumentos soportados
        
        - Bisturí #11 y #15
        - Pinzas Kelly y Allis
        - Tijeras Mayo y Metzenbaum
        - Portaagujas
        - Separador Farabeuf
        - Aspirador quirúrgico
        - Gasas estériles
        
        ## Uso típico
        
        1. Subir imagen a `/api/v1/yolo/detect`
        2. Recibir detecciones con coordenadas y confianza
        3. Obtener resumen con cantidad por tipo de instrumento
        """,
        routes=app.routes,
    )
    
    # Agregar información adicional
    openapi_schema["info"]["contact"] = {
        "name": "Equipo de Desarrollo EIVAI",
        "email": "desarrollo@eivai.com"
    }
    openapi_schema["info"]["license"] = {
        "name": "MIT",
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
