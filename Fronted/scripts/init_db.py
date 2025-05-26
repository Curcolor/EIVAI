"""
Script para inicializar la base de datos y crear las tablas
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.models import create_all_tables, drop_all_tables
from src.config.database import engine
from sqlalchemy import text

def init_database():
    """
    Inicializar la base de datos creando todas las tablas
    """
    try:
        print("Inicializando la base de datos...")
        
        # Verificar conexión
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✓ Conexión a la base de datos exitosa")
        
        # Crear todas las tablas
        create_all_tables()
        print("✓ Tablas creadas exitosamente")
        
        print("🎉 Base de datos inicializada correctamente")
        
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        return False
    
    return True

def reset_database():
    """
    Reiniciar la base de datos eliminando y recreando todas las tablas
    """
    try:
        print("⚠️  Reiniciando la base de datos...")
        
        # Eliminar todas las tablas
        drop_all_tables()
        print("✓ Tablas eliminadas")
        
        # Crear todas las tablas
        create_all_tables()
        print("✓ Tablas recreadas")
        
        print("🎉 Base de datos reiniciada correctamente")
        
    except Exception as e:
        print(f"❌ Error al reiniciar la base de datos: {e}")
        return False
    
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Gestión de la base de datos EIVAI")
    parser.add_argument("--reset", action="store_true", help="Reiniciar la base de datos (eliminar y recrear tablas)")
    
    args = parser.parse_args()
    
    if args.reset:
        reset_database()
    else:
        init_database()
