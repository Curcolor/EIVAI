"""
Rutas principales de la aplicación
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ...config.config import settings

# Configurar templates
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

# Router principal
main_router = APIRouter()


@main_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Página principal
    """
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Inicio"}
    )


@main_router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """
    Página acerca de
    """
    return templates.TemplateResponse(
        "about.html", 
        {"request": request, "title": "Acerca de"}
    )


@main_router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    """
    Página de contacto
    """
    return templates.TemplateResponse(
        "contact.html", 
        {"request": request, "title": "Contacto"}
    )


@main_router.get("/health")
async def health_check():
    """
    Endpoint de health check
    """
    return {"status": "ok", "message": "Servidor funcionando correctamente"}
