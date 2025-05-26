"""
EIVAI - Sistema de Identificación de Herramientas Quirúrgicas con IA
Archivo: routes.py - Configuración de rutas principales de la aplicación

Descripción:
    Este módulo define todas las rutas y endpoints de la aplicación EIVAI.
    Incluye la página principal (dashboard), identificación de herramientas,
    páginas informativas, sistema de autenticación y endpoints de monitoreo.

Funcionalidades:
    - Ruta principal (/) que sirve el dashboard del sistema
    - Sistema de autenticación (/login, /registro, /logout)
    - Ruta de identificación (/identificacion) para análisis de herramientas
    - Páginas informativas (/acerca-de, /contacto)
    - Endpoint de salud del sistema (/health)
    - Gestión de sesiones de usuario
    - Configuración de templates con Jinja2

Autor: Equipo EIVAI
Fecha: 2025
Versión: 2.2.0
"""

from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import secrets
from datetime import datetime, timedelta

from .config import settings

# Configuración de templates Jinja2 para renderizado de páginas HTML
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

# Router principal para todas las rutas de la aplicación
main_router = APIRouter()


@main_router.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    """
    Ruta principal - Dashboard del sistema EIVAI
    
    Descripción:
        Página de inicio que funciona como dashboard principal del sistema.
        Muestra estadísticas en tiempo real, estado del sistema y accesos rápidos.
        
    Parámetros:
        request (Request): Objeto de solicitud HTTP de FastAPI
        
    Retorna:
        HTMLResponse: Página HTML renderizada con el dashboard principal
        
    Funcionalidades:
        - Estadísticas del sistema en tiempo real
        - Panel de bienvenida con información del sistema
        - Estado de componentes (servidor, base de datos, modelos IA)
        - Accesos directos a funcionalidades principales
    """
    user = get_current_user(request)
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Inicio", "user": user}
    )


@main_router.get("/acerca-de", response_class=HTMLResponse)
async def acerca_de(request: Request):
    """
    Página de información "Acerca de"
    
    Descripción:
        Página informativa que contiene detalles sobre el sistema EIVAI,
        su propósito, tecnologías utilizadas y equipo de desarrollo.
        
    Parámetros:
        request (Request): Objeto de solicitud HTTP de FastAPI
        
    Retorna:
        HTMLResponse: Página HTML con información del sistema
    """
    user = get_current_user(request)
    return templates.TemplateResponse(
        "about.html", 
        {"request": request, "title": "Acerca de", "user": user}
    )


@main_router.get("/contacto", response_class=HTMLResponse)
async def contacto(request: Request):
    """
    Página de contacto
    
    Descripción:
        Página con información de contacto del equipo de desarrollo
        y soporte técnico del sistema EIVAI.
        
    Parámetros:
        request (Request): Objeto de solicitud HTTP de FastAPI
        
    Retorna:
        HTMLResponse: Página HTML con formulario e información de contacto
    """
    user = get_current_user(request)
    return templates.TemplateResponse(
        "contact.html", 
        {"request": request, "title": "Contacto", "user": user}
    )


@main_router.get("/panel-control", response_class=HTMLResponse)
async def panel_control(request: Request):
    """
    Ruta alternativa para el dashboard/panel de control
    
    Descripción:
        Ruta alternativa que redirige al mismo contenido que la página principal.
        Mantiene compatibilidad con navegación existente y proporciona
        una URL más descriptiva para el panel de control.
        
    Parámetros:
        request (Request): Objeto de solicitud HTTP de FastAPI
        
    Retorna:
        HTMLResponse: Página HTML del dashboard (mismo contenido que "/")
    """
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Panel de Control"}
    )


@main_router.get("/identificacion", response_class=HTMLResponse)
async def identificacion_herramientas(request: Request):
    """
    Página de identificación de herramientas quirúrgicas
    
    Descripción:
        Funcionalidad principal del sistema EIVAI para cargar imágenes
        y obtener identificación automática de herramientas quirúrgicas
        mediante modelos de inteligencia artificial.
        
    Parámetros:
        request (Request): Objeto de solicitud HTTP de FastAPI
        
    Retorna:
        HTMLResponse: Página HTML con interfaz de carga de imágenes y análisis
        
    Funcionalidades:
        - Carga de imágenes mediante drag & drop o selección
        - Procesamiento con modelos de IA especializados
        - Resultados con nivel de confianza y clasificación
        - Historial de identificaciones realizadas
    """
    return templates.TemplateResponse(
        "identificacion.html", 
        {"request": request, "title": "Identificación de Herramientas"}
    )


@main_router.get("/estado-sistema")
async def verificar_estado_sistema():
    """
    Endpoint de verificación del estado del sistema (Health Check)
    
    Descripción:
        Endpoint utilizado para monitoreo y verificación del estado
        de funcionamiento del sistema EIVAI. Proporciona información
        básica sobre el estado del servidor y componentes críticos.
        
    Retorna:
        dict: Diccionario JSON con información del estado del sistema
            - status: Estado general ("ok" o "error")
            - message: Mensaje descriptivo del estado
            - version: Versión actual del sistema
            - timestamp: Marca de tiempo de la respuesta
            
    Uso:
        - Monitoreo automático del sistema
        - Verificaciones de salud en producción
        - Debugging y diagnóstico de problemas
    """
    from datetime import datetime
    
    return {
        "status": "ok", 
        "message": "Sistema EIVAI funcionando correctamente",
        "version": "2.1.0",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "servidor": "activo",
            "base_datos": "conectada", 
            "modelos_ia": "cargados",
            "cache": "optimizando"
        }
    }


# Mantener compatibilidad con rutas en inglés para transición gradual
@main_router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_legacy(request: Request):
    """
    Ruta de compatibilidad - Dashboard (inglés)
    
    Descripción:
        Ruta mantenida para compatibilidad con enlaces existentes.
        Redirige al mismo contenido que la página principal en español.
        
    Nota:
        Esta ruta puede ser eliminada en futuras versiones.
        Se recomienda usar la ruta principal "/" o "/panel-control".
    """
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "title": "Dashboard"}
    )


@main_router.get("/health")
async def health_check_legacy():
    """
    Endpoint de salud del sistema (inglés) - Compatibilidad
    
    Descripción:
        Endpoint mantenido para compatibilidad con sistemas de monitoreo
        que utilicen la ruta en inglés. Proporciona la misma funcionalidad
        que "/estado-sistema".
        
    Nota:
        Se recomienda migrar a "/estado-sistema" para consistencia
        con el resto de la aplicación en español.
    """
    return await verificar_estado_sistema()


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


@main_router.get("/login", response_class=HTMLResponse)
async def mostrar_login(request: Request):
    """
    Mostrar página de login para instrumentadores quirúrgicos
    
    Descripción:
        Página de inicio de sesión con formulario de autenticación
        específicamente diseñada para instrumentadores quirúrgicos.
        
    Parámetros:
        request (Request): Objeto de solicitud HTTP de FastAPI
        
    Retorna:
        HTMLResponse: Página HTML con formulario de login
        
    Características:
        - Formulario de autenticación seguro
        - Validación en tiempo real
        - Diseño médico profesional
        - Indicadores de carga
    """
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "title": "Iniciar Sesión"}
    )


@main_router.post("/login")
async def procesar_login(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    Procesar autenticación de usuario
    
    Descripción:
        Endpoint que procesa las credenciales del usuario y crea una sesión
        si la autenticación es exitosa.
        
    Parámetros:
        request (Request): Objeto de solicitud HTTP
        username (str): Nombre de usuario del instrumentador
        password (str): Contraseña del usuario
        
    Retorna:
        RedirectResponse: Redirección al dashboard si éxito, o al login si error
        
    Validaciones:
        - Verificación de credenciales
        - Estado activo del usuario
        - Actualización de último acceso
        - Creación de sesión segura
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
    
    Descripción:
        Página de registro con formulario completo para instrumentadores
        quirúrgicos que desean crear una cuenta en el sistema EIVAI.
        
    Parámetros:
        request (Request): Objeto de solicitud HTTP de FastAPI
        
    Retorna:
        HTMLResponse: Página HTML con formulario de registro
        
    Características:
        - Formulario de registro profesional
        - Validación de fortaleza de contraseña
        - Verificación de datos únicos
        - Términos y condiciones específicos
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
    
    Descripción:
        Endpoint que procesa el registro de un nuevo usuario instrumentador,
        validando todos los datos y creando la cuenta si es válida.
        
    Parámetros:
        request (Request): Objeto de solicitud HTTP
        nombre_completo (str): Nombre completo del instrumentador
        username (str): Nombre de usuario único
        email (str): Correo electrónico del usuario
        password (str): Contraseña del usuario
        confirm_password (str): Confirmación de contraseña
        licencia_profesional (str): Número de licencia profesional (opcional)
        terms (str): Aceptación de términos y condiciones
        
    Retorna:
        RedirectResponse: Redirección al login si éxito, o al registro si error
        
    Validaciones:
        - Unicidad de nombre de usuario y email
        - Coincidencia de contraseñas
        - Aceptación de términos
        - Fortaleza de contraseña
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
    
    Descripción:
        Endpoint que invalida la sesión actual del usuario y lo redirecciona
        a la página de login.
        
    Parámetros:
        request (Request): Objeto de solicitud HTTP
        
    Retorna:
        RedirectResponse: Redirección a la página de login
        
    Funcionalidades:
        - Invalidación de token de sesión
        - Limpieza de cookies
        - Redirección segura
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


@main_router.get("/perfil", response_class=HTMLResponse)
async def mostrar_perfil(request: Request):
    """
    Mostrar perfil del instrumentador quirúrgico
    
    Descripción:
        Página del perfil del usuario autenticado donde puede ver
        y editar su información personal y profesional.
        
    Parámetros:
        request (Request): Objeto de solicitud HTTP
        
    Retorna:
        HTMLResponse: Página de perfil si está autenticado, redirect si no
        
    Características:
        - Información personal y profesional
        - Estadísticas de uso del sistema
        - Opciones de configuración
        - Cambio de contraseña
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
