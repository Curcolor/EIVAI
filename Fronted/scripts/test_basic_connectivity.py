#!/usr/bin/env python3
"""
Script de prueba simplificado para verificar la comunicación básica frontend-backend
Usa endpoints de prueba sin autenticación
"""
import asyncio
import sys
import json
import httpx
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent.parent / "src"))


async def test_basic_endpoints():
    """
    Probar endpoints básicos sin autenticación
    """
    print("🔧 Iniciando pruebas básicas de conectividad...")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    
    # Lista de endpoints de prueba
    test_endpoints = [
        ("/api/test/dashboard/stats", "Dashboard Stats"),
        ("/api/test/dashboard/completo", "Dashboard Completo"),
        ("/api/test/usuarios", "Usuarios"),
        ("/api/test/instrumentos/estadisticas", "Instrumentos"),
        ("/api/test/alertas/activas", "Alertas"),
        ("/api/test/procedimientos/estadisticas", "Procedimientos"),
        ("/api/test/conteos", "Conteos"),
        ("/api/test/sets/activos", "Sets")
    ]
    
    results = {}
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        for endpoint, name in test_endpoints:
            print(f"\n🧪 Probando: {name}")
            print("-" * 40)
            
            try:
                response = await client.get(f"{base_url}{endpoint}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ {name}: ÉXITO")
                    print(f"   📊 Status Code: {response.status_code}")
                    print(f"   📊 Datos: {len(data) if isinstance(data, (list, dict)) else 'N/A'} elementos")
                    
                    if isinstance(data, dict) and 'success' in data:
                        print(f"   ✨ Success Flag: {data['success']}")
                    
                    results[name] = {
                        'status': 'success',
                        'status_code': response.status_code,
                        'data': data
                    }
                else:
                    print(f"❌ {name}: FALLO")
                    print(f"   📝 Status Code: {response.status_code}")
                    print(f"   📝 Response: {response.text}")
                    
                    results[name] = {
                        'status': 'error',
                        'status_code': response.status_code,
                        'error': response.text
                    }
                    
            except Exception as e:
                print(f"❌ {name}: ERROR")
                print(f"   📝 Excepción: {str(e)}")
                results[name] = {
                    'status': 'error',
                    'error': str(e)
                }
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS BÁSICAS")
    print("=" * 60)
    
    successful = sum(1 for r in results.values() if r['status'] == 'success')
    total = len(results)
    
    print(f"✅ Pruebas exitosas: {successful}/{total}")
    print(f"❌ Pruebas fallidas: {total - successful}/{total}")
    
    if successful == total:
        print("\n🎉 ¡Todas las pruebas básicas pasaron! El servidor está funcionando correctamente.")
    else:
        print(f"\n⚠️  {total - successful} pruebas fallaron. Revisar la configuración del servidor.")
    
    # Guardar resultados detallados
    try:
        with open("test_basic_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n📄 Resultados detallados guardados en: test_basic_results.json")
    except Exception as e:
        print(f"\n⚠️  No se pudieron guardar los resultados: {e}")
    
    return successful == total


async def test_server_status():
    """
    Verificar el estado del servidor
    """
    print("\n🌐 Verificando estado del servidor...")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Probar endpoint raíz
            response = await client.get(f"{base_url}/")
            print(f"✅ Servidor accesible: Status {response.status_code}")
            
            # Probar documentación
            docs_response = await client.get(f"{base_url}/docs")
            if docs_response.status_code == 200:
                print("✅ Documentación Swagger disponible")
            
            # Probar endpoint OpenAPI
            openapi_response = await client.get(f"{base_url}/openapi.json")
            if openapi_response.status_code == 200:
                openapi_data = openapi_response.json()
                print(f"✅ OpenAPI schema disponible: {len(openapi_data.get('paths', {}))} endpoints registrados")
            
            return True
            
    except Exception as e:
        print(f"❌ Error conectando al servidor: {e}")
        print("💡 Asegúrate de que el servidor esté ejecutándose en http://127.0.0.1:8000")
        return False


if __name__ == "__main__":
    print("🚀 EIVAI - Test Básico de Conectividad")
    print("=" * 60)
    
    try:
        # Verificar servidor
        server_ok = asyncio.run(test_server_status())
        
        if server_ok:
            # Ejecutar pruebas básicas
            success = asyncio.run(test_basic_endpoints())
            
            if success:
                print("\n🎊 ¡CONECTIVIDAD BÁSICA EXITOSA!")
                sys.exit(0)
            else:
                print("\n💥 Algunas pruebas básicas fallaron")
                sys.exit(1)
        else:
            print("\n💥 No se pudo conectar al servidor")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error crítico durante las pruebas: {e}")
        sys.exit(1)
