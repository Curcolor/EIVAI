"""
Rutas API para gestión de conteos de instrumentos con soporte para fotos
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse

from ..middlewares.auth_middleware import require_auth
from ..controllers.conteo_controller import ConteoController
from ..schemas import (
    ConteoCreateSchema, 
    ConteoInstrumentoResponse, 
    ConteoWithPhotosResponse,
    PaginationParams,
    ResponseMessage
)
from ...utils.file_utils import save_multiple_images, FileValidationError

router = APIRouter(prefix="/api/conteos", tags=["Conteos"])
conteo_controller = ConteoController()


@router.post("", response_model=ConteoInstrumentoResponse)
async def crear_conteo(
    conteo_data: ConteoCreateSchema,
    usuario_actual = Depends(require_auth)
):
    """
    Crear un nuevo conteo de instrumento sin fotos
    """
    try:
        conteo = await conteo_controller.crear_conteo(
            conteo_data=conteo_data.dict(),
            usuario_id=usuario_actual.usuario_id
        )
        return conteo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/with-photos", response_model=ConteoWithPhotosResponse)
async def crear_conteo_con_fotos(
    procedimiento_id: int = Form(...),
    instrumento_id: int = Form(...),
    tipo_conteo: str = Form(...),
    cantidad_contada: int = Form(...),
    cantidad_esperada: int = Form(...),
    observaciones: Optional[str] = Form(None),
    fotos: List[UploadFile] = File(...),
    usuario_actual = Depends(require_auth)
):
    """
    Crear un nuevo conteo de instrumento con fotos
    """
    try:
        # Validar datos del conteo
        conteo_data = ConteoCreateSchema(
            procedimiento_id=procedimiento_id,
            instrumento_id=instrumento_id,
            tipo_conteo=tipo_conteo,
            cantidad_contada=cantidad_contada,
            cantidad_esperada=cantidad_esperada,
            observaciones=observaciones
        )
        
        # Crear el conteo primero
        conteo = await conteo_controller.crear_conteo(
            conteo_data=conteo_data.dict(),
            usuario_id=usuario_actual.usuario_id
        )
        
        # Guardar fotos si se proporcionaron
        if fotos and fotos[0].filename:  # Verificar que no sea una lista vacía
            try:
                saved_files = await save_multiple_images(fotos, conteo.conteo_id)
                
                # Guardar información de fotos en la base de datos
                for file_info in saved_files:
                    await conteo_controller.agregar_foto_conteo(
                        conteo_id=conteo.conteo_id,
                        foto_data=file_info
                    )
                
            except FileValidationError as e:
                # Si hay error con las fotos, eliminar el conteo creado
                await conteo_controller.eliminar_conteo(conteo.conteo_id)
                raise HTTPException(status_code=400, detail=f"Error con las fotos: {str(e)}")
        
        # Obtener conteo con fotos
        conteo_completo = await conteo_controller.obtener_conteo_con_fotos(conteo.conteo_id)
        return conteo_completo
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[ConteoInstrumentoResponse])
async def listar_conteos(
    pagination: PaginationParams = Depends(),
    procedimiento_id: Optional[int] = None,
    tipo_conteo: Optional[str] = None,
    tiene_discrepancia: Optional[bool] = None,
    usuario_actual = Depends(require_auth)
):
    """
    Listar conteos con filtros opcionales
    """
    try:
        filtros = {}
        if procedimiento_id:
            filtros['procedimiento_id'] = procedimiento_id
        if tipo_conteo:
            filtros['tipo_conteo'] = tipo_conteo
        if tiene_discrepancia is not None:
            filtros['tiene_discrepancia'] = tiene_discrepancia
            
        conteos = await conteo_controller.listar_conteos(
            skip=pagination.skip,
            limit=pagination.limit,
            filtros=filtros
        )
        return conteos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conteo_id}", response_model=ConteoWithPhotosResponse)
async def obtener_conteo(
    conteo_id: int,
    usuario_actual = Depends(require_auth)
):
    """
    Obtener conteo específico con fotos
    """
    try:
        conteo = await conteo_controller.obtener_conteo_con_fotos(conteo_id)
        if not conteo:
            raise HTTPException(status_code=404, detail="Conteo no encontrado")
        return conteo
    except Exception as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{conteo_id}", response_model=ConteoInstrumentoResponse)
async def actualizar_conteo(
    conteo_id: int,
    cantidad_contada: Optional[int] = None,
    observaciones: Optional[str] = None,
    usuario_actual = Depends(require_auth)
):
    """
    Actualizar conteo existente
    """
    try:
        datos_actualizacion = {}
        if cantidad_contada is not None:
            datos_actualizacion['cantidad_contada'] = cantidad_contada
        if observaciones is not None:
            datos_actualizacion['observaciones'] = observaciones
            
        conteo = await conteo_controller.actualizar_conteo(conteo_id, datos_actualizacion)
        return conteo
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{conteo_id}", response_model=ResponseMessage)
async def eliminar_conteo(
    conteo_id: int,
    usuario_actual = Depends(require_auth)
):
    """
    Eliminar conteo y sus fotos asociadas
    """
    try:
        await conteo_controller.eliminar_conteo(conteo_id)
        return ResponseMessage(message="Conteo eliminado exitosamente")
    except Exception as e:
        if "no encontrado" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/procedimiento/{procedimiento_id}/resumen")
async def obtener_resumen_conteos_procedimiento(
    procedimiento_id: int,
    usuario_actual = Depends(require_auth)
):
    """
    Obtener resumen de conteos para un procedimiento específico
    """
    try:
        resumen = await conteo_controller.obtener_resumen_conteos_procedimiento(procedimiento_id)
        return resumen
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/discrepancias/reporte")
async def obtener_reporte_discrepancias(
    fecha_inicio: Optional[str] = None,
    fecha_fin: Optional[str] = None,
    usuario_actual = Depends(require_auth)
):
    """
    Obtener reporte de discrepancias en conteos
    """
    try:
        reporte = await conteo_controller.obtener_reporte_discrepancias(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        return reporte
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{conteo_id}/verificar", response_model=ResponseMessage)
async def verificar_conteo(
    conteo_id: int,
    usuario_actual = Depends(require_auth)
):
    """
    Verificar y procesar un conteo específico
    """
    try:
        resultado = await conteo_controller.verificar_conteo(conteo_id)
        if resultado.get('discrepancia_encontrada'):
            return ResponseMessage(
                message=f"Conteo verificado - Discrepancia detectada: {resultado.get('mensaje')}",
                success=True
            )
        else:
            return ResponseMessage(
                message="Conteo verificado exitosamente sin discrepancias",
                success=True
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/estadisticas/discrepancias")
async def obtener_estadisticas_discrepancias(
    usuario_actual = Depends(require_auth)
):
    """
    Obtener estadísticas de discrepancias en conteos
    """
    try:
        stats = await conteo_controller.obtener_estadisticas_discrepancias()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
