# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\api\controllers\set_controller.py
"""
Controlador para gestión de sets quirúrgicos
"""
from typing import Dict, Any, List
from typing import List, Optional, Any, Dict
from src.services.set_service import SetService
from src.api.schemas import SetQuirurgicoCreate, SetQuirurgicoUpdate, SetQuirurgicoResponse

class SetController:
    """
    Controlador para operaciones de sets quirúrgicos
    """
    
    def __init__(self):
        self.set_service = SetService()
    
    def crear_set(self) -> tuple:
        """
        Crear un nuevo set quirúrgico
        """
        try:
            data = request.json
            
            # Validaciones básicas
            if not data.get('nombre'):
                return jsonify({
                    'success': False,
                    'message': 'El nombre del set es requerido'
                }), 400
            
            # Crear set
            set_data = {
                'nombre': data['nombre'],
                'descripcion': data.get('descripcion', ''),
                'especialidad': data.get('especialidad', ''),
                'activo': data.get('activo', True)
            }
            
            set_quirurgico = self.set_service.crear_set(set_data)
            
            return jsonify({
                'success': True,
                'message': 'Set quirúrgico creado exitosamente',
                'data': {
                    'set_id': set_quirurgico.set_id,
                    'nombre': set_quirurgico.nombre,
                    'descripcion': set_quirurgico.descripcion,
                    'especialidad': set_quirurgico.especialidad,
                    'activo': set_quirurgico.activo
                }
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def obtener_set(self, set_id: int) -> tuple:
        """
        Obtener información de un set específico con sus instrumentos
        """
        try:
            set_quirurgico = self.set_service.obtener_set_con_instrumentos(set_id)
            
            if not set_quirurgico:
                return jsonify({
                    'success': False,
                    'message': 'Set quirúrgico no encontrado'
                }), 404
            
            return jsonify({
                'success': True,
                'data': {
                    'set_id': set_quirurgico.set_id,
                    'nombre': set_quirurgico.nombre,
                    'descripcion': set_quirurgico.descripcion,
                    'especialidad': set_quirurgico.especialidad,
                    'activo': set_quirurgico.activo,
                    'instrumentos': [
                        {
                            'instrumento_id': rel.instrumento.instrumento_id,
                            'nombre': rel.instrumento.nombre,
                            'cantidad': rel.cantidad,
                            'obligatorio': rel.obligatorio,
                            'disponible': rel.instrumento.cantidad_disponible >= rel.cantidad,
                            'estado': rel.instrumento.estado
                        }
                        for rel in set_quirurgico.instrumentos
                    ] if set_quirurgico.instrumentos else [],
                    'total_instrumentos': len(set_quirurgico.instrumentos) if set_quirurgico.instrumentos else 0
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def actualizar_set(self, set_id: int) -> tuple:
        """
        Actualizar información de un set quirúrgico
        """
        try:
            data = request.json
            
            set_quirurgico = self.set_service.actualizar_set(set_id, data)
            
            if not set_quirurgico:
                return jsonify({
                    'success': False,
                    'message': 'Set quirúrgico no encontrado'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Set quirúrgico actualizado exitosamente',
                'data': {
                    'set_id': set_quirurgico.set_id,
                    'nombre': set_quirurgico.nombre,
                    'descripcion': set_quirurgico.descripcion,
                    'especialidad': set_quirurgico.especialidad,
                    'activo': set_quirurgico.activo
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def agregar_instrumento(self, set_id: int) -> tuple:
        """
        Agregar un instrumento a un set quirúrgico
        """
        try:
            data = request.json
            
            if not data.get('instrumento_id'):
                return jsonify({
                    'success': False,
                    'message': 'ID del instrumento es requerido'
                }), 400
            
            relacion = self.set_service.agregar_instrumento_a_set(
                set_id=set_id,
                instrumento_id=data['instrumento_id'],
                cantidad=data.get('cantidad', 1),
                obligatorio=data.get('obligatorio', True)
            )
            
            if not relacion:
                return jsonify({
                    'success': False,
                    'message': 'No se pudo agregar el instrumento al set'
                }), 400
            
            return jsonify({
                'success': True,
                'message': 'Instrumento agregado al set exitosamente',
                'data': {
                    'set_id': relacion.set_id,
                    'instrumento_id': relacion.instrumento_id,
                    'cantidad': relacion.cantidad,
                    'obligatorio': relacion.obligatorio
                }
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def remover_instrumento(self, set_id: int, instrumento_id: int) -> tuple:
        """
        Remover un instrumento de un set quirúrgico
        """
        try:
            success = self.set_service.remover_instrumento_de_set(set_id, instrumento_id)
            
            if not success:
                return jsonify({
                    'success': False,
                    'message': 'Instrumento no encontrado en el set'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Instrumento removido del set exitosamente'
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def obtener_sets_activos(self) -> tuple:
        """
        Obtener todos los sets quirúrgicos activos
        """
        try:
            sets = self.set_service.obtener_sets_activos()
            
            return jsonify({
                'success': True,
                'data': [
                    {
                        'set_id': s.set_id,
                        'nombre': s.nombre,
                        'descripcion': s.descripcion,
                        'especialidad': s.especialidad,
                        'total_instrumentos': len(s.instrumentos) if s.instrumentos else 0
                    }
                    for s in sets
                ],
                'total': len(sets)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def obtener_sets_por_especialidad(self, especialidad: str) -> tuple:
        """
        Obtener sets quirúrgicos por especialidad
        """
        try:
            sets = self.set_service.obtener_sets_por_especialidad(especialidad)
            
            return jsonify({
                'success': True,
                'data': [
                    {
                        'set_id': s.set_id,
                        'nombre': s.nombre,
                        'descripcion': s.descripcion,
                        'total_instrumentos': len(s.instrumentos) if s.instrumentos else 0
                    }
                    for s in sets
                ],
                'especialidad': especialidad,
                'total': len(sets)
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def verificar_disponibilidad(self, set_id: int) -> tuple:
        """
        Verificar disponibilidad de todos los instrumentos de un set
        """
        try:
            verificacion = self.set_service.verificar_disponibilidad_set(set_id)
            
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
    
    def duplicar_set(self, set_id: int) -> tuple:
        """
        Duplicar un set quirúrgico existente
        """
        try:
            data = request.json
            
            if not data.get('nuevo_nombre'):
                return jsonify({
                    'success': False,
                    'message': 'Nuevo nombre es requerido'
                }), 400
            
            # Solo administradores pueden duplicar sets
            if g.current_user.rol != 'Administrador':
                return jsonify({
                    'success': False,
                    'message': 'Se requieren permisos de administrador'
                }), 403
            
            nuevo_set = self.set_service.duplicar_set(set_id, data['nuevo_nombre'])
            
            if not nuevo_set:
                return jsonify({
                    'success': False,
                    'message': 'Set original no encontrado'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Set duplicado exitosamente',
                'data': {
                    'set_id': nuevo_set.set_id,
                    'nombre': nuevo_set.nombre,
                    'descripcion': nuevo_set.descripcion,
                    'especialidad': nuevo_set.especialidad
                }
            }), 201
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def obtener_estadisticas_sets(self) -> tuple:
        """
        Obtener estadísticas de sets quirúrgicos
        """
        try:
            estadisticas = self.set_service.obtener_estadisticas_sets()
            
            return jsonify({
                'success': True,
                'data': estadisticas
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
    
    def buscar_sets(self) -> tuple:
        """
        Buscar sets quirúrgicos con filtros
        """
        try:
            termino = request.args.get('termino', '')
            especialidad = request.args.get('especialidad')
            activo = request.args.get('activo')
            
            # Convertir string a boolean si se proporciona
            activo_bool = None
            if activo is not None:
                activo_bool = activo.lower() == 'true'
            
            sets = self.set_service.buscar_sets(termino, especialidad, activo_bool)
            
            return jsonify({
                'success': True,
                'data': [
                    {
                        'set_id': s.set_id,
                        'nombre': s.nombre,
                        'descripcion': s.descripcion,
                        'especialidad': s.especialidad,
                        'activo': s.activo,
                        'total_instrumentos': len(s.instrumentos) if s.instrumentos else 0
                    }
                    for s in sets
                ],
                'total': len(sets),
                'filtros': {
                    'termino': termino,
                    'especialidad': especialidad,
                    'activo': activo
                }
            }), 200
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': 'Error interno del servidor',
                'error': str(e)
            }), 500
