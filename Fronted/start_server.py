#!/usr/bin/env python3
"""
Script simplificado para iniciar el servidor EIVAI
"""
import sys
import os
import subprocess
import time

def check_python():
    """Verificar que Python funcione"""
    try:
        import uvicorn
        import fastapi
        print("✅ Dependencias verificadas: uvicorn y fastapi disponibles")
        return True
    except ImportError as e:
        print(f"❌ Error de dependencias: {e}")
        print("💡 Instalar con: pip install fastapi uvicorn")
        return False

def start_server():
    """Iniciar el servidor"""
    try:
        print("🚀 Iniciando servidor EIVAI...")
        print("📍 URL: http://127.0.0.1:8000")
        print("📍 Documentación: http://127.0.0.1:8000/docs")
        print("🔄 Presiona Ctrl+C para detener")
        
        # Cambiar al directorio del proyecto
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        
        # Iniciar uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.api.app:app", 
            "--reload", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        return False
    
    return True

def main():
    """Función principal"""
    print("=" * 60)
    print("🏥 EIVAI - Sistema de Identificación de Herramientas Quirúrgicas")
    print("=" * 60)
    
    if not check_python():
        return False
    
    print("\n📋 Iniciando servidor FastAPI...")
    return start_server()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
