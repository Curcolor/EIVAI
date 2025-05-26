# ORM - Sistema EIVAI

Este directorio contiene la configuración del ORM (Object-Relational Mapping) para el Sistema de Gestión de Instrumental Quirúrgico EIVAI.

## Estructura

```
src/
├── config/
│   └── database.py          # Configuración de la base de datos
├── api/
│   └── models/              # Modelos ORM
│       ├── __init__.py      # Exportaciones de modelos
│       ├── base.py          # Modelo base y mixins
│       ├── usuario.py       # Modelo de usuarios
│       ├── estado_instrumento.py
│       ├── instrumento.py
│       ├── set_quirurgico.py
│       ├── set_instrumento.py
│       ├── procedimiento_quirurgico.py
│       ├── conteo_instrumento.py
│       ├── ciclo_esterilizacion.py
│       ├── instrumento_esterilizacion.py
│       ├── alerta.py
│       ├── fotografia.py
│       └── auditoria_accion.py
└── services/                # Servicios de negocio
    ├── __init__.py
    ├── base_service.py      # Servicio base CRUD
    ├── usuario_service.py   # Servicio de usuarios
    └── instrumento_service.py
```

## Configuración

### 1. Variables de Entorno

Crear un archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

Configurar las variables de base de datos:

```env
DB_SERVER=localhost
DB_DATABASE=EIVEI_DB
DB_USERNAME=sa
DB_PASSWORD=tu_contraseña
DB_DRIVER=ODBC Driver 17 for SQL Server
```

### 2. Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### 3. Inicialización de la Base de Datos

```bash
# Crear tablas
python scripts/init_db.py

# Reiniciar base de datos (eliminar y recrear)
python scripts/init_db.py --reset
```

### 4. Pruebas

```bash
# Probar conexión y modelos
python scripts/test_orm.py
```

## Uso del ORM

### Importar Modelos

```python
from src.api.models import Usuario, Instrumento, SetQuirurgico
from src.config.database import get_db
```

### Usar Servicios

```python
from src.services import UsuarioService, InstrumentoService

# Crear servicio
user_service = UsuarioService()

# Usar con dependencia de base de datos
def get_users(db: Session = Depends(get_db)):
    return user_service.get_active_users(db)
```

### Operaciones CRUD Básicas

```python
# Crear usuario
user_data = {
    'nombre_usuario': 'nuevo_user',
    'nombre_completo': 'Usuario Nuevo',
    'email': 'usuario@hospital.com',
    'password_hash': 'hash_password'
}
nuevo_usuario = user_service.create(db, user_data)

# Obtener por ID
usuario = user_service.get_by_id(db, 1)

# Actualizar
user_service.update(db, 1, {'email': 'nuevo@email.com'})

# Eliminar
user_service.delete(db, 1)
```

## Modelos Principales

### Usuario
- Gestión de instrumentadores y usuarios del sistema
- Autenticación y autorización
- Auditoría de acciones

### Instrumento
- Catálogo de instrumentos quirúrgicos
- Estados y mantenimiento
- Historial de uso

### SetQuirurgico
- Conjuntos de instrumentos para procedimientos
- Relación con instrumentos mediante SetInstrumento

### ProcedimientoQuirurgico
- Registro de procedimientos quirúrgicos
- Conteos inicial y final
- Seguimiento de estado

### ConteoInstrumento
- Registro de conteos de instrumentos
- Fotografías de evidencia
- Detección de discrepancias

## Características del ORM

### Relaciones
- **One-to-Many**: Usuario → ProcedimientoQuirurgico
- **Many-to-Many**: SetQuirurgico ↔ Instrumento (través de SetInstrumento)
- **One-to-One**: Instrumento → EstadoInstrumento

### Validaciones
- Constraints de base de datos
- Validaciones a nivel de modelo
- Checks de integridad referencial

### Auditoría
- Registro automático de cambios
- Timestamps en todos los modelos
- Trazabilidad completa

### Índices
- Optimización de consultas frecuentes
- Índices compuestos para búsquedas complejas
- Performance mejorada

## Servicios

Los servicios proporcionan una capa de abstracción sobre los modelos:

- **BaseService**: CRUD genérico para todos los modelos
- **UsuarioService**: Autenticación, gestión de contraseñas
- **InstrumentoService**: Búsquedas, mantenimiento, contadores

## Seguridad

- Hashing de contraseñas con SHA256
- Validación de entrada de datos
- Transacciones para consistencia
- Manejo de errores y rollback automático

## Troubleshooting

### Error de Conexión
1. Verificar que SQL Server esté ejecutándose
2. Comprobar credenciales en `.env`
3. Verificar que el driver ODBC esté instalado

### Error de Importación
```python
# Asegurar que el PYTHONPATH incluya el directorio src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### Problemas de Migración
```bash
# Reiniciar base de datos
python scripts/init_db.py --reset
```
