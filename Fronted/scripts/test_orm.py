"""
Script para probar la conexión a la base de datos y el ORM
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.database import engine, SessionLocal
from src.api.models import Usuario, EstadoInstrumento, Instrumento
from src.services import UsuarioService, InstrumentoService
from sqlalchemy import text

def test_connection():
    """
    Probar la conexión a la base de datos
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT @@VERSION"))
            version = result.fetchone()[0]
            print(f"✓ Conexión exitosa a SQL Server: {version}")
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_models():
    """
    Probar los modelos ORM
    """
    try:
        db = SessionLocal()
        
        # Probar consulta de usuarios
        usuarios = db.query(Usuario).limit(5).all()
        print(f"✓ Usuarios encontrados: {len(usuarios)}")
        for usuario in usuarios:
            print(f"  - {usuario.nombre_completo} ({usuario.nombre_usuario})")
        
        # Probar consulta de estados
        estados = db.query(EstadoInstrumento).all()
        print(f"✓ Estados de instrumento: {len(estados)}")
        for estado in estados:
            print(f"  - {estado.nombre_estado}")
        
        # Probar consulta de instrumentos
        instrumentos = db.query(Instrumento).limit(5).all()
        print(f"✓ Instrumentos encontrados: {len(instrumentos)}")
        for instrumento in instrumentos:
            print(f"  - {instrumento.nombre_instrumento} ({instrumento.codigo_instrumento})")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en modelos: {e}")
        return False

def test_services():
    """
    Probar los servicios
    """
    try:
        db = SessionLocal()
        
        # Probar servicio de usuarios
        user_service = UsuarioService()
        usuarios = user_service.get_active_users(db)
        print(f"✓ Usuarios activos (servicio): {len(usuarios)}")
        
        # Probar servicio de instrumentos
        instrument_service = InstrumentoService()
        instrumentos_mantenimiento = instrument_service.get_que_requieren_mantenimiento(db)
        print(f"✓ Instrumentos que requieren mantenimiento: {len(instrumentos_mantenimiento)}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en servicios: {e}")
        return False

def main():
    """
    Ejecutar todas las pruebas
    """
    print("🔍 Probando la configuración del ORM...")
    print("-" * 50)
    
    # Probar conexión
    if not test_connection():
        return
    
    print("-" * 50)
    
    # Probar modelos
    if not test_models():
        return
    
    print("-" * 50)
    
    # Probar servicios
    if not test_services():
        return
    
    print("-" * 50)
    print("🎉 Todas las pruebas completadas exitosamente!")
    print("📋 El ORM está configurado y funcionando correctamente.")

if __name__ == "__main__":
    main()
