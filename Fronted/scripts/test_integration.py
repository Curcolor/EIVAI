# filepath: c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted\scripts\test_integration.py
"""
Script de prueba de integración para el sistema EIVAI
"""
import asyncio
import sys
import os
from datetime import datetime

# Agregar el directorio padre al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.database import get_db, create_all_tables


async def test_database_connection():
    """
    Probar conexión a la base de datos
    """
    print("🔌 Probando conexión a la base de datos...")
    try:
        db_gen = get_db()
        db = next(db_gen)
        db.close()
        print("✅ Conexión a la base de datos exitosa")
        return True
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {str(e)}")
        return False


def test_usuario_service():
    """
    Probar servicio de usuarios
    """
    print("\n👤 Probando servicio de usuarios...")
    try:
        from src.services.usuario_service import UsuarioService
        usuario_service = UsuarioService()
        print("✅ Servicio de usuarios importado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en servicio de usuarios: {str(e)}")
        return False


def test_instrumento_service():
    """
    Probar servicio de instrumentos
    """
    print("\n🔧 Probando servicio de instrumentos...")
    try:
        from src.services.instrumento_service import InstrumentoService
        instrumento_service = InstrumentoService()
        print("✅ Servicio de instrumentos importado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en servicio de instrumentos: {str(e)}")
        return False


def test_alerta_service():
    """
    Probar servicio de alertas
    """
    print("\n🚨 Probando servicio de alertas...")
    try:
        from src.services.alerta_service import AlertaService
        alerta_service = AlertaService()
        print("✅ Servicio de alertas importado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en servicio de alertas: {str(e)}")
        return False


def test_set_service():
    """
    Probar servicio de sets quirúrgicos
    """
    print("\n📦 Probando servicio de sets quirúrgicos...")
    try:
        from src.services.set_service import SetService
        set_service = SetService()
        print("✅ Servicio de sets quirúrgicos importado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en servicio de sets: {str(e)}")
        return False


def test_dashboard_service():
    """
    Probar servicio de dashboard
    """
    print("\n📊 Probando servicio de dashboard...")
    try:
        from src.services.dashboard_service import DashboardService
        dashboard_service = DashboardService()
        print("✅ Servicio de dashboard importado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en servicio de dashboard: {str(e)}")
        return False


async def test_api_schemas():
    """
    Probar importación de esquemas
    """
    print("\n📋 Probando esquemas de la API...")
    try:
        from src.api.schemas import (
            UsuarioResponse, 
            InstrumentoResponse, 
            AlertaResponse,
            DashboardStatsResponse,
            ConteoCreateSchema
        )
        print("✅ Todos los esquemas se importaron correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al importar esquemas: {str(e)}")
        return False


async def test_controllers():
    """
    Probar importación de controladores
    """
    print("\n🎮 Probando controladores...")
    try:
        from src.api.controllers.usuario_controller import UsuarioController
        from src.api.controllers.instrumento_controller import InstrumentoController
        from src.api.controllers.alerta_controller import AlertaController
        from src.api.controllers.dashboard_controller import DashboardController
        
        print("✅ Todos los controladores se importaron correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al importar controladores: {str(e)}")
        return False


async def test_routes():
    """
    Probar importación de rutas
    """
    print("\n🛣️ Probando rutas de la API...")
    try:
        from src.api.routes import (
            usuarios_router,
            instrumentos_router,
            alertas_router,
            dashboard_router
        )
        print("✅ Todas las rutas se importaron correctamente")
        return True
    except Exception as e:
        print(f"❌ Error al importar rutas: {str(e)}")
        return False


async def test_file_utils():
    """
    Probar utilidades de archivos
    """
    print("\n📁 Probando utilidades de archivos...")
    try:
        from src.utils.file_utils import (
            validate_file_extension,
            generate_unique_filename,
            init_upload_directories
        )
        
        # Probar validación de extensión
        assert validate_file_extension("test.jpg", {'.jpg', '.png'}) == True
        assert validate_file_extension("test.txt", {'.jpg', '.png'}) == False
        
        # Probar generación de nombre único
        unique_name = generate_unique_filename("test.jpg")
        assert unique_name.endswith('.jpg')
        
        # Inicializar directorios
        init_upload_directories()
        
        print("✅ Utilidades de archivos funcionando correctamente")
        return True
    except Exception as e:
        print(f"❌ Error en utilidades de archivos: {str(e)}")
        return False


async def run_all_tests():
    """
    Ejecutar todas las pruebas
    """
    print("🚀 Iniciando pruebas de integración del sistema EIVAI\n")
    
    tests = [
        ("Conexión a la base de datos", test_database_connection),
        ("Esquemas de la API", test_api_schemas),
        ("Controladores", test_controllers),
        ("Rutas", test_routes),
        ("Utilidades de archivos", test_file_utils),
        ("Servicio de usuarios", test_usuario_service),
        ("Servicio de instrumentos", test_instrumento_service),
        ("Servicio de alertas", test_alerta_service),
        ("Servicio de sets", test_set_service),
        ("Servicio de dashboard", test_dashboard_service),
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                resultado = await test_func()
            else:
                resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"❌ Error inesperado en {nombre}: {str(e)}")
            resultados.append((nombre, False))
    
    # Resumen de resultados
    print("\n" + "="*60)
    print("📋 RESUMEN DE PRUEBAS")
    print("="*60)
    
    exitosos = 0
    fallidos = 0
    
    for nombre, resultado in resultados:
        if resultado:
            print(f"✅ {nombre}")
            exitosos += 1
        else:
            print(f"❌ {nombre}")
            fallidos += 1
    
    print("\n" + "-"*60)
    print(f"Total: {len(resultados)} pruebas")
    print(f"Exitosas: {exitosos}")
    print(f"Fallidas: {fallidos}")
    
    if fallidos == 0:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("El sistema EIVAI está listo para uso.")
    else:
        print(f"\n⚠️ {fallidos} pruebas fallaron.")
        print("Revisar los errores antes de usar el sistema.")
    
    return fallidos == 0


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
