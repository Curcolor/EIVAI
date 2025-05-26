#!/usr/bin/env python3
"""
Script simple para inicializar la base de datos SQLite
"""
import sys
import os
from sqlalchemy import text

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("🚀 Iniciando configuración de base de datos SQLite")

try:
    print("📦 Importando configuración de base de datos...")
    from src.config.database import engine, Base, SessionLocal
    print("✅ Configuración importada correctamente")
    
    print("📦 Importando modelos...")
    # Importar todos los modelos para que se registren en Base.metadata
    from src.api.models import usuario, estado_instrumento, instrumento, set_quirurgico
    from src.api.models import alerta, conteo_instrumento, procedimiento_quirurgico
    print("✅ Modelos importados correctamente")
    
    print("🏗️ Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")
    
    print("📊 Verificando tablas creadas...")
    # Comprobar que el archivo de base de datos se creó
    if os.path.exists("eivai_local.db"):
        print("✅ Archivo de base de datos creado: eivai_local.db")
        file_size = os.path.getsize("eivai_local.db")
        print(f"📏 Tamaño del archivo: {file_size} bytes")
    else:
        print("❌ No se pudo crear el archivo de base de datos")
    
    # Probar conexión
    print("🔗 Probando conexión...")
    db = SessionLocal()
    try:
        # Ejecutar una consulta simple
        result = db.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = result.fetchall()
        print(f"✅ Conexión exitosa. Tablas creadas: {len(tables)}")
        for table in tables:
            print(f"   • {table[0]}")
    finally:
        db.close()
    
    print("\n🎉 Base de datos SQLite configurada exitosamente")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
