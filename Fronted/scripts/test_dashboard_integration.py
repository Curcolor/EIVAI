#!/usr/bin/env python3
"""
Script de prueba para verificar la integración del dashboard
Prueba todos los endpoints disponibles y muestra los resultados
"""
import asyncio
import sys
import json
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from api.frontend_services.main_service import FrontendAPIService


async def test_dashboard_integration():
    """
    Probar la integración completa del dashboard
    """
    print("🔧 Iniciando pruebas de integración del dashboard...")
    print("=" * 60)
    
    # Inicializar el servicio principal
    api_service = FrontendAPIService()    # Lista de pruebas a ejecutar
    tests = [
        ("Dashboard Completo", api_service.obtener_datos_dashboard_completo),
        ("Usuarios", lambda: api_service.usuarios.obtener_usuarios(limit=10)),
        ("Instrumentos Estadísticas", api_service.instrumentos.obtener_estadisticas_uso),
        ("Alertas Activas", lambda: api_service.alertas.obtener_alertas_activas(limit=5)),
        ("Conteos", lambda: api_service.conteos.obtener_conteos(limit=5)),
        ("Sets Activos", api_service.sets.obtener_sets_activos),
        ("Procedimientos Estadísticas", api_service.procedimientos.obtener_estadisticas_procedimientos)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🧪 Probando: {test_name}")
        print("-" * 40)
        
        try:
            result = await test_func()
            
            if isinstance(result, dict) and 'success' in result:
                if result['success']:
                    print(f"✅ {test_name}: ÉXITO")
                    if 'data' in result:
                        print(f"   📊 Datos: {len(result['data']) if isinstance(result['data'], (list, dict)) else 'N/A'} elementos")
                else:
                    print(f"❌ {test_name}: FALLO")
                    print(f"   📝 Error: {result.get('message', 'Sin mensaje')}")
            else:
                print(f"✅ {test_name}: ÉXITO (formato directo)")
                print(f"   📊 Datos: {len(result) if isinstance(result, (list, dict)) else 'N/A'} elementos")
            
            results[test_name] = {
                'status': 'success',
                'data': result
            }
            
        except Exception as e:
            print(f"❌ {test_name}: ERROR")
            print(f"   📝 Excepción: {str(e)}")
            results[test_name] = {
                'status': 'error',
                'error': str(e)
            }
    
    # Resumen de resultados
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    successful = sum(1 for r in results.values() if r['status'] == 'success')
    total = len(results)
    
    print(f"✅ Pruebas exitosas: {successful}/{total}")
    print(f"❌ Pruebas fallidas: {total - successful}/{total}")
    
    if successful == total:
        print("\n🎉 ¡Todas las pruebas pasaron! La integración está funcionando correctamente.")
    else:
        print(f"\n⚠️  {total - successful} pruebas fallaron. Revisar la configuración.")
    
    # Guardar resultados detallados
    try:
        with open("test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n📄 Resultados detallados guardados en: test_results.json")
    except Exception as e:
        print(f"\n⚠️  No se pudieron guardar los resultados: {e}")
    
    return successful == total


async def test_specific_endpoints():
    """
    Probar endpoints específicos del dashboard
    """
    print("\n🎯 Probando endpoints específicos del dashboard...")
    print("=" * 60)
    
    api_service = FrontendAPIService()
    
    # Probar endpoint del dashboard
    try:
        print("🧪 Probando Dashboard Service...")
        dashboard_stats = await api_service.dashboard.obtener_estadisticas_dashboard()
        print(f"✅ Dashboard Stats: {json.dumps(dashboard_stats, indent=2, default=str)}")
        
        print("\n🧪 Probando Dashboard Completo...")
        dashboard_completo = await api_service.dashboard.obtener_dashboard_completo()
        print(f"✅ Dashboard Completo: {json.dumps(dashboard_completo, indent=2, default=str)}")
        
    except Exception as e:
        print(f"❌ Error en dashboard endpoints: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("🚀 EIVAI - Test de Integración del Dashboard")
    print("=" * 60)
    
    try:
        # Ejecutar pruebas principales
        success1 = asyncio.run(test_dashboard_integration())
        
        # Ejecutar pruebas específicas
        success2 = asyncio.run(test_specific_endpoints())
        
        if success1 and success2:
            print("\n🎊 ¡INTEGRACIÓN COMPLETAMENTE EXITOSA!")
            sys.exit(0)
        else:
            print("\n💥 Algunas pruebas fallaron")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error crítico durante las pruebas: {e}")
        sys.exit(1)
