#!/bin/bash

# Script para configurar el entorno del microservicio de detección YOLO
# Versión: 1.0
# Fecha: 26/05/2025

echo "=== Configurando entorno para Microservicio de Detección YOLO ==="

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python -m venv venv
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Crear directorios necesarios
echo "Creando estructura de directorios..."
mkdir -p models
mkdir -p temp_uploads
mkdir -p logs

# Descargar modelo preentrenado de YOLO
echo "Descargando modelo YOLO preentrenado..."
python -c "
from ultralytics import YOLO
import os

# Crear directorio models si no existe
os.makedirs('models', exist_ok=True)

# Descargar modelo YOLOv8n (nano) para detección general
model = YOLO('yolov8n.pt')
print('Modelo YOLOv8n descargado exitosamente')

# El modelo se guardará automáticamente en ~/.ultralytics/
print('Configuración completada')
"

echo "=== Configuración completada exitosamente ==="
echo "Para activar el entorno: source venv/bin/activate"
echo "Para ejecutar la aplicación: uvicorn src.api.app:app --host 0.0.0.0 --port 8002 --reload"
