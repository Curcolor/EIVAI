import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings:
    """Configuración de la aplicación"""
    
    # Configuración de la aplicación
    APP_NAME: str = "YOLO Detection Microservice"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Microservicio para detección de instrumentos quirúrgicos usando YOLO"
    
    # Configuración del servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8002))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Configuración de YOLO
    YOLO_MODEL_PATH: str = os.getenv("YOLO_MODEL_PATH", "yolov8n.pt")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", 0.5))
    IOU_THRESHOLD: float = float(os.getenv("IOU_THRESHOLD", 0.45))
    
    # Configuración de archivos
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "temp_uploads")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB
    ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "bmp", "tiff", "webp"}
    
    # Mapeo de instrumentos quirúrgicos
    SURGICAL_INSTRUMENTS_MAP = {
        0: {"codigo": "BISP-001", "nombre": "Bisturí #11", "descripcion": "Bisturí hoja número 11"},
        1: {"codigo": "BISP-002", "nombre": "Bisturí #15", "descripcion": "Bisturí hoja número 15"},
        2: {"codigo": "PINZ-001", "nombre": "Pinza Kelly", "descripcion": "Pinza hemostática Kelly curva"},
        3: {"codigo": "PINZ-002", "nombre": "Pinza Allis", "descripcion": "Pinza de prensión Allis"},
        4: {"codigo": "TIJR-001", "nombre": "Tijera Mayo", "descripcion": "Tijera Mayo recta"},
        5: {"codigo": "TIJR-002", "nombre": "Tijera Metzenbaum", "descripcion": "Tijera Metzenbaum curva"},
        6: {"codigo": "PORT-001", "nombre": "Portaagujas", "descripcion": "Portaagujas Mayo-Hegar"},
        7: {"codigo": "SEPA-001", "nombre": "Separador Farabeuf", "descripcion": "Separador autoestático Farabeuf"},
        8: {"codigo": "ASPI-001", "nombre": "Aspirador quirúrgico", "descripcion": "Tubo de aspiración quirúrgica"},
        9: {"codigo": "GASA-001", "nombre": "Gasas estériles", "descripcion": "Paquete de gasas estériles 4x4"}
    }

# Instancia global de configuración
settings = Settings()
