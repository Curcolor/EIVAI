# Microservicio de Detección YOLO

Microservicio especializado para la detección de instrumentos quirúrgicos usando YOLO (You Only Look Once) con Ultralytics.

## Características

- 🔍 **Detección en tiempo real** de instrumentos quirúrgicos
- 📊 **Conteo automático** por tipo de instrumento
- 🎯 **Alta precisión** con umbrales configurables
- 📸 **Múltiples formatos** de imagen soportados
- 🚀 **API RESTful** con FastAPI
- 📚 **Documentación automática** con Swagger/OpenAPI
- 🐋 **Containerizado** con Docker

## Instrumentos Detectados

| Código | Instrumento | Descripción |
|--------|-------------|-------------|
| BISP-001 | Bisturí #11 | Bisturí hoja número 11 |
| BISP-002 | Bisturí #15 | Bisturí hoja número 15 |
| PINZ-001 | Pinza Kelly | Pinza hemostática Kelly curva |
| PINZ-002 | Pinza Allis | Pinza de prensión Allis |
| TIJR-001 | Tijera Mayo | Tijera Mayo recta |
| TIJR-002 | Tijera Metzenbaum | Tijera Metzenbaum curva |
| PORT-001 | Portaagujas | Portaagujas Mayo-Hegar |
| SEPA-001 | Separador Farabeuf | Separador autoestático Farabeuf |
| ASPI-001 | Aspirador quirúrgico | Tubo de aspiración quirúrgica |
| GASA-001 | Gasas estériles | Paquete de gasas estériles 4x4 |

## Instalación

### Opción 1: Usando Docker (Recomendado)

```bash
# Construir imagen
docker build -t yolo-detection-ms .

# Ejecutar contenedor
docker run -p 8002:8002 yolo-detection-ms
```

### Opción 2: Instalación local

```bash
# Clonar repositorio
git clone <repository-url>
cd yolo-detection-ms

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Ejecutar aplicación
python run.py
```

### Opción 3: Script automático

```bash
# Dar permisos de ejecución (Linux/Mac)
chmod +x configurar_entorno.sh

# Ejecutar script
./configurar_entorno.sh
```

## Uso de la API

### Detectar instrumentos

```bash
curl -X POST "http://localhost:8002/api/v1/yolo/detect" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@imagen_instrumentos.jpg" \
     -F "confidence_threshold=0.5" \
     -F "iou_threshold=0.45"
```

### Respuesta de ejemplo

```json
{
  "success": true,
  "total_objects": 5,
  "detections": [
    {
      "id": 1,
      "class_id": 0,
      "confidence": 0.85,
      "bbox": {
        "x1": 100.5,
        "y1": 200.3,
        "x2": 150.7,
        "y2": 250.8
      },
      "instrument": {
        "codigo": "BISP-001",
        "nombre": "Bisturí #11",
        "descripcion": "Bisturí hoja número 11"
      }
    }
  ],
  "summary": {
    "BISP-001": {
      "nombre": "Bisturí #11",
      "descripcion": "Bisturí hoja número 11",
      "cantidad": 2,
      "confianza_promedio": 0.85
    },
    "PINZ-001": {
      "nombre": "Pinza Kelly",
      "descripcion": "Pinza hemostática Kelly curva",
      "cantidad": 3,
      "confianza_promedio": 0.78
    }
  },
  "confidence_threshold": 0.5,
  "iou_threshold": 0.45,
  "file_info": {
    "filename": "imagen_instrumentos.jpg",
    "content_type": "image/jpeg",
    "size": 1024000
  }
}
```

## Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/yolo/detect` | Detectar instrumentos en imagen |
| GET | `/api/v1/yolo/model/info` | Información del modelo |
| GET | `/api/v1/yolo/instruments` | Lista de instrumentos soportados |
| GET | `/api/v1/yolo/health` | Estado del servicio |
| GET | `/docs` | Documentación Swagger |
| GET | `/redoc` | Documentación ReDoc |

## Configuración

### Variables de entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `HOST` | Host del servidor | `0.0.0.0` |
| `PORT` | Puerto del servidor | `8002` |
| `DEBUG` | Modo debug | `False` |
| `YOLO_MODEL_PATH` | Ruta del modelo YOLO | `yolov8n.pt` |
| `CONFIDENCE_THRESHOLD` | Umbral de confianza | `0.5` |
| `IOU_THRESHOLD` | Umbral de IoU | `0.45` |
| `UPLOAD_DIR` | Directorio temporal | `temp_uploads` |
| `MAX_FILE_SIZE` | Tamaño máximo archivo | `10485760` (10MB) |

### Formatos de imagen soportados

- JPG/JPEG
- PNG
- BMP
- TIFF
- WEBP

## Desarrollo

### Estructura del proyecto

```
yolo-detection-ms/
├── src/
│   ├── api/
│   │   ├── app.py              # Aplicación FastAPI
│   │   ├── controllers/        # Controladores
│   │   └── routes/             # Rutas de la API
│   ├── config/
│   │   └── settings.py         # Configuración
│   └── services/
│       └── yolo_service.py     # Servicio YOLO
├── requirements.txt            # Dependencias Python
├── Dockerfile                  # Imagen Docker
├── run.py                     # Punto de entrada
└── README.md                  # Este archivo
```

### Personalización del modelo

Para usar un modelo personalizado:

1. Entrena tu modelo YOLO con tus propios datos
2. Guarda el modelo entrenado (archivo `.pt`)
3. Actualiza `YOLO_MODEL_PATH` en la configuración
4. Modifica `SURGICAL_INSTRUMENTS_MAP` en `settings.py`

### Testing

```bash
# Ejecutar tests
pytest tests/

# Con cobertura
pytest tests/ --cov=src
```

## Despliegue

### Docker Compose

```yaml
version: '3.8'
services:
  yolo-detection:
    build: .
    ports:
      - "8002:8002"
    environment:
      - DEBUG=False
      - CONFIDENCE_THRESHOLD=0.6
    volumes:
      - ./models:/app/models
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yolo-detection-ms
spec:
  replicas: 2
  selector:
    matchLabels:
      app: yolo-detection-ms
  template:
    metadata:
      labels:
        app: yolo-detection-ms
    spec:
      containers:
      - name: yolo-detection-ms
        image: yolo-detection-ms:latest
        ports:
        - containerPort: 8002
```

## Solución de problemas

### Error: Modelo no encontrado

```bash
# Descargar modelo manualmente
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Error: Memoria insuficiente

- Reducir el tamaño de imagen antes del procesamiento
- Usar un modelo más pequeño (yolov8n en lugar de yolov8x)
- Ajustar los workers de uvicorn

### Error: Archivo demasiado grande

- Ajustar `MAX_FILE_SIZE` en la configuración
- Comprimir imágenes antes del envío

## Contribución

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

MIT License - ver archivo LICENSE para detalles

## Contacto

- **Equipo de Desarrollo**: desarrollo@eivai.com
- **Documentación**: [docs.eivai.com](https://docs.eivai.com)
- **Issues**: [GitHub Issues](https://github.com/eivai/yolo-detection-ms/issues)
