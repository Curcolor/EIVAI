"""
Script de ejemplo para probar el microservicio YOLO Detection
Versión: 1.0
Fecha: 26/05/2025
"""

import requests
import json
from pathlib import Path

# Configuración
API_BASE_URL = "http://localhost:8002"
API_VERSION = "/api/v1/yolo"

def test_health_check():
    """Probar el health check del servicio"""
    print("🔍 Probando health check...")
    
    try:
        response = requests.get(f"{API_BASE_URL}{API_VERSION}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_model_info():
    """Probar obtención de información del modelo"""
    print("\n📋 Probando información del modelo...")
    
    try:
        response = requests.get(f"{API_BASE_URL}{API_VERSION}/model/info")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_instruments():
    """Probar obtención de instrumentos soportados"""
    print("\n🔧 Probando instrumentos soportados...")
    
    try:
        response = requests.get(f"{API_BASE_URL}{API_VERSION}/instruments")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Total instrumentos: {data.get('total_instruments', 0)}")
        
        # Mostrar algunos instrumentos
        instruments = data.get('supported_instruments', {})
        print("\nAlgunos instrumentos soportados:")
        for key, instrument in list(instruments.items())[:3]:
            print(f"  - {instrument['codigo']}: {instrument['nombre']}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_detect_with_sample_image():
    """Probar detección con imagen de muestra"""
    print("\n🖼️ Probando detección con imagen de muestra...")
    
    # Crear imagen de muestra
    from PIL import Image
    import tempfile
    import os
    
    # Crear imagen RGB simple
    img = Image.new('RGB', (640, 480), color='white')
    
    # Guardar en archivo temporal
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        img.save(tmp.name, 'JPEG')
        temp_image_path = tmp.name
    
    try:
        # Abrir imagen y enviar
        with open(temp_image_path, 'rb') as img_file:
            files = {
                'file': ('test_image.jpg', img_file, 'image/jpeg')
            }
            
            # Parámetros opcionales
            params = {
                'confidence_threshold': 0.5,
                'iou_threshold': 0.45
            }
            
            response = requests.post(
                f"{API_BASE_URL}{API_VERSION}/detect",
                files=files,
                params=params
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Objetos detectados: {data.get('total_objects', 0)}")
                
                # Mostrar resumen si hay detecciones
                summary = data.get('summary', {})
                if summary:
                    print("\nResumen de detecciones:")
                    for codigo, info in summary.items():
                        print(f"  - {info['nombre']}: {info['cantidad']} unidades")
                else:
                    print("No se detectaron instrumentos en la imagen de muestra")
                
                return True
            else:
                print(f"Error: {response.text}")
                return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Limpiar archivo temporal
        if os.path.exists(temp_image_path):
            os.unlink(temp_image_path)

def test_api_documentation():
    """Probar acceso a documentación de la API"""
    print("\n📚 Probando documentación de la API...")
    
    try:
        # Probar OpenAPI JSON
        response = requests.get(f"{API_BASE_URL}/openapi.json")
        print(f"OpenAPI JSON Status: {response.status_code}")
        
        # Probar Swagger UI
        response = requests.get(f"{API_BASE_URL}/docs")
        print(f"Swagger UI Status: {response.status_code}")
        
        # Probar ReDoc
        response = requests.get(f"{API_BASE_URL}/redoc")
        print(f"ReDoc Status: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal para ejecutar todas las pruebas"""
    print("🚀 Iniciando pruebas del microservicio YOLO Detection")
    print("=" * 60)
    
    # Lista de pruebas
    tests = [
        ("Health Check", test_health_check),
        ("Model Info", test_get_model_info),
        ("Supported Instruments", test_get_instruments),
        ("Image Detection", test_detect_with_sample_image),
        ("API Documentation", test_api_documentation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))
        
        if success:
            print(f"✅ {test_name}: EXITOSO")
        else:
            print(f"❌ {test_name}: FALLIDO")
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print(f"\nResultado: {passed}/{total} pruebas exitosas")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! El microservicio está funcionando correctamente.")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la configuración del servicio.")
    
    return passed == total

if __name__ == "__main__":
    # Información de uso
    print("Microservicio YOLO Detection - Script de Prueba")
    print("Asegúrate de que el servicio esté ejecutándose en http://localhost:8002")
    print("Para iniciar el servicio: python run.py")
    print()
    
    success = main()
    exit(0 if success else 1)
