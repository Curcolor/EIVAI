#!/usr/bin/env python3
"""
Test simple para verificar el funcionamiento básico de la aplicación
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Verificar que todos los imports funcionen correctamente"""
    print("🔍 Probando imports...")
    
    try:
        from src.api.app import create_app
        print("✅ src.api.app importado correctamente")
        
        from src.config.config import settings
        print("✅ src.config.config importado correctamente")
        
        # Crear la aplicación
        app = create_app()
        print("✅ Aplicación FastAPI creada correctamente")
        
        print(f"📋 Nombre de la aplicación: {app.title}")
        print(f"📋 Versión: {app.version}")
        
        return True
    except Exception as e:
        print(f"❌ Error en imports: {e}")
        return False

def test_routes():
    """Verificar que las rutas estén configuradas"""
    print("\n🔍 Verificando rutas...")
    
    try:
        from src.api.app import create_app
        app = create_app()
        
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        
        print(f"✅ Total de rutas encontradas: {len(routes)}")
        
        # Verificar rutas importantes
        important_routes = ['/health', '/api/dashboard', '/api/test']
        found_routes = []
        
        for important_route in important_routes:
            for route in routes:
                if important_route in route:
                    found_routes.append(route)
                    break
        
        print(f"📋 Rutas importantes encontradas: {found_routes}")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando rutas: {e}")
        return False

def test_frontend_structure():
    """Verificar que los archivos frontend existan"""
    print("\n🔍 Verificando estructura frontend...")
    
    files_to_check = [
        'src/templates/index.html',
        'src/static/js/dashboard.js',
        'src/static/css/dashboard-integration.css',
        'src/api/frontend_services/main_service.py'
    ]
    
    existing_files = []
    missing_files = []
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path} - NO ENCONTRADO")
    
    print(f"📊 Archivos encontrados: {len(existing_files)}/{len(files_to_check)}")
    
    return len(missing_files) == 0

def test_services():
    """Verificar que los servicios frontend se puedan importar"""
    print("\n🔍 Verificando servicios frontend...")
    
    services = [
        'src.api.frontend_services.usuario_service',
        'src.api.frontend_services.instrumento_service',
        'src.api.frontend_services.dashboard_service',
        'src.api.frontend_services.main_service'
    ]
    
    successful_imports = 0
    
    for service in services:
        try:
            __import__(service)
            print(f"✅ {service}")
            successful_imports += 1
        except Exception as e:
            print(f"❌ {service} - Error: {e}")
    
    print(f"📊 Servicios importados correctamente: {successful_imports}/{len(services)}")
    
    return successful_imports == len(services)

def main():
    """Ejecutar todos los tests"""
    print("🚀 Iniciando tests de verificación del sistema EIVAI\n")
    
    tests = [
        ("Imports básicos", test_imports),
        ("Configuración de rutas", test_routes),
        ("Estructura frontend", test_frontend_structure),
        ("Servicios frontend", test_services)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"TEST: {test_name}")
        print('='*50)
        
        if test_func():
            passed_tests += 1
            print(f"✅ {test_name} - PASADO")
        else:
            print(f"❌ {test_name} - FALLIDO")
    
    print(f"\n{'='*50}")
    print("RESUMEN DE TESTS")
    print('='*50)
    print(f"Tests ejecutados: {total_tests}")
    print(f"Tests pasados: {passed_tests}")
    print(f"Tests fallidos: {total_tests - passed_tests}")
    print(f"Tasa de éxito: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 ¡Todos los tests pasaron! El sistema está listo.")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests fallaron. Revisar los errores arriba.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
