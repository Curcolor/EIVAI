#!/bin/bash

# Script de configuración del entorno de desarrollo
# Autor: GitHub Copilot
# Fecha: Mayo 2025

echo "=== Configurando entorno de desarrollo para el Micorservicio API de Texto a voz ==="
echo "--------------------------------------------------------------------"

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "Creando entorno virtual..."
    python -m venv .venv
    echo "Entorno virtual creado correctamente."
else
    echo "El entorno virtual ya existe."
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/Scripts/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Crear archivo .env desde .env.example si no existe
if [ ! -f ".env" ]; then
    echo "Creando archivo .env desde la plantilla..."
    cp .env.example .env
    echo "⚠️  Por favor, edite el archivo .env y configure su clave API de DeepSeek."
else
    echo "El archivo .env ya existe."
fi

# Crear directorio de logs si no existe
if [ ! -d "logs" ]; then
    echo "Creando directorio de logs..."
    mkdir logs
fi

echo "--------------------------------------------------------------------"
echo "✅ Configuración completada. Para iniciar el microservicio API ejecute:"
echo "    python run.py"
echo ""
echo "📝 Para ejecutar las pruebas:"
echo "    python probar_api.py"
echo ""
echo "🐳 Para iniciar con Docker:"
echo "    docker-compose up -d"
echo "--------------------------------------------------------------------"
