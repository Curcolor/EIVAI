# Solución de Problemas - DeepSeek API

Este documento proporciona información para solucionar problemas comunes que pueden surgir al utilizar el microservicio DeepSeek API.

## Tabla de Contenidos

- [Problemas de Conexión](#problemas-de-conexión)
- [Errores de Autenticación](#errores-de-autenticación)
- [Problemas con la API de DeepSeek](#problemas-con-la-api-de-deepseek)
- [Errores en la Configuración](#errores-en-la-configuración)
- [Problemas de Docker](#problemas-de-docker)
- [Logs y Depuración](#logs-y-depuración)
- [Preguntas Frecuentes](#preguntas-frecuentes)

## Problemas de Conexión

### El servicio no responde

**Síntoma**: No puedes conectarte al servicio o recibes errores de conexión rechazada.

**Soluciones**:

1. Verifica que el servicio esté ejecutándose:
   ```bash
   ps aux | grep uvicorn
   ```

2. Comprueba que el puerto configurado esté disponible y no bloqueado por un firewall:
   ```bash
   netstat -tuln | grep <puerto>
   ```

3. Verifica que estás usando la dirección correcta (host:puerto).

### Timeouts frecuentes

**Síntoma**: Las solicitudes a la API tardan mucho tiempo o fallan con timeout.

**Soluciones**:

1. Aumenta el valor de `REQUEST_TIMEOUT` en las variables de entorno.
2. Verifica la conectividad con la API de DeepSeek:
   ```bash
   curl -v https://api.deepseek.com/v1/health
   ```
3. Comprueba si hay problemas de red o proxies que puedan estar afectando la conexión.

## Errores de Autenticación

### Error 401 No Autorizado

**Síntoma**: Recibes un error 401 al intentar usar la API.

**Soluciones**:

1. Asegúrate de incluir el encabezado `X-API-Key` en todas las solicitudes.
2. Verifica que la API Key coincide con la configurada en `DEFAULT_API_KEY`.
3. Comprueba que no hay espacios adicionales o caracteres invisibles en la API Key.

### Error 403 Prohibido

**Síntoma**: Recibes un error 403 al intentar usar la API.

**Soluciones**:

1. Verifica que la API Key proporcionada es válida y coincide exactamente con la configurada.
2. Comprueba los logs del servicio para ver detalles adicionales sobre el error.

## Problemas con la API de DeepSeek

### Error al conectar con DeepSeek

**Síntoma**: El servicio devuelve errores relacionados con la API de DeepSeek.

**Soluciones**:

1. Verifica que `DEEPSEEK_API_KEY` es válida:
   ```bash
   curl -H "Authorization: Bearer tu_api_key" https://api.deepseek.com/v1/models
   ```

2. Comprueba que `DEEPSEEK_API_URL` apunta a la URL correcta.

3. Verifica si la API de DeepSeek está experimentando problemas mediante su página de estado.

### Errores de Modelo No Encontrado

**Síntoma**: Recibes errores indicando que el modelo solicitado no existe.

**Soluciones**:

1. Verifica que el modelo especificado en `DEEPSEEK_MODELO` o en la solicitud es válido.
2. Consulta la lista de modelos disponibles en la API de DeepSeek.

## Errores en la Configuración

### Variables de Entorno Faltantes

**Síntoma**: El servicio no inicia o devuelve errores sobre configuración faltante.

**Soluciones**:

1. Asegúrate de que todas las variables de entorno requeridas están definidas:
   ```bash
   env | grep DEEPSEEK
   ```

2. Verifica que el archivo `.env` existe y está correctamente formateado.

3. Si usas Docker, comprueba que las variables están pasadas al contenedor.

### Errores de Formato en Variables

**Síntoma**: El servicio inicia pero se comporta de manera inesperada.

**Soluciones**:

1. Verifica que los valores numéricos (`API_PUERTO`, `MAX_TOKENS_PREDETERMINADO`, etc.) son números válidos.
2. Asegúrate de que la temperatura está en el rango de 0.0 a 1.0.

## Problemas de Docker

### El Contenedor No Inicia

**Síntoma**: El contenedor Docker no inicia o se detiene inmediatamente.

**Soluciones**:

1. Verifica los logs del contenedor:
   ```bash
   docker logs deepseek-api-ms
   ```

2. Comprueba que todas las variables de entorno requeridas están definidas en `docker-compose.yml` o pasadas al contenedor.

3. Verifica que el puerto no está siendo utilizado por otro servicio:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

### Healthcheck Fallando

**Síntoma**: Docker reporta que el healthcheck del contenedor está fallando.

**Soluciones**:

1. Verifica que el servicio está respondiendo al endpoint `/salud`:
   ```bash
   curl http://localhost:<puerto>/salud
   ```

2. Comprueba que la variable `API_PUERTO` está correctamente configurada y es la misma que se usa en el healthcheck.

3. Revisa los logs para identificar posibles errores en el servicio.

## Logs y Depuración

### Habilitar Logs Detallados

Para obtener más información sobre los errores, puedes aumentar el nivel de detalle de los logs:

1. Cambia la variable de entorno `NIVEL_LOG` a `DEBUG`.
2. Reinicia el servicio para aplicar los cambios.
3. Examina los logs en la carpeta `logs/app.log` o en la salida de la consola.

### Depuración de Solicitudes

Para depurar problemas con las solicitudes, puedes usar herramientas como `curl` con el flag `-v`:

```bash
curl -v -X POST http://localhost:5003/api/v1/procesar \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu_api_key" \
  -d '{"texto": "Test"}'
```

## Preguntas Frecuentes

### ¿Cómo puedo cambiar el modelo utilizado?

Puedes cambiar el modelo de dos formas:
1. Modificando la variable de entorno `DEEPSEEK_MODELO`.
2. Especificando el modelo en cada solicitud mediante el parámetro `modelo`.

### ¿Por qué la API es lenta a veces?

La velocidad de respuesta depende de varios factores:
1. Tamaño del texto a procesar.
2. Disponibilidad y carga de los servidores de DeepSeek.
3. Parámetros como `max_tokens` (valores más altos pueden resultar en tiempos de procesamiento más largos).

### ¿Puedo usar este servicio en producción?

Sí, el servicio está diseñado para ser utilizado en entornos de producción. Consideraciones:
1. Configura correctamente las variables de entorno.
2. Asegura la API Key con prácticas seguras.
3. Implementa monitoreo y alertas para detectar problemas.
4. Considera usar un sistema de balanceo de carga para alta disponibilidad.

---

Si encuentras un problema que no está cubierto en esta guía, por favor revisa los logs del servicio y la documentación de la API de DeepSeek, o contacta al equipo de soporte.
