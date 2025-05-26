#!/usr/bin/env python3
"""
Script de prueba final para verificar la integración completa del dashboard EIVAI
"""
import asyncio
import aiohttp
import json
from datetime import datetime
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DashboardIntegrationTester:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"
        self.session = None
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
    
    async def setup(self):
        """Configurar la sesión HTTP"""
        self.session = aiohttp.ClientSession()
    
    async def cleanup(self):
        """Limpiar recursos"""
        if self.session:
            await self.session.close()
    
    async def test_endpoint(self, endpoint, description):
        """Probar un endpoint específico"""
        try:
            print(f"🔍 Probando: {description}")
            print(f"   URL: {self.base_url}{endpoint}")
            
            async with self.session.get(f"{self.base_url}{endpoint}") as response:
                status = response.status
                
                if status == 200:
                    data = await response.json()
                    print(f"   ✅ Estado: {status} - Respuesta válida")
                    print(f"   📊 Datos recibidos: {len(str(data))} caracteres")
                    self.test_results['passed'] += 1
                    return True, data
                else:
                    error_text = await response.text()
                    print(f"   ❌ Estado: {status}")
                    print(f"   📝 Error: {error_text[:200]}...")
                    self.test_results['failed'] += 1
                    self.test_results['errors'].append(f"{endpoint}: {status} - {error_text[:100]}")
                    return False, None
                      except Exception as e:
            print(f"   💥 Excepción: {str(e)}")
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"{endpoint}: Exception - {str(e)}")
            return False, None
    
    async def test_dashboard_complete(self):
        """Probar el endpoint completo del dashboard"""
        print("\n" + "="*80)
        print("🚀 PRUEBA DE INTEGRACIÓN COMPLETA DEL DASHBOARD EIVAI")
        print("="*80)
        
        success, data = await self.test_endpoint(
            "/api/test/dashboard/completo",
            "Dashboard completo (datos integrados)"
        )
        
        if success and data:
            print("\n📋 ANÁLISIS DE DATOS RECIBIDOS:")
            print("-" * 40)
            
            # Verificar estructura de datos
            expected_keys = [
                'stats_generales', 'alertas', 'instrumentos', 
                'procedimientos', 'conteos_recientes', 'sets_quirurgicos'
            ]
            
            for key in expected_keys:
                if key in data:
                    print(f"   ✅ {key}: Presente")
                    if isinstance(data[key], dict):
                        print(f"      📊 Tipo: Objeto con {len(data[key])} campos")
                    elif isinstance(data[key], list):
                        print(f"      📊 Tipo: Lista con {len(data[key])} elementos")
                    else:
                        print(f"      📊 Tipo: {type(data[key]).__name__}")
                else:
                    print(f"   ❌ {key}: Faltante")
            
            return True
        return False
    
    async def test_individual_endpoints(self):
        """Probar endpoints individuales"""
        print("\n" + "="*80)
        print("🔧 PRUEBA DE ENDPOINTS INDIVIDUALES")
        print("="*80)
          endpoints = [
            ("/api/test/dashboard/stats", "Estadísticas generales del dashboard"),
            ("/api/test/alertas/activas", "Alertas activas del sistema"),
            ("/api/test/instrumentos/estadisticas", "Estadísticas de instrumentos"),
            ("/api/test/procedimientos/estadisticas", "Estadísticas de procedimientos"),
            ("/api/test/conteos", "Conteos recientes"),
            ("/api/test/sets/activos", "Sets quirúrgicos activos"),
        ]
        
        individual_results = []
        for endpoint, description in endpoints:
            success, data = await self.test_endpoint(endpoint, description)
            individual_results.append((endpoint, success, data))
            await asyncio.sleep(0.5)  # Pequeña pausa entre requests
        
        return individual_results
    
    async def test_static_files(self):
        """Probar acceso a archivos estáticos"""
        print("\n" + "="*80)
        print("📁 PRUEBA DE ARCHIVOS ESTÁTICOS")
        print("="*80)
        
        static_files = [
            ("/static/js/dashboard.js", "JavaScript del dashboard"),
            ("/static/css/dashboard-integration.css", "CSS de integración"),
            ("/", "Página principal (dashboard)")
        ]
        
        for file_path, description in static_files:
            try:
                async with self.session.get(f"{self.base_url}{file_path}") as response:
                    if response.status == 200:
                        content_length = len(await response.text())
                        print(f"   ✅ {description}: {content_length} caracteres")
                        self.test_results['passed'] += 1
                    else:
                        print(f"   ❌ {description}: Estado {response.status}")
                        self.test_results['failed'] += 1
            except Exception as e:
                print(f"   💥 {description}: {str(e)}")
                self.test_results['failed'] += 1
    
    async def run_complete_test(self):
        """Ejecutar todas las pruebas"""
        start_time = datetime.now()
        
        try:
            await self.setup()
            
            print("🏥 EIVAI - Sistema de Identificación de Herramientas Quirúrgicas")
            print(f"⏰ Iniciando pruebas: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"🌐 Servidor: {self.base_url}")
            
            # Probar conectividad básica
            print("\n🔗 Verificando conectividad con el servidor...")
            try:
                async with self.session.get(f"{self.base_url}/docs") as response:
                    if response.status == 200:
                        print("   ✅ Servidor respondiendo correctamente")
                    else:
                        print(f"   ⚠️ Servidor responde con estado: {response.status}")
            except Exception as e:
                print(f"   ❌ Error de conectividad: {str(e)}")
                print("   💡 Asegúrate de que el servidor esté ejecutándose en el puerto 8000")
                return
            
            # Ejecutar pruebas principales
            await self.test_dashboard_complete()
            await self.test_individual_endpoints()
            await self.test_static_files()
            
            # Mostrar resumen final
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print("\n" + "="*80)
            print("📊 RESUMEN DE RESULTADOS")
            print("="*80)
            print(f"⏱️ Duración: {duration:.2f} segundos")
            print(f"✅ Pruebas exitosas: {self.test_results['passed']}")
            print(f"❌ Pruebas fallidas: {self.test_results['failed']}")
            print(f"📈 Tasa de éxito: {(self.test_results['passed']/(self.test_results['passed']+self.test_results['failed'])*100):.1f}%")
            
            if self.test_results['errors']:
                print(f"\n🚨 ERRORES ENCONTRADOS ({len(self.test_results['errors'])}):")
                print("-" * 40)
                for i, error in enumerate(self.test_results['errors'], 1):
                    print(f"   {i}. {error}")
            
            if self.test_results['failed'] == 0:
                print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
                print("💚 El dashboard está listo para uso en producción")
            else:
                print(f"\n⚠️ {self.test_results['failed']} pruebas fallaron")
                print("🔧 Revisa los errores arriba para resolver problemas")
            
        except Exception as e:
            print(f"\n💥 Error crítico durante las pruebas: {str(e)}")
        finally:
            await self.cleanup()

async def main():
    """Función principal"""
    tester = DashboardIntegrationTester()
    await tester.run_complete_test()

if __name__ == "__main__":
    asyncio.run(main())
