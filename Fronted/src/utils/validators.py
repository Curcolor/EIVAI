"""
Utilidades de validación para el sistema EIVAI
"""
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, ValidationError
import re


def validate_request_data(data: Dict[str, Any], required_fields: List[str]) -> tuple:
    """
    Validar datos de solicitud
    
    Args:
        data: Diccionario con los datos a validar
        required_fields: Lista de campos requeridos
        
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    if not isinstance(data, dict):
        return False, "Los datos deben ser un diccionario"
    
    # Verificar campos requeridos
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Campos requeridos faltantes: {', '.join(missing_fields)}"
    
    return True, ""


def validate_email(email: str) -> bool:
    """
    Validar formato de email
    """
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple:
    """
    Validar contraseña
    
    Returns:
        tuple: (es_válida, mensaje_error)
    """
    if not password:
        return False, "La contraseña es requerida"
    
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"
    
    if len(password) > 100:
        return False, "La contraseña no puede tener más de 100 caracteres"
    
    return True, ""


def validate_username(username: str) -> tuple:
    """
    Validar nombre de usuario
    
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    if not username:
        return False, "El nombre de usuario es requerido"
    
    if len(username) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres"
    
    if len(username) > 50:
        return False, "El nombre de usuario no puede tener más de 50 caracteres"
    
    # Solo caracteres alfanuméricos y guiones bajos
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "El nombre de usuario solo puede contener letras, números y guiones bajos"
    
    return True, ""


def validate_instrumento_data(data: Dict[str, Any]) -> tuple:
    """
    Validar datos de instrumento
    
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    required_fields = ["nombre", "categoria_id"]
    is_valid, error_msg = validate_request_data(data, required_fields)
    
    if not is_valid:
        return False, error_msg
    
    # Validar nombre
    nombre = data.get("nombre", "").strip()
    if len(nombre) < 2:
        return False, "El nombre del instrumento debe tener al menos 2 caracteres"
    
    if len(nombre) > 100:
        return False, "El nombre del instrumento no puede tener más de 100 caracteres"
    
    return True, ""


def validate_conteo_data(data: Dict[str, Any]) -> tuple:
    """
    Validar datos de conteo
    
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    required_fields = ["instrumento_id", "cantidad_inicial"]
    is_valid, error_msg = validate_request_data(data, required_fields)
    
    if not is_valid:
        return False, error_msg
    
    # Validar cantidad inicial
    try:
        cantidad = int(data.get("cantidad_inicial", 0))
        if cantidad < 0:
            return False, "La cantidad inicial no puede ser negativa"
    except (ValueError, TypeError):
        return False, "La cantidad inicial debe ser un número entero"
    
    return True, ""


def validate_alerta_data(data: Dict[str, Any]) -> tuple:
    """
    Validar datos de alerta
    
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    required_fields = ["titulo", "tipo_alerta", "prioridad"]
    is_valid, error_msg = validate_request_data(data, required_fields)
    
    if not is_valid:
        return False, error_msg
    
    # Validar prioridad
    prioridades_validas = ["baja", "media", "alta", "critica"]
    prioridad = data.get("prioridad", "").lower()
    if prioridad not in prioridades_validas:
        return False, f"Prioridad debe ser una de: {', '.join(prioridades_validas)}"
    
    return True, ""


def validate_pydantic_model(model_class: BaseModel, data: Dict[str, Any]) -> tuple:
    """
    Validar datos usando un modelo Pydantic
    
    Args:
        model_class: Clase del modelo Pydantic
        data: Datos a validar
        
    Returns:
        tuple: (modelo_válido_o_None, lista_errores)
    """
    try:
        validated_model = model_class(**data)
        return validated_model, []
    except ValidationError as e:
        errors = []
        for error in e.errors():
            field = ".".join(str(x) for x in error["loc"])
            errors.append(f"{field}: {error['msg']}")
        return None, errors


def sanitize_input(input_str: str) -> str:
    """
    Sanitizar entrada de texto
    """
    if not isinstance(input_str, str):
        return ""
    
    # Remover caracteres peligrosos para prevenir inyecciones
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`']
    sanitized = input_str
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()


def validate_id(id_value: Any, field_name: str = "ID") -> tuple:
    """
    Validar que un ID sea válido
    
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    try:
        id_int = int(id_value)
        if id_int <= 0:
            return False, f"{field_name} debe ser un número positivo"
        return True, ""
    except (ValueError, TypeError):
        return False, f"{field_name} debe ser un número entero válido"


def validate_pagination_params(skip: Any, limit: Any) -> tuple:
    """
    Validar parámetros de paginación
    
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    try:
        skip_int = int(skip) if skip is not None else 0
        limit_int = int(limit) if limit is not None else 100
        
        if skip_int < 0:
            return False, "skip debe ser mayor o igual a 0"
        
        if limit_int <= 0:
            return False, "limit debe ser mayor a 0"
        
        if limit_int > 1000:
            return False, "limit no puede ser mayor a 1000"
        
        return True, ""
    except (ValueError, TypeError):
        return False, "skip y limit deben ser números enteros válidos"
