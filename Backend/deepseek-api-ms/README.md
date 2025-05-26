# EIVAI Assistant API Microservicio

Microservicio especializado de Asistente de IA para el Sistema de Gestión de Instrumental Quirúrgico EIVAI.

## Descripción

Este microservicio proporciona capacidades avanzadas de Inteligencia Artificial específicamente diseñadas para el Sistema EIVAI (Sistema de Gestión de Instrumental Quirúrgico). Utiliza la API de DeepSeek como motor subyacente para ofrecer funcionalidades inteligentes contextualizadas al dominio médico quirúrgico.

## Características Principales

### 🔍 Análisis de Conteos de Instrumentos
- Detección automática de discrepancias entre conteos inicial y final
- Evaluación de criticidad y riesgo para la seguridad del paciente
- Recomendaciones específicas para resolución de problemas
- Análisis contextual basado en tipo de cirugía

### 📊 Reportes Quirúrgicos Inteligentes
- Generación automática de reportes profesionales
- Análisis de calidad y métricas de seguridad
- Resúmenes ejecutivos con insights relevantes
- Documentación adecuada para expedientes médicos

### 💬 Consultas en Lenguaje Natural
- Respuestas a preguntas sobre instrumentos quirúrgicos
- Información sobre protocolos y procedimientos
- Orientación sobre mejores prácticas médicas
- Consultas sobre normativas de seguridad

### 📈 Análisis de Patrones de Uso
- Identificación de tendencias en uso de instrumentos
- Optimización de inventario quirúrgico
- Predicciones de demanda futura
- Recomendaciones de eficiencia operacional

### 🚨 Alertas Inteligentes
- Generación contextualizada de alertas críticas
- Notificaciones de mantenimiento y esterilización
- Alertas de cumplimiento normativo
- Avisos de seguridad del paciente

## Arquitectura del Sistema

El microservicio está estructurado en capas especializadas:

```
EIVAI Assistant API
├── Controladores EIVAI (eivai_controller.py)
├── Servicios Especializados (eivai_assistant_service.py)
├── Modelos de Dominio (eivai_models.py)
├── Rutas API (eivai_routes.py)
└── Servicio Base DeepSeek (deepseek_service.py)
```

## Funcionalidades por Contexto EIVAI

### Entidades del Sistema
- **Usuarios**: Instrumentadores quirúrgicos
- **Sets Quirúrgicos**: Conjuntos de instrumentos por especialidad
- **Instrumentos**: Herramientas quirúrgicas individuales
- **Procedimientos**: Cirugías con conteos de seguridad
- **Esterilización**: Ciclos de limpieza y esterilización
- **Alertas**: Notificaciones de seguridad y calidad

### Procesos Automatizados
1. **Conteo de Seguridad**: Verificación de instrumentos pre/post cirugía
2. **Trazabilidad**: Seguimiento completo del instrumental
3. **Control de Calidad**: Monitoreo de estándares de seguridad
4. **Auditoría**: Registro de todas las acciones del sistema

## Requisitos

- Python 3.9+
- FastAPI para API REST
- Pydantic para validación de datos
- DeepSeek API para procesamiento de IA
- Base de datos EIVAI (SQL Server)
- Docker (opcional, para despliegue en contenedor)

### Dependencias Específicas
- **Tenacity**: Para reintentos automáticos
- **SQLAlchemy**: Para integración con base de datos EIVAI
- **Pydantic**: Para modelos de dominio médico
- **FastAPI**: Para endpoints especializados

## Configuración

Todas las configuraciones se realizan mediante variables de entorno. Copia el archivo `.env.example` a `.env` y ajusta los valores según sea necesario.

### Variables de entorno requeridas

| Variable                   | Descripción                                      | Ejemplo                  |
|----------------------------|--------------------------------------------------|--------------------------|
| API_HOST                   | Host donde se ejecutará la API                   | 0.0.0.0                  |
| API_PUERTO                 | Puerto donde se ejecutará la API                 | 5003                     |
| NIVEL_LOG                  | Nivel de logging (DEBUG, INFO, WARNING, ERROR)   | INFO                     |
| DEFAULT_API_KEY            | API key para autenticación con este servicio     | eivai_assistant_key      |
| DEEPSEEK_API_KEY           | API key para autenticación con DeepSeek          | sk-abcd1234              |
| DEEPSEEK_API_URL           | URL base de la API de DeepSeek                   | https://api.deepseek.com |
| DEEPSEEK_MODELO            | Modelo de DeepSeek a utilizar                    | deepseek-chat            |
| TEMPERATURA_PREDETERMINADA | Temperatura por defecto para análisis médico     | 0.3                      |
| MAX_TOKENS_PREDETERMINADO  | Número máximo de tokens para respuestas médicas  | 800                      |
| REQUEST_TIMEOUT            | Timeout para las solicitudes en segundos         | 30                       |
| MAX_REINTENTOS             | Número máximo de reintentos para errores         | 3                        |
| TIEMPO_ENTRE_REINTENTOS    | Tiempo entre reintentos en segundos              | 2                        |

## Instalación y Ejecución

### Ejecución Local

1. Clona este repositorio
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura las variables de entorno (crea un archivo `.env` basado en `.env.example`)
4. Ejecuta la aplicación:
   ```bash
   python run.py
   ```
   o
   ```bash
   uvicorn src.api.app:app --host 0.0.0.0 --port 5003
   ```

### Ejecución con Docker

1. Configura las variables de entorno (crea un archivo `.env` basado en `.env.example`)
2. Construye y ejecuta con Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Uso de la API EIVAI

### Autenticación

Todas las solicitudes a la API (excepto `/salud` y `/`) requieren una API Key que debe enviarse en el encabezado `X-API-Key`.

### Endpoints Principales

#### Verificar Estado del Sistema EIVAI

```
GET /api/v1/eivai/estado
```

Ejemplo de respuesta:
```json
{
  "estado": "operativo",
  "mensaje": "EIVAI Assistant está funcionando correctamente",
  "sistema_eivai": {
    "sistema_activo": true,
    "version": "1.0.0",
    "funcionalidades_disponibles": [
      "Análisis de conteos de instrumentos",
      "Generación de reportes quirúrgicos",
      "Consultas en lenguaje natural",
      "Análisis de patrones de uso",
      "Alertas inteligentes"
    ]
  },
  "timestamp": "2025-05-26T10:30:00",
  "servicios_ia_activos": true
}
```

#### Analizar Conteos de Instrumentos

```
POST /api/v1/eivai/analizar-conteos
```

Ejemplo de solicitud:
```json
{
  "conteo_inicial": [
    {
      "instrumento_id": 1,
      "nombre_instrumento": "Bisturí #11",
      "codigo_instrumento": "BIS-011",
      "cantidad_esperada": 2,
      "cantidad_contada": 2
    },
    {
      "instrumento_id": 2,
      "nombre_instrumento": "Pinza Kelly",
      "codigo_instrumento": "PIN-KEL",
      "cantidad_esperada": 4,
      "cantidad_contada": 4
    }
  ],
  "conteo_final": [
    {
      "instrumento_id": 1,
      "nombre_instrumento": "Bisturí #11",
      "codigo_instrumento": "BIS-011",
      "cantidad_esperada": 2,
      "cantidad_contada": 1
    },
    {
      "instrumento_id": 2,
      "nombre_instrumento": "Pinza Kelly",
      "codigo_instrumento": "PIN-KEL",
      "cantidad_esperada": 4,
      "cantidad_contada": 4
    }
  ],
  "tipo_cirugia": "Laparoscopia",
  "procedimiento_id": 123,
  "incluir_recomendaciones": true
}
```

#### Generar Reporte Quirúrgico

```
POST /api/v1/eivai/generar-reporte
```

Ejemplo de solicitud:
```json
{
  "procedimiento_data": {
    "procedimiento_id": 123,
    "tipo_cirugia": "Colecistectomía Laparoscópica",
    "paciente": "Juan Pérez",
    "medico": "Dr. María García",
    "fecha_procedimiento": "2025-05-26T14:30:00",
    "estado_procedimiento": "FINALIZADO",
    "nombre_set": "Set Laparoscopia Básico",
    "usuario_responsable": "Enfermera Ana López",
    "conteo_inicial_completo": true,
    "conteo_final_completo": true
  },
  "incluir_recomendaciones": true,
  "incluir_analisis_detallado": true
}
```

#### Consulta en Lenguaje Natural

```
POST /api/v1/eivai/consulta-natural
```

Ejemplo de solicitud:
```json
{
  "consulta": "¿Qué instrumentos son esenciales para una cirugía de apendicectomía?",
  "incluir_referencias": true
}
```

#### Analizar Patrones de Uso

```
POST /api/v1/eivai/analizar-patrones
```

Ejemplo de solicitud:
```json
{
  "datos_historicos": [
    {
      "fecha": "2025-05-20",
      "instrumento_id": 1,
      "nombre_instrumento": "Bisturí #11",
      "tipo_procedimiento": "Laparoscopia",
      "cantidad_utilizada": 2
    }
  ],
  "periodo_analisis": "Últimos 30 días",
  "tipo_analisis": "uso_instrumentos"
}
```

#### Generar Alerta Inteligente

```
POST /api/v1/eivai/generar-alerta
```

Ejemplo de solicitud:
```json
{
  "tipo_alerta": "INSTRUMENTO_FALTANTE",
  "prioridad": "ALTA",
  "datos_contexto": {
    "instrumento_id": 1,
    "procedimiento_id": 123,
    "datos_adicionales": {
      "nombre_instrumento": "Bisturí #11",
      "cantidad_faltante": 1
    }
  },
  "requiere_accion_inmediata": true
}
```

## Ejemplos con cURL

### Verificar estado
```bash
curl -X GET http://localhost:5003/salud
```

### Procesar texto
```bash
curl -X POST http://localhost:5003/api/v1/procesar \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu_api_key" \
  -d '{
    "texto": "Traduce este texto al francés: 'Hola mundo'",
    "temperatura": 0.7
  }'
```

## Documentación

La documentación interactiva de la API está disponible en:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

Documentación adicional disponible en la carpeta `docs/`:
- [Ejemplos Detallados](docs/ejemplos_detallados.md): Ejemplos completos de uso e integración
- [Solución de Problemas](docs/solucion_problemas.md): Guía para solucionar problemas comunes
- [Arquitectura del Sistema](docs/arquitectura.md): Descripción de la arquitectura y componentes

## Mantenimiento y Operación

### Logs

Los logs se almacenan en el directorio `logs/` y también se muestran en la consola. El nivel de logging puede configurarse mediante la variable de entorno `NIVEL_LOG`.

### Monitoreo de salud

El servicio proporciona un endpoint `/salud` para verificar su estado. Este endpoint también se utiliza para el healthcheck de Docker.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.

---

© 2025 InklúAI - Todos los derechos reservados
