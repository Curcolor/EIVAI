"""
Configuración de la base de datos para el Sistema EIVAI
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos
DB_SERVER = os.getenv('DB_SERVER', 'localhost')
DB_DATABASE = os.getenv('DB_DATABASE', 'EIVEI_DB')
DB_USERNAME = os.getenv('DB_USERNAME', 'sa')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')
DB_DRIVER = os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')

# Crear la cadena de conexión para SQL Server
DATABASE_URL = f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}?driver={DB_DRIVER.replace(' ', '+')}"

# Crear el motor de base de datos
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Cambiar a True para ver las consultas SQL en logs
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "check_same_thread": False,
        "timeout": 30
    }
)

# Crear la sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

def get_db():
    """
    Dependency para obtener una sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_all_tables():
    """
    Crear todas las tablas en la base de datos
    """
    Base.metadata.create_all(bind=engine)

def drop_all_tables():
    """
    Eliminar todas las tablas de la base de datos
    """
    Base.metadata.drop_all(bind=engine)
