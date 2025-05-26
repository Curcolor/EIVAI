# Multi-stage build para optimizar tamaño
FROM python:3.10-slim AS builder

WORKDIR /app

# Instalar herramientas de construcción
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

# Copiar archivos de requisitos primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instalar dependencias en un entorno virtual
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Segunda etapa: imagen final
FROM python:3.10-slim

LABEL maintainer="InklúAI Team <info@inkluai.com>"
LABEL description="Microservicio de procesamiento de texto usando la API de DeepSeek"

# Copiar el entorno virtual desde la etapa anterior
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# Instalar herramientas necesarias para el healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar el código de la aplicación
COPY . .

# Crear directorio de logs
RUN mkdir -p logs

# Configurar variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Exponer el puerto (será sobreescrito por la variable de entorno)
EXPOSE 5003

# Configurar healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${API_PUERTO}/salud || exit 1

# Comando para ejecutar la aplicación
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "${API_PUERTO}"]
