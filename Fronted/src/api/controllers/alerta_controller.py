# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\api\controllers\alerta_controller.py
"""
Controlador para gestión de alertas del sistema
"""
from typing import Dict, Any, List
from datetime import datetime
from typing import List, Optional, Any, Dict
from src.services.alerta_service import AlertaService
from src.api.schemas import AlertaCreateSchema

class AlertaController:
    """
    Controlador para operaciones de alertas del sistema
    """
    
    def __init__(self):
        self.alerta_service = AlertaService()
    
    def crear_alerta(self) -> tuple:
        """
        Crear una nueva alerta manualmente
        """
        try:
            data = request.json
            
            # Validaciones básicas
            if not data.get('tipo_alerta') or not data.get('mensaje'):
                return jsonify({
                    'success': False,
                    'message': 'Tipo de alerta y mensaje son requeridos'
                }), 400
            
            alerta = self.alerta_service.crear_alerta(
                tipo_alerta=data['tipo_alerta'],
                mensaje=data['mensaje'],
                prioridad=data.get('prioridad', 'Media'),
                instrumento_id=data.get('instrumento_id'),
                procedimiento_id=data.get('procedimiento_id')
            )
            
            return jsonify({
                'success': True,
                'message': 'Alerta creada exitosamente',
                'data': {
                    'alerta_id': alerta.alerta_id,
                    'tipo_alerta': alerta.tipo_alerta,
                    'mensaje': alerta.mensaje,
                    'prioridad': alerta.prioridad,
                    'fecha_creacion': alerta.fecha_creacion.isoformat()
                }
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def obtener_alertas_activas(self) -> tuple:
        """
        Obtener todas las alertas activas
        """
        try:
            limit = int(request.args.get('limit', 50))
            alertas = self.alerta_service.obtener_alertas_activas(limit)
            
            return jsonify({
                'success': True,
                'data': [
                    {
                        'alerta_id': alerta.alerta_id,
                        'tipo_alerta': alerta.tipo_alerta,
                        'mensaje': alerta.mensaje,
                        'prioridad': alerta.prioridad,
                        'fecha_creacion': alerta.fecha_creacion.isoformat() if alerta.fecha_creacion else None,
                        'instrumento': {
                            'id': alerta.instrumento.instrumento_id,
                            'nombre': alerta.instrumento.nombre
                        } if alerta.instrumento else None,
                        'procedimiento': {
                            'id': alerta.procedimiento.procedimiento_id,
                            'nombre': alerta.procedimiento.nombre
                        } if alerta.procedimiento else None
                    }
                    for alerta in alertas
                ],
                'total': len(alertas)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def obtener_alertas_por_tipo(self, tipo_alerta: str) -> tuple:
        """
        Obtener alertas por tipo específico
        """
        try:
            alertas = self.alerta_service.obtener_alertas_por_tipo(tipo_alerta)
            
            return jsonify({
                'success': True,
                'data': [
                    {
                        'alerta_id': alerta.alerta_id,
                        'mensaje': alerta.mensaje,
                        'prioridad': alerta.prioridad,
                        'fecha_creacion': alerta.fecha_creacion.isoformat() if alerta.fecha_creacion else None,
                        'instrumento': {
                            'id': alerta.instrumento.instrumento_id,
                            'nombre': alerta.instrumento.nombre
                        } if alerta.instrumento else None,
                        'procedimiento': {
                            'id': alerta.procedimiento.procedimiento_id,
                            'nombre': alerta.procedimiento.nombre
                        } if alerta.procedimiento else None
                    }
                    for alerta in alertas
                ],
                'tipo_alerta': tipo_alerta,
                'total': len(alertas)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def resolver_alerta(self, alerta_id: int) -> tuple:
        """
        Marcar una alerta como resuelta
        """
        try:
            data = request.json or {}
            resolucion = data.get('resolucion', '')
            
            alerta = self.alerta_service.resolver_alerta(alerta_id, resolucion)
            
            if not alerta:
                return jsonify({
                    'success': False,
                    'message': 'Alerta no encontrada'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Alerta resuelta exitosamente',
                'data': {
                    'alerta_id': alerta.alerta_id,
                    'fecha_resolucion': alerta.fecha_resolucion.isoformat() if alerta.fecha_resolucion else None,
                    'resolucion': alerta.resolucion
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def obtener_alerta(self, alerta_id: int) -> tuple:
        """
        Obtener información detallada de una alerta
        """
        try:
            alerta = self.alerta_service.get_by_id(alerta_id)
            
            if not alerta:
                return jsonify({
                    'success': False,
                    'message': 'Alerta no encontrada'
                }), 404
            
            return jsonify({
                'success': True,
                'data': {
                    'alerta_id': alerta.alerta_id,
                    'tipo_alerta': alerta.tipo_alerta,
                    'mensaje': alerta.mensaje,
                    'prioridad': alerta.prioridad,
                    'activa': alerta.activa,
                    'fecha_creacion': alerta.fecha_creacion.isoformat() if alerta.fecha_creacion else None,
                    'fecha_resolucion': alerta.fecha_resolucion.isoformat() if alerta.fecha_resolucion else None,
                    'resolucion': alerta.resolucion,
                    'instrumento': {
                        'id': alerta.instrumento.instrumento_id,
                        'nombre': alerta.instrumento.nombre,
                        'estado': alerta.instrumento.estado
                    } if alerta.instrumento else None,
                    'procedimiento': {
                        'id': alerta.procedimiento.procedimiento_id,
                        'nombre': alerta.procedimiento.nombre,
                        'estado': alerta.procedimiento.estado
                    } if alerta.procedimiento else None
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def ejecutar_verificaciones(self) -> tuple:
        """
        Ejecutar verificaciones automáticas de alertas
        """
        try:
            # Solo administradores pueden ejecutar verificaciones manuales
            if g.current_user.rol != 'Administrador':
                return jsonify({
                    'success': False,
                    'message': 'Se requieren permisos de administrador'
                }), 403
            
            resultado = self.alerta_service.ejecutar_verificaciones_automaticas()
            
            return jsonify({
                'success': True,
                'message': 'Verificaciones ejecutadas exitosamente',
                'data': resultado
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def obtener_estadisticas_alertas(self) -> tuple:
        """
        Obtener estadísticas de alertas
        """
        try:
            # Obtener filtros de fecha desde query parameters
            fecha_inicio = request.args.get('fecha_inicio')
            fecha_fin = request.args.get('fecha_fin')
            
            # Convertir fechas si se proporcionan
            fecha_inicio_dt = None
            fecha_fin_dt = None
            
            if fecha_inicio:
                fecha_inicio_dt = datetime.fromisoformat(fecha_inicio)
            if fecha_fin:
                fecha_fin_dt = datetime.fromisoformat(fecha_fin)
            
            estadisticas = self.alerta_service.obtener_estadisticas_alertas(fecha_inicio_dt, fecha_fin_dt)
            
            return jsonify({
                'success': True,
                'data': estadisticas
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': 'Formato de fecha inválido',
                'error': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def obtener_resumen_alertas(self) -> tuple:
        """
        Obtener resumen rápido de alertas para dashboard
        """
        try:
            alertas_activas = self.alerta_service.obtener_alertas_activas(10)
            
            # Contar por prioridad
            conteo_prioridad = {
                'Alta': 0,
                'Media': 0,
                'Baja': 0
            }
            
            # Contar por tipo
            conteo_tipo = {}
            
            for alerta in alertas_activas:
                conteo_prioridad[alerta.prioridad] = conteo_prioridad.get(alerta.prioridad, 0) + 1
                conteo_tipo[alerta.tipo_alerta] = conteo_tipo.get(alerta.tipo_alerta, 0) + 1
            
            return jsonify({
                'success': True,
                'data': {
                    'total_activas': len(alertas_activas),
                    'por_prioridad': conteo_prioridad,
                    'por_tipo': conteo_tipo,
                    'alertas_recientes': [
                        {
                            'alerta_id': alerta.alerta_id,
                            'tipo_alerta': alerta.tipo_alerta,
                            'mensaje': alerta.mensaje,
                            'prioridad': alerta.prioridad,
                            'fecha_creacion': alerta.fecha_creacion.isoformat() if alerta.fecha_creacion else None
                        }
                        for alerta in alertas_activas[:5]  # Solo las 5 más recientes
                    ]
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
