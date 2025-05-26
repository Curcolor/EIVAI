# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\src\utils\file_utils.py
"""
Utilidades para manejo de archivos y fotos
"""
import os
import uuid
import hashlib
from typing import List, Optional, Tuple
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageOps
from fastapi import UploadFile, HTTPException
from io import BytesIO
import aiofiles

# Configuración de archivos
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_WIDTH = 2048
MAX_IMAGE_HEIGHT = 2048
UPLOAD_DIR = "uploads"
PHOTOS_DIR = os.path.join(UPLOAD_DIR, "photos")
THUMBNAILS_DIR = os.path.join(UPLOAD_DIR, "thumbnails")


class FileValidationError(Exception):
    """Excepción para errores de validación de archivos"""
    pass


def init_upload_directories():
    """
    Inicializar directorios de carga de archivos
    """
    for directory in [UPLOAD_DIR, PHOTOS_DIR, THUMBNAILS_DIR]:
        Path(directory).mkdir(parents=True, exist_ok=True)


def validate_file_extension(filename: str, allowed_extensions: set) -> bool:
    """
    Validar extensión de archivo
    """
    if not filename:
        return False
    
    file_ext = Path(filename).suffix.lower()
    return file_ext in allowed_extensions


def validate_file_size(file_size: int, max_size: int = MAX_FILE_SIZE) -> bool:
    """
    Validar tamaño de archivo
    """
    return file_size <= max_size


def generate_unique_filename(original_filename: str) -> str:
    """
    Generar nombre único para archivo manteniendo la extensión
    """
    file_ext = Path(original_filename).suffix.lower()
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{unique_id}{file_ext}"


def calculate_file_hash(file_content: bytes) -> str:
    """
    Calcular hash MD5 del contenido del archivo
    """
    return hashlib.md5(file_content).hexdigest()


async def validate_image_file(file: UploadFile) -> Tuple[bool, str]:
    """
    Validar archivo de imagen
    
    Returns:
        Tuple[bool, str]: (es_válido, mensaje_error)
    """
    # Validar extensión
    if not validate_file_extension(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        return False, f"Extensión no permitida. Permitidas: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
    
    # Leer contenido del archivo
    try:
        content = await file.read()
        await file.seek(0)  # Resetear posición del archivo
    except Exception as e:
        return False, f"Error al leer archivo: {str(e)}"
    
    # Validar tamaño
    if not validate_file_size(len(content)):
        return False, f"Archivo demasiado grande. Máximo permitido: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
    
    # Validar que sea una imagen válida
    try:
        with Image.open(BytesIO(content)) as img:
            img.verify()
    except Exception:
        return False, "El archivo no es una imagen válida"
    
    return True, ""


async def process_and_save_image(
    file: UploadFile, 
    conteo_id: int,
    create_thumbnail: bool = True
) -> dict:
    """
    Procesar y guardar imagen con redimensionamiento y thumbnail
    
    Returns:
        dict: Información del archivo guardado
    """
    # Validar imagen
    is_valid, error_msg = await validate_image_file(file)
    if not is_valid:
        raise FileValidationError(error_msg)
    
    # Leer contenido
    content = await file.read()
    
    # Generar información del archivo
    original_filename = file.filename
    unique_filename = generate_unique_filename(original_filename)
    file_hash = calculate_file_hash(content)
    file_size = len(content)
    
    # Procesar imagen
    try:
        with Image.open(BytesIO(content)) as img:
            # Convertir a RGB si es necesario
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Aplicar rotación automática basada en EXIF
            img = ImageOps.exif_transpose(img)
            
            # Redimensionar si es necesario
            if img.width > MAX_IMAGE_WIDTH or img.height > MAX_IMAGE_HEIGHT:
                img.thumbnail((MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT), Image.Resampling.LANCZOS)
            
            # Guardar imagen principal
            main_path = os.path.join(PHOTOS_DIR, unique_filename)
            img.save(main_path, quality=90, optimize=True)
            
            # Crear thumbnail si se solicita
            thumbnail_path = None
            if create_thumbnail:
                thumb_img = img.copy()
                thumb_img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                thumbnail_filename = f"thumb_{unique_filename}"
                thumbnail_path = os.path.join(THUMBNAILS_DIR, thumbnail_filename)
                thumb_img.save(thumbnail_path, quality=85, optimize=True)
            
            # Obtener información final
            final_size = os.path.getsize(main_path)
            width, height = img.size
            
    except Exception as e:
        raise FileValidationError(f"Error al procesar imagen: {str(e)}")
    
    return {
        'original_filename': original_filename,
        'stored_filename': unique_filename,
        'file_path': main_path,
        'thumbnail_path': thumbnail_path,
        'file_hash': file_hash,
        'file_size': final_size,
        'width': width,
        'height': height,
        'conteo_id': conteo_id,
        'mime_type': f"image/{Path(unique_filename).suffix[1:]}"
    }


async def save_multiple_images(
    files: List[UploadFile], 
    conteo_id: int
) -> List[dict]:
    """
    Guardar múltiples imágenes
    """
    if len(files) > 10:  # Límite de 10 imágenes por conteo
        raise FileValidationError("Máximo 10 imágenes permitidas por conteo")
    
    saved_files = []
    
    for file in files:
        try:
            file_info = await process_and_save_image(file, conteo_id)
            saved_files.append(file_info)
        except FileValidationError as e:
            # Limpiar archivos ya guardados en caso de error
            for saved_file in saved_files:
                try:
                    if os.path.exists(saved_file['file_path']):
                        os.remove(saved_file['file_path'])
                    if saved_file['thumbnail_path'] and os.path.exists(saved_file['thumbnail_path']):
                        os.remove(saved_file['thumbnail_path'])
                except:
                    pass
            raise e
    
    return saved_files


def delete_image_files(file_path: str, thumbnail_path: Optional[str] = None):
    """
    Eliminar archivos de imagen del sistema de archivos
    """
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception:
        pass
    
    try:
        if thumbnail_path and os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
    except Exception:
        pass


def get_file_url(filename: str, is_thumbnail: bool = False) -> str:
    """
    Obtener URL para acceder a un archivo
    """
    if is_thumbnail:
        return f"/static/uploads/thumbnails/{filename}"
    else:
        return f"/static/uploads/photos/{filename}"


# Inicializar directorios al importar el módulo
init_upload_directories()
