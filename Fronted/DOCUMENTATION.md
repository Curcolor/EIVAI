# EIVAI Frontend - Documentación Completa

## 📋 Índice
1. [Descripción General](#descripción-general)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Sistema de Autenticación](#sistema-de-autenticación)
5. [Rutas y Páginas](#rutas-y-páginas)
6. [Gestión de CSS](#gestión-de-css)
7. [Instalación y Configuración](#instalación-y-configuración)
8. [Uso del Sistema](#uso-del-sistema)
9. [Funcionalidades](#funcionalidades)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Descripción General

**EIVAI** (Enhanced Instrument Visual AI) es un sistema avanzado de identificación de herramientas quirúrgicas basado en Inteligencia Artificial. El frontend está desarrollado con **FastAPI** y utiliza una arquitectura modular que garantiza escalabilidad, seguridad y facilidad de mantenimiento en entornos hospitalarios críticos.

### Características Principales
- ✅ **Identificación IA**: Precisión del 99.7% en identificación de herramientas
- ✅ **Tiempo Real**: Análisis en menos de 2 segundos
- ✅ **Base de Datos**: Más de 2,500 instrumentos quirúrgicos
- ✅ **Seguridad**: Cumple estándares HIPAA y GDPR
- ✅ **Interfaz Intuitiva**: Diseño médico especializado
- ✅ **Multiplataforma**: Compatible con web y móvil
- ✅ **Soporte 24/7**: Para centros médicos críticos

---

## 🏗️ Arquitectura del Sistema

### Stack Tecnológico

#### Backend & API
- **Python 3.9+**: Lenguaje principal
- **FastAPI**: Framework web moderno y de alto rendimiento
- **Uvicorn**: Servidor ASGI para producción
- **Jinja2**: Motor de templates para renderizado HTML
- **Pydantic**: Validación de datos y serialización

#### Frontend & UI
- **HTML5**: Estructura semántica
- **Bootstrap 5**: Framework CSS responsivo
- **JavaScript**: Interactividad y validaciones del lado cliente
- **Font Awesome**: Iconografía médica y de interfaz
- **CSS personalizado**: Tema quirúrgico especializado

#### Seguridad
- **Session-based Authentication**: Autenticación basada en sesiones
- **HTTP-only Cookies**: Prevención de ataques XSS
- **CSRF Protection**: Protección contra ataques CSRF
- **Password Hashing**: SHA256 (recomendado bcrypt en producción)

---

## 📁 Estructura del Proyecto

```
EIVAI-Frontend/
├── run.py                          # Punto de entrada principal
├── requirements.txt                # Dependencias de Python
├── README.md                      # Documentación básica
├── .env                           # Variables de entorno (crear)
└── src/
    ├── __init__.py
    ├── app.py                     # Configuración principal de FastAPI
    ├── config/
    │   ├── __init__.py
    │   ├── config.py              # Configuraciones del sistema
    │   └── database.py            # Configuración de base de datos
    ├── api/
    │   ├── __init__.py
    │   ├── app.py                 # Aplicación FastAPI
    │   └── routes/
    │       ├── __init__.py
    │       └── routes.py          # Todas las rutas de la aplicación
    ├── services/                  # Servicios de negocio
    │   ├── __init__.py
    │   ├── base_service.py
    │   ├── instrumento_service.py
    │   └── usuario_service.py
    ├── static/                    # Archivos estáticos
    │   ├── css/                   # Estilos CSS por página
    │   │   ├── style.css          # Estilos globales
    │   │   ├── auth.css           # Login y registro
    │   │   ├── index.css          # Dashboard principal
    │   │   ├── perfil.css         # Página de perfil
    │   │   ├── identificacion.css # Identificación IA
    │   │   ├── about.css          # Página about
    │   │   └── contact.css        # Página de contacto
    │   ├── js/                    # Scripts JavaScript
    │   │   ├── main.js           # Funciones generales
    │   │   └── contact.js        # Validaciones de contacto
    │   └── img/                  # Imágenes y recursos
    ├── templates/                # Plantillas HTML
    │   ├── base.html            # Plantilla base con navegación
    │   ├── index.html           # Dashboard principal
    │   ├── login.html           # Página de login
    │   ├── registro.html        # Registro de usuarios
    │   ├── perfil.html          # Perfil de usuario
    │   ├── identificacion.html  # Funcionalidad IA
    │   ├── about.html           # Información del sistema
    │   └── contact.html         # Contacto y soporte
    └── utils/                   # Utilidades generales
        └── __init__.py
```

---

## 🔐 Sistema de Autenticación

### Descripción
El sistema utiliza autenticación basada en sesiones con cookies HTTP-only para máxima seguridad.

### Características de Seguridad
- **Sesiones temporales**: 8 horas de duración por defecto
- **Cookies HTTP-only**: Previenen acceso desde JavaScript malicioso
- **Validación de usuarios**: Verificación de estado activo
- **Logout seguro**: Invalidación completa de sesión

### Flujo de Autenticación

1. **Login** (`/login`)
   - Usuario ingresa credenciales
   - Sistema verifica en base de datos simulada
   - Crea token de sesión único
   - Establece cookie HTTP-only
   - Redirige al dashboard

2. **Protección de Rutas**
   ```python
   user = get_current_user(request)
   if not user:
       return RedirectResponse(url="/login", status_code=302)
   ```

3. **Logout** (`/logout`)
   - Invalida sesión del servidor
   - Elimina cookie del navegador
   - Redirige al login

### Usuarios por Defecto
```python
# Usuario administrador predeterminado
username: "admin"
password: "admin"
```

> **Nota**: En producción, cambiar credenciales por defecto y usar bcrypt para hashing.

---

## 🛠️ Rutas y Páginas

### Rutas Públicas
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/login` | GET/POST | Página de autenticación |
| `/registro` | GET/POST | Registro de nuevos usuarios |

### Rutas Protegidas (Requieren Autenticación)
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Dashboard principal |
| `/identificacion` | GET | Identificación IA de herramientas |
| `/perfil` | GET | Perfil de usuario |

### Rutas de Información
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/about` | GET | Información del sistema |
| `/contact` | GET/POST | Contacto y soporte |

### Rutas de Servicio
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/logout` | GET | Cerrar sesión |
| `/health` | GET | Health check del sistema |

---

## 🎨 Gestión de CSS

### Arquitectura CSS
Cada página tiene su propio archivo CSS para optimizar la carga y facilitar el mantenimiento:

```css
/* Variables CSS globales para tema quirúrgico */
:root {
    --primary-color: #1B365D;      /* Azul médico profundo */
    --secondary-color: #2F7E79;    /* Verde quirúrgico */
    --success-color: #28a745;      /* Verde éxito */
    --danger-color: #dc3545;       /* Rojo alerta */
    --warning-color: #ffc107;      /* Amarillo advertencia */
    --info-color: #17a2b8;         /* Azul información */
    --light-color: #f8f9fa;        /* Gris claro */
    --dark-color: #343a40;         /* Gris oscuro */
}
```

### Archivos CSS por Página
- **`style.css`**: Estilos globales y base
- **`auth.css`**: Login y registro
- **`index.css`**: Dashboard con estadísticas y gráficos
- **`perfil.css`**: Perfil de usuario con gradientes
- **`identificacion.css`**: Funcionalidad IA con animaciones
- **`about.css`**: Página informativa
- **`contact.css`**: Formulario de contacto y validaciones

### Tema Quirúrgico
- Paleta de colores médica profesional
- Iconografía Font Awesome médica
- Animaciones suaves y profesionales
- Diseño responsivo para tablets médicas

---

## ⚙️ Instalación y Configuración

### Requisitos Previos
- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno

### Instalación Paso a Paso

1. **Clonar el repositorio**
   ```powershell
   git clone <repository-url>
   cd EIVAI/Fronted
   ```

2. **Crear entorno virtual**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Instalar dependencias**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno** (opcional)
   ```powershell
   # Crear archivo .env en la raíz
   echo "ENVIRONMENT=development" > .env
   echo "SECRET_KEY=tu-clave-secreta-aqui" >> .env
   ```

5. **Ejecutar la aplicación**
   ```powershell
   python run.py
   ```

6. **Acceder al sistema**
   - Abrir navegador en: `http://localhost:8000`
   - Usar credenciales: `admin` / `admin`

### Configuración de Producción

#### Variables de Entorno
```bash
ENVIRONMENT=production
SECRET_KEY=clave-super-secreta-para-produccion
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

#### Configuración de Servidor
```python
# En run.py para producción
uvicorn.run(
    "src.api.app:app",
    host="0.0.0.0",
    port=8000,
    reload=False,
    workers=4
)
```

---

## 📱 Uso del Sistema

### Para Instrumentadores Quirúrgicos

1. **Acceso al Sistema**
   - Navegar a la URL del sistema
   - Iniciar sesión con credenciales asignadas
   - Acceder al dashboard principal

2. **Identificación de Herramientas**
   - Ir a "Identificación de Herramientas"
   - Cargar imagen de la herramienta
   - Esperar análisis IA (< 2 segundos)
   - Revisar resultados y confianza

3. **Gestión de Perfil**
   - Acceder a "Mi Perfil"
   - Actualizar información personal
   - Revisar historial de identificaciones

### Para Administradores

1. **Monitoreo del Sistema**
   - Dashboard con estadísticas en tiempo real
   - Health check en `/health`
   - Logs de actividad

2. **Gestión de Usuarios**
   - Revisar registros en logs
   - Activar/desactivar cuentas
   - Gestionar permisos

---

## 🔧 Funcionalidades

### 1. Dashboard Principal (`/`)
- **Estadísticas en tiempo real**: Número de identificaciones, precisión, tiempo promedio
- **Gráficos interactivos**: Uso del sistema por día/semana
- **Accesos rápidos**: Enlaces a funciones principales
- **Alertas del sistema**: Notificaciones importantes

### 2. Identificación IA (`/identificacion`)
- **Carga de imágenes**: Drag & drop o selección de archivos
- **Análisis en tiempo real**: Procesamiento < 2 segundos
- **Resultados detallados**: Nombre, categoría, confianza
- **Historial de identificaciones**: Últimas 10 identificaciones

### 3. Perfil de Usuario (`/perfil`)
- **Información personal**: Nombre, email, licencia profesional
- **Estadísticas personales**: Identificaciones realizadas, precisión promedio
- **Configuración de cuenta**: Cambio de contraseña, preferencias
- **Historial de actividad**: Log de accesos y acciones

### 4. Página de Contacto (`/contact`)
- **Formulario de contacto**: Validación cliente y servidor
- **Múltiples categorías**: Soporte técnico, consultas, errores
- **Información de contacto**: Email, teléfono, ubicación
- **Términos de privacidad**: Modal con políticas GDPR/HIPAA

### 5. Información del Sistema (`/about`)
- **Descripción técnica**: Arquitectura y tecnologías
- **Estadísticas del sistema**: Precisión, base de datos, rendimiento
- **Estructura del proyecto**: Organización de archivos
- **Recursos adicionales**: Documentación, soporte

---

## 🚨 Troubleshooting

### Problemas Comunes

#### 1. Error de Módulos No Encontrados
```powershell
# Problema: ModuleNotFoundError
# Solución: Verificar entorno virtual y dependencias
pip install -r requirements.txt
.\venv\Scripts\Activate.ps1
```

#### 2. Puerto Ya en Uso
```powershell
# Problema: Port 8000 is already in use
# Solución: Cambiar puerto o terminar proceso
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### 3. Templates No Encontrados
```python
# Problema: TemplateNotFound
# Verificar: settings.TEMPLATES_DIR en config.py
TEMPLATES_DIR = "src/templates"
```

#### 4. CSS No Se Carga
```html
<!-- Verificar rutas en base.html -->
<link href="/static/css/style.css" rel="stylesheet">
```

#### 5. Sesión No Persiste
```python
# Verificar configuración de cookies
response.set_cookie(
    key="session_token",
    value=session_token,
    httponly=True,
    secure=False  # True en producción con HTTPS
)
```

### Logs y Debugging

#### Habilitar Logs Detallados
```python
# En config.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Verificar Health Check
```bash
# GET http://localhost:8000/health
# Respuesta esperada: {"status": "ok", "message": "Servidor funcionando correctamente"}
```

---

## 📝 Notas Adicionales

### Consideraciones de Seguridad
- Cambiar credenciales por defecto en producción
- Implementar bcrypt para hashing de contraseñas
- Configurar HTTPS en producción
- Implementar rate limiting para APIs
- Configurar CORS apropiadamente

### Optimizaciones de Rendimiento
- Implementar caching de templates
- Minificar CSS y JavaScript
- Optimizar imágenes
- Configurar CDN para archivos estáticos
- Implementar lazy loading para componentes pesados

### Mantenimiento
- Logs regulares de sistema
- Backup de configuraciones
- Monitoreo de rendimiento
- Actualizaciones de seguridad
- Testing automatizado

---

## 📞 Soporte

Para soporte técnico o consultas:
- **Email**: soporte@eivai.com
- **Teléfono**: +57 (1) 800-EIVAI
- **Documentación**: `/about`
- **Health Check**: `/health`

---

*Documentación actualizada: Mayo 2025*
*Versión del Sistema: 2.1.0*
