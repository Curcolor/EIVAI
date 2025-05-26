"""
Rutas principales de la aplicación
"""
from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import secrets
from datetime import datetime, timedelta

from ...config.config import settings

# Configurar templates
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

# Router principal
main_router = APIRouter()

# =============================================================================
# SISTEMA DE AUTENTICACIÓN - INSTRUMENTADOR QUIRÚRGICO
# =============================================================================

# Simulación simple de base de datos en memoria para usuarios
# En producción, esto debería conectarse a una base de datos real
users_db = {
    "admin": {
        "username": "admin",
        "nombre_completo": "Administrador Sistema",
        "email": "admin@eivai.com",
        "password_hash": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # hash de "admin"
        "activo": True,
        "fecha_registro": datetime.now(),
        "ultimo_acceso": None,
        "licencia_profesional": "ADMIN-001"
    }
}

# Sesiones activas (en producción usar Redis o similar)
active_sessions = {}


def hash_password(password: str) -> str:
    """
    Hash simple de contraseña usando SHA256
    En producción usar bcrypt o similar
    """
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """
    Verificar contraseña hasheada
    """
    return hash_password(password) == hashed


def create_session_token() -> str:
    """
    Crear token de sesión único
    """
    return secrets.token_urlsafe(32)


def get_current_user(request: Request) -> Optional[dict]:
    """
    Obtener usuario actual desde la sesión
    
    Descripción:
        Función helper que verifica si hay una sesión activa válida
        y retorna la información del usuario actual.
        
    Parámetros:
        request (Request): Objeto de solicitud HTTP
        
    Retorna:
        dict | None: Información del usuario si está autenticado, None si no
        
    Validaciones:
        - Existencia de token de sesión
        - Validez temporal de la sesión
        - Estado activo del usuario
    """
    session_token = request.cookies.get("session_token")
    
    if not session_token or session_token not in active_sessions:
        return None
    
    session = active_sessions[session_token]
    
    # Verificar si la sesión ha expirado
    if datetime.now() > session["expires"]:
        del active_sessions[session_token]
        return None
    
    # Obtener datos del usuario
    username = session["username"]
    user = users_db.get(username)
    
    if not user or not user["activo"]:
        return None
    
    return user


@main_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Página principal - Dashboard de inicio
    Requiere autenticación: redirige al login si no está autenticado
    """
    user = get_current_user(request)
    
    # Redirigir a login si no está autenticado
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Inicio", "user": user}
    )


@main_router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """
    Página acerca de
    """
    user = get_current_user(request)
    return templates.TemplateResponse(
        "about.html", 
        {"request": request, "title": "Acerca de", "user": user}
    )


@main_router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    """
    Página de contacto
    """
    user = get_current_user(request)
    return templates.TemplateResponse(
        "contact.html", 
        {"request": request, "title": "Contacto", "user": user}
    )


@main_router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Dashboard de identificación de herramientas quirúrgicas - mismo contenido que inicio
    """
    user = get_current_user(request)
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Dashboard", "user": user}
    )


@main_router.get("/identificacion", response_class=HTMLResponse)
async def identificacion(request: Request):
    """
    Página de identificación de herramientas quirúrgicas
    Requiere autenticación: redirige al login si no está autenticado
    """
    user = get_current_user(request)
    
    # Redirigir a login si no está autenticado
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse(
        "identificacion.html", 
        {"request": request, "title": "Identificación de Herramientas", "user": user}
    )


# =============================================================================
# RUTAS DE AUTENTICACIÓN
# =============================================================================

@main_router.get("/login", response_class=HTMLResponse)
async def mostrar_login(request: Request):
    """
    Mostrar página de login para instrumentadores quirúrgicos
    """
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "title": "Iniciar Sesión"}
    )


@main_router.post("/login")
async def procesar_login(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    Procesar autenticación de usuario
    """
    # Buscar usuario en la base de datos
    user = users_db.get(username)
    
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request, 
                "title": "Iniciar Sesión",
                "error": "Usuario no encontrado"
            }
        )
    
    # Verificar contraseña
    if not verify_password(password, user["password_hash"]):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request, 
                "title": "Iniciar Sesión",
                "error": "Contraseña incorrecta"
            }
        )
    
    # Verificar que el usuario esté activo
    if not user["activo"]:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request, 
                "title": "Iniciar Sesión",
                "error": "Cuenta desactivada. Contacte al administrador."
            }
        )
    
    # Crear sesión
    session_token = create_session_token()
    active_sessions[session_token] = {
        "username": username,
        "login_time": datetime.now(),
        "expires": datetime.now() + timedelta(hours=8)  # Sesión de 8 horas
    }
    
    # Actualizar último acceso
    users_db[username]["ultimo_acceso"] = datetime.now()
    
    # Crear respuesta de redirección con cookie de sesión
    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(
        key="session_token",
        value=session_token,
        max_age=8 * 60 * 60,  # 8 horas en segundos
        httponly=True,
        secure=False  # En producción debería ser True con HTTPS
    )
    
    return response


@main_router.get("/registro", response_class=HTMLResponse)
async def mostrar_registro(request: Request):
    """
    Mostrar página de registro para nuevos instrumentadores quirúrgicos
    """
    return templates.TemplateResponse(
        "registro.html", 
        {"request": request, "title": "Registro"}
    )


@main_router.post("/registro")
async def procesar_registro(
    request: Request,
    nombre_completo: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    licencia_profesional: str = Form(""),
    terms: str = Form(None)
):
    """
    Procesar registro de nuevo instrumentador quirúrgico
    """
    errors = []
    
    # Validar que las contraseñas coincidan
    if password != confirm_password:
        errors.append("Las contraseñas no coinciden")
    
    # Validar fortaleza de contraseña
    if len(password) < 8:
        errors.append("La contraseña debe tener al menos 8 caracteres")
    
    # Validar términos aceptados
    if not terms:
        errors.append("Debe aceptar los términos y condiciones")
    
    # Verificar que el username no exista
    if username in users_db:
        errors.append("El nombre de usuario ya existe")
    
    # Verificar que el email no exista
    for user in users_db.values():
        if user["email"] == email:
            errors.append("El correo electrónico ya está registrado")
            break
    
    # Si hay errores, mostrar el formulario con los errores
    if errors:
        return templates.TemplateResponse(
            "registro.html",
            {
                "request": request,
                "title": "Registro",
                "errors": errors,
                "form_data": {
                    "nombre_completo": nombre_completo,
                    "username": username,
                    "email": email,
                    "licencia_profesional": licencia_profesional
                }
            }
        )
    
    # Crear nuevo usuario
    users_db[username] = {
        "username": username,
        "nombre_completo": nombre_completo,
        "email": email,
        "password_hash": hash_password(password),
        "activo": True,
        "fecha_registro": datetime.now(),
        "ultimo_acceso": None,
        "licencia_profesional": licencia_profesional or ""
    }
    
    # Redireccionar al login con mensaje de éxito
    response = RedirectResponse(url="/login", status_code=302)
    return response


@main_router.get("/logout")
async def logout(request: Request):
    """
    Cerrar sesión del usuario
    """
    # Obtener token de sesión de las cookies
    session_token = request.cookies.get("session_token")
    
    # Invalidar sesión si existe
    if session_token and session_token in active_sessions:
        del active_sessions[session_token]
    
    # Crear respuesta de redirección y limpiar cookie
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key="session_token")
    
    return response


@main_router.get("/perfil", response_class=HTMLResponse)
async def mostrar_perfil(request: Request):
    """
    Mostrar perfil del instrumentador quirúrgico
    """
    user = get_current_user(request)
    
    if not user:
        return RedirectResponse(url="/login", status_code=302)
    
    return templates.TemplateResponse(
        "perfil.html",
        {
            "request": request,
            "title": "Mi Perfil",
            "user": user
        }
    )


@main_router.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    """
    Página de chat de soporte simulada
    """
    user = get_current_user(request) if 'get_current_user' in globals() else None
    return templates.TemplateResponse(
        "chat.html",
        {"request": request, "title": "Chat", "user": user}
    )


@main_router.get("/health")
async def health_check():
    """
    Endpoint de health check
    """
    return {"status": "ok", "message": "Servidor funcionando correctamente"}
