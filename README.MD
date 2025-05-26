# Frontend Estático EIVAI

Aplicación de frontend estático desarrollada con FastAPI, estructura modular y bien organizada.

## Estructura del Proyecto

```
Fronted/
├── run.py                 # Archivo principal para ejecutar el servidor
├── requirements.txt       # Dependencias del proyecto
├── .venv/                # Entorno virtual (auto-generado)
└── src/                  # Código fuente principal
    ├── __init__.py       # Inicialización del módulo
    ├── app.py            # Creación y configuración de la app FastAPI
    ├── config.py         # Configuración centralizada
    ├── routes.py         # Definición de rutas
    ├── static/           # Archivos estáticos
    │   ├── css/
    │   │   └── style.css # Estilos personalizados
    │   ├── js/
    │   │   └── main.js   # JavaScript principal
    │   └── img/          # Imágenes y recursos
    └── templates/        # Templates HTML con Jinja2
        ├── base.html     # Template base
        ├── index.html    # Página principal
        ├── about.html    # Página acerca de
        └── contact.html  # Página de contacto
```

## Instalación y Configuración

1. **Navegar al directorio del proyecto:**
   ```bash
   cd "c:\Users\Laboratorio\Desktop\Workspace\EIVAI\Fronted"
   ```

2. **Activar el entorno virtual:**
   ```bash
   # En Windows
   .venv\Scripts\activate
   
   # En Linux/Mac
   source .venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el servidor:**
   ```bash
   python run.py
   ```

5. **Abrir en el navegador:**
   - http://localhost:8000

## Características

- ✅ **Estructura Modular**: Código bien organizado y separado por responsabilidades
- ✅ **Configuración Centralizada**: Todas las configuraciones en `config.py`
- ✅ **Rutas Organizadas**: Endpoints definidos en `routes.py`
- ✅ **Templates Dinámicos**: Sistema de templates con Jinja2
- ✅ **Archivos Estáticos**: Soporte completo para CSS, JS e imágenes
- ✅ **Responsive Design**: Interfaz adaptativa con Bootstrap 5
- ✅ **CORS Configurado**: Preparado para desarrollo frontend/backend separado

## Endpoints Disponibles

- `/` - Página principal
- `/about` - Información sobre la aplicación
- `/contact` - Formulario de contacto
- `/health` - Health check del servidor
- `/static/*` - Archivos estáticos

## Tecnologías Utilizadas

- **FastAPI** - Framework web moderno y rápido
- **Uvicorn** - Servidor ASGI de alto rendimiento
- **Jinja2** - Motor de templates potente y flexible
- **Bootstrap 5** - Framework CSS para diseño responsive
- **Font Awesome** - Librería de iconos
- **Python 3.8+** - Lenguaje de programación

## Desarrollo

### Añadir nuevas rutas:
1. Definir la ruta en `src/routes.py`
2. Crear el template correspondiente en `src/templates/`
3. Añadir estilos en `src/static/css/style.css` si es necesario

### Configuración:
- Modificar variables en `src/config.py`
- Las configuraciones se pueden override con variables de entorno

### Archivos estáticos:
- CSS: `src/static/css/`
- JavaScript: `src/static/js/`
- Imágenes: `src/static/img/`

## Scripts Útiles

```bash
# Desarrollo con auto-reload
python run.py

# Verificar estado del servidor
curl http://localhost:8000/health

# Instalar nueva dependencia
pip install nueva-dependencia
pip freeze > requirements.txt
```

## Próximas Mejoras

- [ ] Sistema de autenticación
- [ ] API REST para datos dinámicos
- [ ] Integración con base de datos
- [ ] Tests automatizados
- [ ] Docker containerization
- [ ] CI/CD pipeline

