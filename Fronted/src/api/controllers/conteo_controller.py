# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\api\controllers\conteo_controller.py
"""
Controlador para gestión de conteos de instrumentos
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from typing import List, Optional, Any, Dict
from src.services.conteo_service import ConteoService
from src.api.schemas import ConteoCreateSchema, ConteoUpdateSchema
from src.utils.validators import validate_request_data

class ConteoController:
    """
    Controlador para operaciones de conteos de instrumentos
    """
    
    def __init__(self):
        self.conteo_service = ConteoService()
    
    def crear_conteo(self) -> tuple:
        """
        Crear un nuevo conteo de instrumento
        """
        try:
            # Validar datos de entrada
            data = validate_request_data(request.json, ConteoCreateSchema)
            
            # Agregar usuario contador desde la sesión
            data['usuario_contador_id'] = g.current_user.usuario_id
            data['fecha_conteo'] = datetime.now()
            
            # Crear conteo
            conteo = self.conteo_service.crear_conteo(data)
            
            return jsonify({
                'success': True,
                'message': 'Conteo creado exitosamente',
                'data': {
                    'conteo_id': conteo.conteo_id,
                    'instrumento_id': conteo.instrumento_id,
                    'procedimiento_id': conteo.procedimiento_id,
                    'tipo_conteo': conteo.tipo_conteo,
                    'cantidad_contada': conteo.cantidad_contada,
                    'fecha_conteo': conteo.fecha_conteo.isoformat()
                }
            }), 201
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': 'Error en los datos proporcionados',
                'error': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def obtener_conteo(self, conteo_id: int) -> tuple:
        """
        Obtener información de un conteo específico
        """
        try:
            conteo = self.conteo_service.get_by_id(conteo_id)
            
            if not conteo:
                return jsonify({
                    'success': False,
                    'message': 'Conteo no encontrado'
                }), 404
            
            return jsonify({
                'success': True,
                'data': {
                    'conteo_id': conteo.conteo_id,
                    'instrumento': {
                        'id': conteo.instrumento.instrumento_id,
                        'nombre': conteo.instrumento.nombre
                    } if conteo.instrumento else None,
                    'procedimiento': {
                        'id': conteo.procedimiento.procedimiento_id,
                        'nombre': conteo.procedimiento.nombre
                    } if conteo.procedimiento else None,
                    'tipo_conteo': conteo.tipo_conteo,
                    'cantidad_contada': conteo.cantidad_contada,
                    'discrepancia': conteo.discrepancia,
                    'observaciones': conteo.observaciones,
                    'fecha_conteo': conteo.fecha_conteo.isoformat() if conteo.fecha_conteo else None,
                    'usuario_contador': {
                        'id': conteo.usuario_contador.usuario_id,
                        'nombre': conteo.usuario_contador.nombre_completo
                    } if conteo.usuario_contador else None
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def actualizar_conteo(self, conteo_id: int) -> tuple:
        """
        Actualizar información de un conteo
        """
        try:
            # Validar datos de entrada
            data = validate_request_data(request.json, ConteoUpdateSchema)
            
            # Actualizar conteo
            conteo = self.conteo_service.actualizar_conteo(conteo_id, data)
            
            if not conteo:
                return jsonify({
                    'success': False,
                    'message': 'Conteo no encontrado'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Conteo actualizado exitosamente',
                'data': {
                    'conteo_id': conteo.conteo_id,
                    'cantidad_contada': conteo.cantidad_contada,
                    'discrepancia': conteo.discrepancia,
                    'observaciones': conteo.observaciones
                }
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': 'Error en los datos proporcionados',
                'error': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def obtener_conteos_procedimiento(self, procedimiento_id: int) -> tuple:
        """
        Obtener todos los conteos de un procedimiento
        """
        try:
            conteos = self.conteo_service.obtener_conteos_por_procedimiento(procedimiento_id)
            
            return jsonify({
                'success': True,
                'data': [
                    {
                        'conteo_id': conteo.conteo_id,
                        'instrumento': {
                            'id': conteo.instrumento.instrumento_id,
                            'nombre': conteo.instrumento.nombre
                        } if conteo.instrumento else None,
                        'tipo_conteo': conteo.tipo_conteo,
                        'cantidad_contada': conteo.cantidad_contada,
                        'discrepancia': conteo.discrepancia,
                        'fecha_conteo': conteo.fecha_conteo.isoformat() if conteo.fecha_conteo else None,
                        'usuario_contador': {
                            'nombre': conteo.usuario_contador.nombre_completo
                        } if conteo.usuario_contador else None
                    }
                    for conteo in conteos
                ],
                'total': len(conteos)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def verificar_conteo_completo(self, procedimiento_id: int) -> tuple:
        """
        Verificar si el conteo de un procedimiento está completo
        """
        try:
            verificacion = self.conteo_service.verificar_conteo_completo(procedimiento_id)
            
            return jsonify({
                'success': True,
                'data': verificacion
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def obtener_estadisticas_conteo(self) -> tuple:
        """
        Obtener estadísticas de conteos
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
            
            estadisticas = self.conteo_service.obtener_estadisticas_conteo(fecha_inicio_dt, fecha_fin_dt)
            
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
    
    def buscar_conteos(self) -> tuple:
        """
        Buscar conteos con filtros
        """
        try:
            # Obtener parámetros de búsqueda
            filtros = {}
            
            if request.args.get('instrumento_id'):
                filtros['instrumento_id'] = int(request.args.get('instrumento_id'))
            if request.args.get('procedimiento_id'):
                filtros['procedimiento_id'] = int(request.args.get('procedimiento_id'))
            if request.args.get('tipo_conteo'):
                filtros['tipo_conteo'] = request.args.get('tipo_conteo')
            if request.args.get('discrepancia'):
                filtros['discrepancia'] = request.args.get('discrepancia').lower() == 'true'
            if request.args.get('fecha_inicio'):
                filtros['fecha_inicio'] = datetime.fromisoformat(request.args.get('fecha_inicio'))
            if request.args.get('fecha_fin'):
                filtros['fecha_fin'] = datetime.fromisoformat(request.args.get('fecha_fin'))
            
            # Parámetros de paginación
            limit = int(request.args.get('limit', 50))
            offset = int(request.args.get('offset', 0))
            
            resultado = self.conteo_service.buscar_conteos(filtros, limit, offset)
            
            return jsonify({
                'success': True,
                'data': [
                    {
                        'conteo_id': conteo.conteo_id,
                        'instrumento': {
                            'id': conteo.instrumento.instrumento_id,
                            'nombre': conteo.instrumento.nombre
                        } if conteo.instrumento else None,
                        'procedimiento': {
                            'id': conteo.procedimiento.procedimiento_id,
                            'nombre': conteo.procedimiento.nombre
                        } if conteo.procedimiento else None,
                        'tipo_conteo': conteo.tipo_conteo,
                        'cantidad_contada': conteo.cantidad_contada,
                        'discrepancia': conteo.discrepancia,
                        'fecha_conteo': conteo.fecha_conteo.isoformat() if conteo.fecha_conteo else None,
                        'usuario_contador': {
                            'nombre': conteo.usuario_contador.nombre_completo
                        } if conteo.usuario_contador else None
                    }
                    for conteo in resultado['conteos']
                ],
                'pagination': {
                    'total': resultado['total'],
                    'limit': resultado['limit'],
                    'offset': resultado['offset'],
                    'has_more': resultado['offset'] + resultado['limit'] < resultado['total']
                }
            }), 200
            
        except ValueError as e:
            return jsonify({
                'success': False,
                'message': 'Parámetros inválidos',
                'error': str(e)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
