@echo off
REM Script para configurar el entorno del microservicio de detección YOLO en Windows
REM Versión: 1.0
REM Fecha: 26/05/2025

echo === Configurando entorno para Microservicio de Detección YOLO ===

REM Verificar que Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no está instalado o no está en el PATH
    echo Por favor instala Python 3.11 o superior
    pause
    exit /b 1
)

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate

REM Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Crear directorios necesarios
echo Creando estructura de directorios...
if not exist "models" mkdir models
if not exist "temp_uploads" mkdir temp_uploads
if not exist "logs" mkdir logs

REM Copiar archivo de configuración
if not exist ".env" (
    if exist ".env.example" (
        echo Copiando archivo de configuración...
        copy .env.example .env
    )
)

REM Descargar modelo preentrenado de YOLO
echo Descargando modelo YOLO preentrenado...
python -c "from ultralytics import YOLO; import os; os.makedirs('models', exist_ok=True); model = YOLO('yolov8n.pt'); print('Modelo YOLOv8n descargado exitosamente'); print('Configuración completada')"

if %errorlevel% neq 0 (
    echo Advertencia: No se pudo descargar el modelo YOLO
    echo Esto puede deberse a problemas de conectividad
    echo El modelo se descargará automáticamente en el primer uso
)

echo.
echo === Configuración completada exitosamente ===
echo.
echo Para activar el entorno manualmente: venv\Scripts\activate
echo Para ejecutar la aplicación: python run.py
echo Para ejecutar tests: pytest tests/
echo Para ver documentación: http://localhost:8002/docs
echo.
pause
