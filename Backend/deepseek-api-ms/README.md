# DeepSeek API Microservicio

Microservicio modular que consume la API de DeepSeek para procesamiento de texto utilizando FastAPI.

## Descripción

Este microservicio proporciona una interfaz web para procesar texto utilizando la API de DeepSeek. Permite enviar texto para su procesamiento y recibir respuestas generadas por los modelos de lenguaje de DeepSeek.

## Características

- Procesamiento de texto usando modelos de DeepSeek
- Configuración completa mediante variables de entorno
- Autenticación mediante API Key
- Manejo de errores y reintentos automáticos
- Logging detallado
- Documentación automática con Swagger UI
- Contenerización con Docker

## Requisitos

- Python 3.9+
- FastAPI
- Pydantic
- Python-dotenv
- Requests
- Tenacity (para reintentos)
- Docker (opcional, para despliegue en contenedor)

## Configuración

Todas las configuraciones se realizan mediante variables de entorno. Copia el archivo `.env.example` a `.env` y ajusta los valores según sea necesario.

### Variables de entorno requeridas

| Variable                   | Descripción                                      | Ejemplo                  |
|----------------------------|--------------------------------------------------|--------------------------|
| API_HOST                   | Host donde se ejecutará la API                   | 0.0.0.0                  |
| API_PUERTO                 | Puerto donde se ejecutará la API                 | 5003                     |
| NIVEL_LOG                  | Nivel de logging (DEBUG, INFO, WARNING, ERROR)   | INFO                     |
| DEFAULT_API_KEY            | API key para autenticación con este servicio     | mi_clave_secreta         |
| DEEPSEEK_API_KEY           | API key para autenticación con DeepSeek          | sk-abcd1234              |
| DEEPSEEK_API_URL           | URL base de la API de DeepSeek                   | https://api.deepseek.com |
| DEEPSEEK_MODELO            | Modelo de DeepSeek a utilizar                    | deepseek-chat            |
| TEMPERATURA_PREDETERMINADA | Temperatura por defecto (0.0 a 1.0)              | 0.7                      |
| MAX_TOKENS_PREDETERMINADO  | Número máximo de tokens a generar por defecto    | 200                      |
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

## Uso de la API

### Autenticación

Todas las solicitudes a la API (excepto `/salud` y `/`) requieren una API Key que debe enviarse en el encabezado `X-API-Key`.

### Endpoints

#### Verificar Estado del Servicio

```
GET /salud
```

Ejemplo de respuesta:
```json
{
  "estado": "operativo"
}
```

#### Información del Servicio

```
GET /
```

#### Verificar Estado de DeepSeek

```
GET /api/v1/estado
```

Ejemplo de respuesta:
```json
{
  "estado": "operativo",
  "mensaje": "El servicio de procesamiento de texto con DeepSeek está funcionando correctamente",
  "modelo_predeterminado": "deepseek-chat",
  "timestamp": 1621234567.89
}
```

#### Procesar Texto

```
POST /api/v1/procesar
```

Cabecera requerida:
```
X-API-Key: tu_api_key
```

Cuerpo de la solicitud:
```json
{
  "texto": "Traduce este texto al francés: 'Hola mundo'",
  "temperatura": 0.7,
  "max_tokens": 100,
  "modelo": "deepseek-chat"
}
```

Parámetros opcionales:
- `temperatura`: Nivel de aleatoriedad (0.0 a 1.0)
- `max_tokens`: Número máximo de tokens a generar
- `modelo`: Modelo específico de DeepSeek a utilizar

Ejemplo de respuesta:
```json
{
  "texto_procesado": "Bonjour le monde",
  "modelo_usado": "deepseek-chat",
  "tokens_entrada": 12,
  "tokens_salida": 3,
  "tiempo_proceso": 0.856
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
