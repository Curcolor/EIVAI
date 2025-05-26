# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\api\middlewares\auth_middleware.py
"""
Middleware de autenticación para el sistema EIVAI
"""
from functools import wraps
from flask import request, jsonify, g, session
from src.services.usuario_service import UsuarioService

def token_required(f):
    """
    Decorator para validar token de sesión en rutas protegidas
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si hay sesión activa
        if 'user_id' not in session:
            return jsonify({
                'success': False,
                'message': 'Token de autenticación requerido',
                'error': 'AUTHENTICATION_REQUIRED'
            }), 401
        
        try:
            # Obtener información del usuario de la sesión
            usuario_service = UsuarioService()
            usuario = usuario_service.get_by_id(session['user_id'])
            
            if not usuario:
                session.clear()
                return jsonify({
                    'success': False,
                    'message': 'Usuario no encontrado',
                    'error': 'USER_NOT_FOUND'
                }), 401
            
            if not usuario.activo:
                session.clear()
                return jsonify({
                    'success': False,
                    'message': 'Usuario inactivo',
                    'error': 'USER_INACTIVE'
                }), 401
            
            # Almacenar usuario en contexto global de Flask
            g.current_user = usuario
            
        except Exception as e:
            session.clear()
            return jsonify({
                'success': False,
                'message': 'Error al validar autenticación',
                'error': str(e)
            }), 500
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator para rutas que requieren permisos de administrador
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'current_user') or not g.current_user:
            return jsonify({
                'success': False,
                'message': 'Autenticación requerida',
                'error': 'AUTHENTICATION_REQUIRED'
            }), 401
        
        if g.current_user.rol != 'Administrador':
            return jsonify({
                'success': False,
                'message': 'Se requieren permisos de administrador',
                'error': 'ADMIN_REQUIRED'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def cors_middleware():
    """
    Middleware para manejar CORS
    """
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    return after_request

def session_middleware():
    """
    Middleware para inicializar datos de sesión
    """
    def before_request():
        # Actualizar última actividad de usuario si está logueado
        if 'user_id' in session:
            try:
                usuario_service = UsuarioService()
                usuario_service.update_last_activity(session['user_id'])
            except Exception:
                # Si hay error, limpiar sesión
                session.clear()
    
    return before_request
