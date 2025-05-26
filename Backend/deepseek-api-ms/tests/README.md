# Tests para DeepSeek API Microservicio

Este directorio contiene las pruebas unitarias y de integración para el microservicio de DeepSeek API.

## Estructura de Directorios

```
tests/
├── __init__.py          # Inicialización del paquete de tests
├── conftest.py          # Configuración general para pytest
├── integration/         # Tests de integración para probar la API completa
└── unit/                # Tests unitarios para componentes individuales
```

## Requisitos

Para ejecutar las pruebas, necesitas instalar las dependencias de desarrollo:

```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

## Ejecución de Pruebas

### Ejecutar todas las pruebas

```bash
pytest
```

### Ejecutar solo pruebas unitarias

```bash
pytest tests/unit/
```

### Ejecutar solo pruebas de integración

```bash
pytest tests/integration/
```

### Ejecutar con cobertura de código

```bash
pytest --cov=src
```

### Generar informe de cobertura HTML

```bash
pytest --cov=src --cov-report=html
```

El informe HTML se generará en el directorio `htmlcov/`.

## Configuración de Pruebas

Las pruebas utilizan variables de entorno simuladas definidas en `conftest.py`. Para las pruebas de integración, se utiliza `TestClient` de FastAPI para simular las solicitudes HTTP sin necesidad de un servidor real.

Para las pruebas que involucran la API de DeepSeek, se utilizan mocks para evitar realizar llamadas reales a la API durante las pruebas.

## Convenciones de Nombrado

- Los archivos de prueba comienzan con `test_`.
- Las clases de prueba comienzan con `Test`.
- Los métodos de prueba comienzan con `test_`.

## Añadir Nuevas Pruebas

Al añadir nuevas funcionalidades al microservicio, es recomendable agregar las pruebas correspondientes:

1. Para componentes individuales, añadir pruebas unitarias en el directorio `unit/`.
2. Para endpoints de la API, añadir pruebas de integración en el directorio `integration/`.

---

© 2025 InklúAI - Todos los derechos reservados
