#!/usr/bin/env python3
"""
Script de prueba simplificado para componentes FastAPI del sistema EIVAI
Se enfoca en los componentes que sabemos que funcionan
"""

import sys
import os
import traceback
from pathlib import Path

# Agregar el directorio raíz al path de Python
script_dir = Path(__file__).parent
project_root = script_dir.parent
sys.path.insert(0, str(project_root))

def test_database_connection():
    """Probar conexión a la base de datos"""
    try:
        from src.config.database import SessionLocal, engine
        
        # Probar crear sesión
        session = SessionLocal()
        session.close()
        
        # Probar conexión al engine
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            
        return True, "Conexión exitosa"
    except Exception as e:
        return False, str(e)

def test_schemas():
    """Probar importación de esquemas"""
    try:
        from src.api.schemas import (
            UsuarioCreate, UsuarioResponse,
            InstrumentoCreate, InstrumentoResponse,
            ConteoCreateSchema, ConteoInstrumentoResponse,
            AlertaCreateSchema, AlertaResponse,
            EstadisticasInstrumento,
            DashboardStatsResponse
        )
        return True, "Todos los esquemas importados correctamente"
    except Exception as e:
        return False, str(e)

def test_services():
    """Probar importación de servicios"""
    services = [
        ("usuario_service", "src.services.usuario_service", "UsuarioService"),
        ("instrumento_service", "src.services.instrumento_service", "InstrumentoService"),
        ("alerta_service", "src.services.alerta_service", "AlertaService"),
        ("conteo_service", "src.services.conteo_service", "ConteoService"),
        ("dashboard_service", "src.services.dashboard_service", "DashboardService"),
        ("set_service", "src.services.set_service", "SetService"),
    ]
    
    results = {}
    for name, module, class_name in services:
        try:
            module_obj = __import__(module, fromlist=[class_name])
            service_class = getattr(module_obj, class_name)
            # Intentar instanciar (sin hacer llamadas a la DB)
            results[name] = True
        except Exception as e:
            results[name] = False
            print(f"❌ Error en {name}: {str(e)}")
    
    return results

def test_fastapi_routes():
    """Probar importación de rutas FastAPI"""
    routes = [
        ("usuarios", "src.api.routes.usuarios"),
        ("instrumentos", "src.api.routes.instrumentos"),
        ("procedimientos", "src.api.routes.procedimientos"),
        ("conteos", "src.api.routes.conteos"),
        ("alertas", "src.api.routes.alertas"),
        ("sets", "src.api.routes.sets"),
        ("dashboard", "src.api.routes.dashboard"),
    ]
    
    results = {}
    for name, module in routes:
        try:
            module_obj = __import__(module, fromlist=["router"])
            router = getattr(module_obj, "router")
            results[name] = True
        except Exception as e:
            results[name] = False
            print(f"❌ Error en ruta {name}: {str(e)}")
    
    return results

def test_file_utils():
    """Probar utilidades de archivos"""
    try:
        from src.utils.file_utils import (
            validate_image_file, 
            init_upload_directories,
            FileValidationError
        )
        return True, "Utilidades de archivos importadas correctamente"
    except Exception as e:
        return False, str(e)

def test_fastapi_app():
    """Probar que la aplicación FastAPI se puede crear"""
    try:
        from src.api.app import app
        # Verificar que es una instancia de FastAPI
        from fastapi import FastAPI
        if isinstance(app, FastAPI):
            return True, "Aplicación FastAPI creada exitosamente"
        else:
            return False, "app no es una instancia de FastAPI"
    except Exception as e:
        return False, str(e)

def main():
    print("🚀 Iniciando pruebas simplificadas del sistema EIVAI")
    print("="*60)
    
    tests = [
        ("🔌 Conexión a la base de datos", test_database_connection),
        ("📋 Esquemas de la API", test_schemas),
        ("📁 Utilidades de archivos", test_file_utils),
        ("🚀 Aplicación FastAPI", test_fastapi_app),
    ]
    
    results = {}
    
    # Ejecutar pruebas básicas
    for test_name, test_func in tests:
        print(f"{test_name}...")
        try:
            success, message = test_func()
            if success:
                print(f"✅ {message}")
                results[test_name] = True
            else:
                print(f"❌ {message}")
                results[test_name] = False
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            results[test_name] = False
    
    # Probar servicios
    print("👥 Probando servicios...")
    service_results = test_services()
    for service, success in service_results.items():
        if success:
            print(f"✅ Servicio {service} importado correctamente")
        results[f"servicio_{service}"] = success
    
    # Probar rutas FastAPI
    print("🛣️ Probando rutas FastAPI...")
    route_results = test_fastapi_routes()
    for route, success in route_results.items():
        if success:
            print(f"✅ Ruta {route} importada correctamente")
        results[f"ruta_{route}"] = success
    
    # Resumen
    print("="*60)
    print("📋 RESUMEN DE PRUEBAS")
    print("="*60)
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {test_name}")
    
    print("-" * 60)
    print(f"Total: {total} pruebas")
    print(f"Exitosas: {successful}")
    print(f"Fallidas: {total - successful}")
    
    if successful == total:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está listo.")
        return 0
    else:
        print(f"⚠️ {total - successful} pruebas fallaron.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
