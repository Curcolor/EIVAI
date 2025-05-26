# Ejemplos Detallados de Uso - DeepSeek API

Este documento proporciona ejemplos detallados sobre cómo usar e integrar el microservicio DeepSeek API en diferentes escenarios.

## Tabla de Contenidos

- [Introducción](#introducción)
- [Autenticación](#autenticación)
- [Ejemplos de Integración](#ejemplos-de-integración)
  - [Ejemplos con cURL](#ejemplos-con-curl)
  - [Ejemplos con Python](#ejemplos-con-python)
  - [Ejemplos con JavaScript](#ejemplos-con-javascript)
- [Casos de Uso Comunes](#casos-de-uso-comunes)
  - [Traducción de Textos](#traducción-de-textos)
  - [Generación de Contenido](#generación-de-contenido)
  - [Análisis de Sentimiento](#análisis-de-sentimiento)
  - [Resumen de Textos](#resumen-de-textos)
- [Optimización de Parámetros](#optimización-de-parámetros)
- [Manejo de Errores](#manejo-de-errores)
- [Integración con Aplicaciones Web](#integración-con-aplicaciones-web)

## Introducción

El microservicio DeepSeek API permite procesar texto utilizando la API de DeepSeek. Proporciona una interfaz REST para enviar solicitudes de procesamiento de texto y recibir las respuestas generadas por los modelos de lenguaje de DeepSeek.

## Autenticación

Todas las solicitudes a la API (excepto `/salud` y `/`) requieren una API Key que debe enviarse en el encabezado `X-API-Key`.

```
X-API-Key: tu_api_key
```

Esta API Key se configura mediante la variable de entorno `DEFAULT_API_KEY`.

## Ejemplos de Integración

### Ejemplos con cURL

**Verificar estado del servicio:**

```bash
curl -X GET http://localhost:5003/salud
```

**Verificar estado de DeepSeek:**

```bash
curl -X GET http://localhost:5003/api/v1/estado \
  -H "X-API-Key: tu_api_key"
```

**Procesar texto simple:**

```bash
curl -X POST http://localhost:5003/api/v1/procesar \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu_api_key" \
  -d '{
    "texto": "¿Cuál es la capital de Francia?"
  }'
```

**Procesar texto con parámetros personalizados:**

```bash
curl -X POST http://localhost:5003/api/v1/procesar \
  -H "Content-Type: application/json" \
  -H "X-API-Key: tu_api_key" \
  -d '{
    "texto": "Escribe un poema corto sobre la primavera",
    "temperatura": 0.9,
    "max_tokens": 150,
    "modelo": "deepseek-chat"
  }'
```

### Ejemplos con Python

**Instalación de requisitos:**

```bash
pip install requests
```

**Cliente básico:**

```python
import requests
import json

# Configuración
API_URL = "http://localhost:5003"
API_KEY = "tu_api_key"

# Verificar estado
def verificar_estado():
    response = requests.get(f"{API_URL}/salud")
    return response.json()

# Procesar texto
def procesar_texto(texto, temperatura=None, max_tokens=None, modelo=None):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    payload = {"texto": texto}
    
    # Agregar parámetros opcionales si están presentes
    if temperatura is not None:
        payload["temperatura"] = temperatura
    if max_tokens is not None:
        payload["max_tokens"] = max_tokens
    if modelo is not None:
        payload["modelo"] = modelo
    
    response = requests.post(
        f"{API_URL}/api/v1/procesar",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Ejemplos de uso
if __name__ == "__main__":
    # Verificar estado
    print("Estado del servicio:")
    print(json.dumps(verificar_estado(), indent=2))
    
    # Procesamiento simple
    print("\nProcesamiento simple:")
    resultado = procesar_texto("¿Cuál es la capital de España?")
    print(json.dumps(resultado, indent=2))
    
    # Procesamiento con parámetros personalizados
    print("\nProcesamiento con parámetros personalizados:")
    resultado = procesar_texto(
        "Escribe un eslogan para una marca de café",
        temperatura=0.8,
        max_tokens=50
    )
    print(json.dumps(resultado, indent=2))
```

### Ejemplos con JavaScript

**Cliente JavaScript (usando Fetch API):**

```javascript
// Configuración
const API_URL = 'http://localhost:5003';
const API_KEY = 'tu_api_key';

// Verificar estado
async function verificarEstado() {
  const response = await fetch(`${API_URL}/salud`);
  return await response.json();
}

// Procesar texto
async function procesarTexto(texto, temperatura = null, maxTokens = null, modelo = null) {
  const headers = {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY
  };
  
  const payload = { texto };
  
  // Agregar parámetros opcionales si están presentes
  if (temperatura !== null) payload.temperatura = temperatura;
  if (maxTokens !== null) payload.max_tokens = maxTokens;
  if (modelo !== null) payload.modelo = modelo;
  
  try {
    const response = await fetch(`${API_URL}/api/v1/procesar`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify(payload)
    });
    
    if (response.ok) {
      return await response.json();
    } else {
      console.error(`Error: ${response.status}`);
      const errorData = await response.text();
      console.error(errorData);
      return null;
    }
  } catch (error) {
    console.error('Error al procesar texto:', error);
    return null;
  }
}

// Ejemplos de uso
async function ejemplos() {
  // Verificar estado
  console.log('Estado del servicio:');
  const estado = await verificarEstado();
  console.log(estado);
  
  // Procesamiento simple
  console.log('\nProcesamiento simple:');
  const resultadoSimple = await procesarTexto('¿Cuáles son los planetas del sistema solar?');
  console.log(resultadoSimple);
  
  // Procesamiento con parámetros personalizados
  console.log('\nProcesamiento con parámetros personalizados:');
  const resultadoPersonalizado = await procesarTexto(
    'Escribe un poema corto sobre el mar',
    0.9,
    100
  );
  console.log(resultadoPersonalizado);
}

// Ejecutar ejemplos
ejemplos();
```

## Casos de Uso Comunes

### Traducción de Textos

```json
{
  "texto": "Traduce el siguiente texto al francés: 'El sol brilla en el cielo azul'",
  "temperatura": 0.3
}
```

Respuesta esperada:

```json
{
  "texto_procesado": "Le soleil brille dans le ciel bleu",
  "modelo_usado": "deepseek-chat",
  "tokens_entrada": 18,
  "tokens_salida": 9,
  "tiempo_proceso": 0.643
}
```

### Generación de Contenido

```json
{
  "texto": "Genera 3 ideas de nombres para una cafetería que se especializa en café orgánico",
  "temperatura": 0.8,
  "max_tokens": 150
}
```

### Análisis de Sentimiento

```json
{
  "texto": "Analiza el sentimiento del siguiente texto: 'La película fue aburrida y los actores no actuaron bien'",
  "temperatura": 0.1
}
```

### Resumen de Textos

```json
{
  "texto": "Resume el siguiente texto en 2 oraciones: 'La inteligencia artificial (IA) es la simulación de procesos de inteligencia humana por parte de máquinas, especialmente sistemas informáticos. Estos procesos incluyen el aprendizaje (la adquisición de información y reglas para el uso de la información), el razonamiento (usar las reglas para llegar a conclusiones aproximadas o definitivas) y la autocorrección. Algunas aplicaciones particulares de la IA incluyen sistemas expertos, reconocimiento de voz y visión artificial. La IA puede ser categorizada como débil o fuerte. La IA débil, también conocida como IA estrecha, es un sistema diseñado para una tarea particular. La IA fuerte, también conocida como inteligencia general artificial, es un sistema con las habilidades cognitivas humanas generalizadas.'",
  "max_tokens": 100
}
```

## Optimización de Parámetros

### Ajuste de Temperatura

La temperatura controla la aleatoriedad en la generación de texto:

- **Valores bajos (0.1-0.3)**: Respuestas más deterministas y conservadoras.
- **Valores medios (0.4-0.6)**: Buen equilibrio entre creatividad y coherencia.
- **Valores altos (0.7-1.0)**: Respuestas más creativas y diversas.

### Ajuste de Max Tokens

El parámetro `max_tokens` controla la longitud máxima de la respuesta generada:

- **Valores bajos (20-50)**: Respuestas cortas y concisas.
- **Valores medios (100-200)**: Respuestas de longitud moderada.
- **Valores altos (300+)**: Respuestas largas y detalladas.

## Manejo de Errores

### Códigos de Error Comunes

- **400**: Error en la solicitud (formato incorrecto, parámetros inválidos)
- **401**: No autorizado (falta API Key)
- **403**: Prohibido (API Key inválida)
- **500**: Error interno del servidor

### Ejemplo de Respuesta de Error

```json
{
  "error": "Error en el servicio DeepSeek",
  "detalle": "Timeout en la conexión con la API de DeepSeek",
  "codigo": 500
}
```

## Integración con Aplicaciones Web

### Ejemplo de Integración con React

```jsx
import React, { useState } from 'react';
import axios from 'axios';

const DeepSeekComponent = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const API_URL = 'http://localhost:5003';
  const API_KEY = 'tu_api_key';
  
  const procesarTexto = async () => {
    if (!input.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.post(
        `${API_URL}/api/v1/procesar`,
        { texto: input },
        {
          headers: {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY
          }
        }
      );
      
      setResult(response.data);
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.error || 'Error al procesar el texto');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div>
      <h2>DeepSeek API Demo</h2>
      
      <div>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribe tu texto aquí..."
          rows={5}
          cols={50}
        />
      </div>
      
      <button onClick={procesarTexto} disabled={loading}>
        {loading ? 'Procesando...' : 'Procesar Texto'}
      </button>
      
      {error && (
        <div style={{ color: 'red', marginTop: '10px' }}>
          {error}
        </div>
      )}
      
      {result && (
        <div style={{ marginTop: '20px' }}>
          <h3>Resultado:</h3>
          <p><strong>Texto procesado:</strong></p>
          <div style={{ whiteSpace: 'pre-wrap', border: '1px solid #ccc', padding: '10px' }}>
            {result.texto_procesado}
          </div>
          <p><strong>Modelo usado:</strong> {result.modelo_usado}</p>
          <p><strong>Tokens entrada/salida:</strong> {result.tokens_entrada}/{result.tokens_salida}</p>
          <p><strong>Tiempo de proceso:</strong> {result.tiempo_proceso.toFixed(2)}s</p>
        </div>
      )}
    </div>
  );
};

export default DeepSeekComponent;
```

---

## Apéndice: Tabla de Modelos Disponibles

| Modelo | Descripción | Caso de uso recomendado |
|--------|-------------|-------------------------|
| deepseek-chat | Modelo conversacional general | Chatbots, preguntas y respuestas, generación de texto |
| deepseek-coder | Especializado en código | Generación y explicación de código |

---

Para más información sobre la API de DeepSeek y sus capacidades, consulta la [documentación oficial de DeepSeek](https://docs.deepseek.com).

Para problemas o dudas específicas sobre esta implementación, revisa el README principal o abre un issue en el repositorio del proyecto.
