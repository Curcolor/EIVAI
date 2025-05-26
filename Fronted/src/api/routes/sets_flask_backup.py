# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\api\routes\sets.py
"""
Rutas API para gestión de sets quirúrgicos
"""
from flask import Blueprint
from src.api.controllers.set_controller import SetController
from src.api.middlewares import token_required, admin_required

# Crear blueprint para rutas de sets
sets_bp = Blueprint('sets', __name__, url_prefix='/api/sets')

# Inicializar controlador
set_controller = SetController()

@sets_bp.route('', methods=['POST'])
@token_required
@admin_required
def crear_set():
    """
    Crear un nuevo set quirúrgico
    ---
    tags:
      - Sets Quirúrgicos
    security:
      - ApiKeyAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - nombre
            properties:
              nombre:
                type: string
                description: Nombre del set quirúrgico
              descripcion:
                type: string
                description: Descripción del set
              especialidad:
                type: string
                description: Especialidad médica
              activo:
                type: boolean
                default: true
                description: Estado activo del set
    responses:
      201:
        description: Set quirúrgico creado exitosamente
      400:
        description: Datos inválidos
      401:
        description: No autorizado
      403:
        description: Permisos insuficientes
    """
    return set_controller.crear_set()

@sets_bp.route('', methods=['GET'])
@token_required
def obtener_sets_activos():
    """
    Obtener todos los sets quirúrgicos activos
    ---
    tags:
      - Sets Quirúrgicos
    security:
      - ApiKeyAuth: []
    responses:
      200:
        description: Lista de sets quirúrgicos activos
      401:
        description: No autorizado
    """
    return set_controller.obtener_sets_activos()

@sets_bp.route('/<int:set_id>', methods=['GET'])
@token_required
def obtener_set(set_id):
    """
    Obtener información de un set específico con sus instrumentos
    ---
    tags:
      - Sets Quirúrgicos
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: set_id
        required: true
        schema:
          type: integer
        description: ID del set quirúrgico
    responses:
      200:
        description: Información detallada del set
      404:
        description: Set no encontrado
      401:
        description: No autorizado
    """
    return set_controller.obtener_set(set_id)

@sets_bp.route('/<int:set_id>', methods=['PUT'])
@token_required
@admin_required
def actualizar_set(set_id):
    """
    Actualizar información de un set quirúrgico
    ---
    tags:
      - Sets Quirúrgicos
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: set_id
        required: true
        schema:
          type: integer
        description: ID del set quirúrgico
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              nombre:
                type: string
                description: Nombre del set
              descripcion:
                type: string
                description: Descripción del set
              especialidad:
                type: string
                description: Especialidad médica
              activo:
                type: boolean
                description: Estado activo del set
    responses:
      200:
        description: Set actualizado exitosamente
      404:
        description: Set no encontrado
      401:
        description: No autorizado
      403:
        description: Permisos insuficientes
    """
    return set_controller.actualizar_set(set_id)

@sets_bp.route('/<int:set_id>/instrumentos', methods=['POST'])
@token_required
@admin_required
def agregar_instrumento(set_id):
    """
    Agregar un instrumento a un set quirúrgico
    ---
    tags:
      - Sets Quirúrgicos
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: set_id
        required: true
        schema:
          type: integer
        description: ID del set quirúrgico
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - instrumento_id
            properties:
              instrumento_id:
                type: integer
                description: ID del instrumento
              cantidad:
                type: integer
                default: 1
                description: Cantidad del instrumento en el set
              obligatorio:
                type: boolean
                default: true
                description: Si el instrumento es obligatorio
    responses:
      201:
        description: Instrumento agregado al set exitosamente
      400:
        description: Datos inválidos
      401:
        description: No autorizado
      403:
        description: Permisos insuficientes
    """
    return set_controller.agregar_instrumento(set_id)

@sets_bp.route('/<int:set_id>/instrumentos/<int:instrumento_id>', methods=['DELETE'])
@token_required
@admin_required
def remover_instrumento(set_id, instrumento_id):
    """
    Remover un instrumento de un set quirúrgico
    ---
    tags:
      - Sets Quirúrgicos
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: set_id
        required: true
        schema:
          type: integer
        description: ID del set quirúrgico
      - in: path
        name: instrumento_id
        required: true
        schema:
          type: integer
        description: ID del instrumento
    responses:
      200:
        description: Instrumento removido del set exitosamente
      404:
        description: Instrumento no encontrado en el set
      401:
        description: No autorizado
      403:
        description: Permisos insuficientes
    """
    return set_controller.remover_instrumento(set_id, instrumento_id)

@sets_bp.route('/especialidad/<string:especialidad>', methods=['GET'])
@token_required
def obtener_sets_por_especialidad(especialidad):
    """
    Obtener sets quirúrgicos por especialidad
    ---
    tags:
      - Sets Quirúrgicos
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: especialidad
        required: true
        schema:
          type: string
        description: Especialidad médica
    responses:
      200:
        description: Lista de sets de la especialidad
      401:
        description: No autorizado
    """
    return set_controller.obtener_sets_por_especialidad(especialidad)

@sets_bp.route('/<int:set_id>/disponibilidad', methods=['GET'])
@token_required
def verificar_disponibilidad(set_id):
    """
    Verificar disponibilidad de todos los instrumentos de un set
    ---
    tags:
      - Sets Quirúrgicos
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: set_id
        required: true
        schema:
          type: integer
        description: ID del set quirúrgico
    responses:
      200:
        description: Estado de disponibilidad del set
      401:
        description: No autorizado
    """
    return set_controller.verificar_disponibilidad(set_id)

@sets_bp.route('/<int:set_id>/duplicar', methods=['POST'])
@token_required
@admin_required
def duplicar_set(set_id):
    """
    Duplicar un set quirúrgico existente
    ---
    tags:
      - Sets Quirúrgicos
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: set_id
        required: true
        schema:
          type: integer
        description: ID del set a duplicar
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - nuevo_nombre
            properties:
              nuevo_nombre:
                type: string
                description: Nombre para el nuevo set
    responses:
      201:
        description: Set duplicado exitosamente
      404:
        description: Set original no encontrado
      401:
        description: No autorizado
      403:
        description: Permisos insuficientes
    """
    return set_controller.duplicar_set(set_id)

@sets_bp.route('/buscar', methods=['GET'])
@token_required
def buscar_sets():
    """
    Buscar sets quirúrgicos con filtros
    ---
    tags:
      - Sets Quirúrgicos
    security:
      - ApiKeyAuth: []
    parameters:
      - in: query
        name: termino
        schema:
          type: string
        description: Término de búsqueda
      - in: query
        name: especialidad
        schema:
          type: string
        description: Filtrar por especialidad
      - in: query
        name: activo
        schema:
          type: boolean
        description: Filtrar por estado activo
    responses:
      200:
        description: Lista de sets que coinciden con los filtros
      401:
        description: No autorizado
    """
    return set_controller.buscar_sets()

@sets_bp.route('/estadisticas', methods=['GET'])
@token_required
def obtener_estadisticas_sets():
    """
    Obtener estadísticas de sets quirúrgicos
    ---
    tags:
      - Sets Quirúrgicos
    security:
      - ApiKeyAuth: []
    responses:
      200:
        description: Estadísticas de sets quirúrgicos
      401:
        description: No autorizado
    """
    return set_controller.obtener_estadisticas_sets()
