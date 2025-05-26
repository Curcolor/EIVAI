#!/usr/bin/env python3
"""
Test simplificado para verificar la estructura del proyecto EIVAI
"""
import os
import sys

def test_file_exists(file_path, description):
    """Verificar si un archivo existe"""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✅ {description}")
        print(f"   📄 {file_path} ({size} bytes)")
        return True
    else:
        print(f"❌ {description}")
        print(f"   📄 {file_path} - NO ENCONTRADO")
        return False

def test_html_content(file_path):
    """Verificar contenido del archivo HTML"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar IDs importantes
        required_ids = [
            'estadisticas-generales',
            'alertas-section', 
            'instrumentos-section',
            'procedimientos-section',
            'refresh-dashboard'
        ]
        
        found_ids = []
        missing_ids = []
        
        for req_id in required_ids:
            if f'id="{req_id}"' in content:
                found_ids.append(req_id)
            else:
                missing_ids.append(req_id)
        
        print(f"   📋 IDs encontrados: {len(found_ids)}/{len(required_ids)}")
        for found_id in found_ids:
            print(f"      ✅ {found_id}")
        
        if missing_ids:
            for missing_id in missing_ids:
                print(f"      ❌ {missing_id}")
        
        return len(missing_ids) == 0
        
    except Exception as e:
        print(f"   ❌ Error leyendo archivo: {e}")
        return False

def test_js_content(file_path):
    """Verificar contenido del archivo JavaScript"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar clases y funciones importantes
        required_elements = [
            'class EIVAIDashboard',
            'loadInitialData',
            'updateStats',
            'updateAlertas',
            'updateInstrumentos'
        ]
        
        found_elements = []
        missing_elements = []
        
        for element in required_elements:
            if element in content:
                found_elements.append(element)
            else:
                missing_elements.append(element)
        
        print(f"   📋 Elementos JavaScript encontrados: {len(found_elements)}/{len(required_elements)}")
        for found_element in found_elements:
            print(f"      ✅ {found_element}")
        
        if missing_elements:
            for missing_element in missing_elements:
                print(f"      ❌ {missing_element}")
        
        return len(missing_elements) == 0
        
    except Exception as e:
        print(f"   ❌ Error leyendo archivo: {e}")
        return False

def main():
    """Ejecutar tests de verificación"""
    print("🚀 EIVAI - Test de Verificación del Sistema")
    print("=" * 60)
    
    # Cambiar al directorio del proyecto
    project_dir = r"c:\Users\SemilleroTI\Desktop\Hackathon\EIVAI\Fronted"
    if os.path.exists(project_dir):
        os.chdir(project_dir)
        print(f"📁 Directorio de trabajo: {os.getcwd()}")
    else:
        print(f"❌ Directorio del proyecto no encontrado: {project_dir}")
        return False
    
    tests_passed = 0
    total_tests = 0
    
    print("\n🔍 1. VERIFICACIÓN DE ARCHIVOS PRINCIPALES")
    print("-" * 50)
    
    # Test 1: Archivos principales
    files_to_test = [
        ("src/templates/index.html", "Template principal del dashboard"),
        ("src/static/js/dashboard.js", "JavaScript del dashboard"),
        ("src/static/css/dashboard-integration.css", "CSS de integración"),
        ("src/api/app.py", "Aplicación FastAPI principal"),
        ("run.py", "Script de ejecución del servidor")
    ]
    
    for file_path, description in files_to_test:
        total_tests += 1
        if test_file_exists(file_path, description):
            tests_passed += 1
    
    print("\n🔍 2. VERIFICACIÓN DEL TEMPLATE HTML")
    print("-" * 50)
    total_tests += 1
    if test_html_content("src/templates/index.html"):
        tests_passed += 1
        print("✅ Template HTML tiene todos los IDs necesarios")
    else:
        print("❌ Template HTML falta algunos IDs necesarios")
    
    print("\n🔍 3. VERIFICACIÓN DEL JAVASCRIPT")
    print("-" * 50)
    total_tests += 1
    if test_js_content("src/static/js/dashboard.js"):
        tests_passed += 1
        print("✅ JavaScript del dashboard tiene todas las funciones necesarias")
    else:
        print("❌ JavaScript del dashboard falta algunas funciones")
    
    print("\n🔍 4. VERIFICACIÓN DE SERVICIOS FRONTEND")
    print("-" * 50)
    
    service_files = [
        "src/api/frontend_services/main_service.py",
        "src/api/frontend_services/dashboard_service.py",
        "src/api/frontend_services/usuario_service.py",
        "src/api/frontend_services/instrumento_service.py"
    ]
    
    for service_file in service_files:
        total_tests += 1
        if test_file_exists(service_file, f"Servicio {os.path.basename(service_file)}"):
            tests_passed += 1
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    print(f"Tests ejecutados: {total_tests}")
    print(f"Tests exitosos: {tests_passed}")
    print(f"Tests fallidos: {total_tests - tests_passed}")
    print(f"Tasa de éxito: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ El sistema está correctamente estructurado")
        print("✅ Todos los archivos necesarios están presentes")
        print("✅ El dashboard tiene la integración completa")
        
        print("\n📋 SIGUIENTES PASOS:")
        print("1. Iniciar el servidor: python run.py")
        print("2. Abrir navegador: http://127.0.0.1:8000")
        print("3. Verificar dashboard en funcionamiento")
        
        return True
    else:
        print(f"\n⚠️ {total_tests - tests_passed} TESTS FALLARON")
        print("🔧 Revisar los archivos faltantes o con errores arriba")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'='*60}")
    if success:
        print("🚀 Sistema listo para pruebas!")
    else:
        print("🔧 Correcciones necesarias antes de continuar")
