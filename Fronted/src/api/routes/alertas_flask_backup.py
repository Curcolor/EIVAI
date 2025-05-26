# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\api\routes\alertas.py
"""
Rutas API para gestión de alertas del sistema
"""
from flask import Blueprint
from src.api.controllers.alerta_controller import AlertaController
from src.api.middlewares import token_required, admin_required

# Crear blueprint para rutas de alertas
alertas_bp = Blueprint('alertas', __name__, url_prefix='/api/alertas')

# Inicializar controlador
alerta_controller = AlertaController()

@alertas_bp.route('', methods=['POST'])
@token_required
@admin_required
def crear_alerta():
    """
    Crear una nueva alerta manualmente
    ---
    tags:
      - Alertas
    security:
      - ApiKeyAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - tipo_alerta
              - mensaje
            properties:
              tipo_alerta:
                type: string
                description: Tipo de alerta
              mensaje:
                type: string
                description: Mensaje de la alerta
              prioridad:
                type: string
                enum: [Alta, Media, Baja]
                default: Media
                description: Prioridad de la alerta
              instrumento_id:
                type: integer
                description: ID del instrumento relacionado (opcional)
              procedimiento_id:
                type: integer
                description: ID del procedimiento relacionado (opcional)
    responses:
      201:
        description: Alerta creada exitosamente
      400:
        description: Datos inválidos
      401:
        description: No autorizado
      403:
        description: Permisos insuficientes
    """
    return alerta_controller.crear_alerta()

@alertas_bp.route('/activas', methods=['GET'])
@token_required
def obtener_alertas_activas():
    """
    Obtener todas las alertas activas
    ---
    tags:
      - Alertas
    security:
      - ApiKeyAuth: []
    parameters:
      - in: query
        name: limit
        schema:
          type: integer
          default: 50
        description: Límite de resultados
    responses:
      200:
        description: Lista de alertas activas
      401:
        description: No autorizado
    """
    return alerta_controller.obtener_alertas_activas()

@alertas_bp.route('/tipo/<string:tipo_alerta>', methods=['GET'])
@token_required
def obtener_alertas_por_tipo(tipo_alerta):
    """
    Obtener alertas por tipo específico
    ---
    tags:
      - Alertas
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: tipo_alerta
        required: true
        schema:
          type: string
        description: Tipo de alerta
    responses:
      200:
        description: Lista de alertas del tipo especificado
      401:
        description: No autorizado
    """
    return alerta_controller.obtener_alertas_por_tipo(tipo_alerta)

@alertas_bp.route('/<int:alerta_id>', methods=['GET'])
@token_required
def obtener_alerta(alerta_id):
    """
    Obtener información detallada de una alerta
    ---
    tags:
      - Alertas
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: alerta_id
        required: true
        schema:
          type: integer
        description: ID de la alerta
    responses:
      200:
        description: Información detallada de la alerta
      404:
        description: Alerta no encontrada
      401:
        description: No autorizado
    """
    return alerta_controller.obtener_alerta(alerta_id)

@alertas_bp.route('/<int:alerta_id>/resolver', methods=['PUT'])
@token_required
def resolver_alerta(alerta_id):
    """
    Marcar una alerta como resuelta
    ---
    tags:
      - Alertas
    security:
      - ApiKeyAuth: []
    parameters:
      - in: path
        name: alerta_id
        required: true
        schema:
          type: integer
        description: ID de la alerta
    requestBody:
      content:
        application/json:
          schema:
            type: object
            properties:
              resolucion:
                type: string
                description: Descripción de la resolución
    responses:
      200:
        description: Alerta resuelta exitosamente
      404:
        description: Alerta no encontrada
      401:
        description: No autorizado
    """
    return alerta_controller.resolver_alerta(alerta_id)

@alertas_bp.route('/verificaciones/ejecutar', methods=['POST'])
@token_required
@admin_required
def ejecutar_verificaciones():
    """
    Ejecutar verificaciones automáticas de alertas
    ---
    tags:
      - Alertas
    security:
      - ApiKeyAuth: []
    responses:
      200:
        description: Verificaciones ejecutadas exitosamente
      401:
        description: No autorizado
      403:
        description: Permisos insuficientes
    """
    return alerta_controller.ejecutar_verificaciones()

@alertas_bp.route('/estadisticas', methods=['GET'])
@token_required
def obtener_estadisticas_alertas():
    """
    Obtener estadísticas de alertas
    ---
    tags:
      - Alertas
    security:
      - ApiKeyAuth: []
    parameters:
      - in: query
        name: fecha_inicio
        schema:
          type: string
          format: date-time
        description: Fecha de inicio para las estadísticas
      - in: query
        name: fecha_fin
        schema:
          type: string
          format: date-time
        description: Fecha de fin para las estadísticas
    responses:
      200:
        description: Estadísticas de alertas
      401:
        description: No autorizado
    """
    return alerta_controller.obtener_estadisticas_alertas()

@alertas_bp.route('/resumen', methods=['GET'])
@token_required
def obtener_resumen_alertas():
    """
    Obtener resumen rápido de alertas para dashboard
    ---
    tags:
      - Alertas
    security:
      - ApiKeyAuth: []
    responses:
      200:
        description: Resumen de alertas
      401:
        description: No autorizado
    """
    return alerta_controller.obtener_resumen_alertas()
