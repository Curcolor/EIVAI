#!/usr/bin/env python3
"""
Script para inicializar la base de datos SQLite con datos de prueba
"""
import sys
import os
from datetime import datetime, timedelta

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.database import engine, Base, SessionLocal
from src.api.models.usuario import Usuario
from src.api.models.estado_instrumento import EstadoInstrumento
from src.api.models.instrumento import Instrumento
from src.api.models.set_quirurgico import SetQuirurgico
from src.api.models.set_instrumento import SetInstrumento
from src.api.models.procedimiento_quirurgico import ProcedimientoQuirurgico
from src.api.models.conteo_instrumento import ConteoInstrumento
from src.api.models.alerta import Alerta


def create_tables():
    """Crear todas las tablas en la base de datos"""
    print("🏗️ Creando tablas en la base de datos SQLite...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")


def insert_sample_data():
    """Insertar datos de muestra para pruebas"""
    db = SessionLocal()
    
    try:
        print("📝 Insertando datos de muestra...")
        
        # 1. Estados de Instrumentos
        estados = [
            EstadoInstrumento(
                estado_id=1,
                nombre_estado="DISPONIBLE",
                descripcion="Instrumento disponible para uso",
                requiere_mantenimiento=False
            ),
            EstadoInstrumento(
                estado_id=2,
                nombre_estado="EN_USO",
                descripcion="Instrumento en uso durante procedimiento",
                requiere_mantenimiento=False
            ),
            EstadoInstrumento(
                estado_id=3,
                nombre_estado="MANTENIMIENTO",
                descripcion="Instrumento requiere mantenimiento",
                requiere_mantenimiento=True
            ),
            EstadoInstrumento(
                estado_id=4,
                nombre_estado="ESTERILIZACION",
                descripcion="Instrumento en proceso de esterilización",
                requiere_mantenimiento=False
            ),
            EstadoInstrumento(
                estado_id=5,
                nombre_estado="FUERA_SERVICIO",
                descripcion="Instrumento fuera de servicio",
                requiere_mantenimiento=True
            )
        ]
        
        for estado in estados:
            existing = db.query(EstadoInstrumento).filter_by(estado_id=estado.estado_id).first()
            if not existing:
                db.add(estado)
        
        # 2. Usuarios
        usuarios = [
            Usuario(
                usuario_id=1,
                nombre_usuario="admin",
                nombre_completo="Administrador del Sistema",
                email="admin@eivai.com",
                password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY0bOvPm6vQF.7e",  # password: admin123
                es_admin=True,
                activo=True
            ),
            Usuario(
                usuario_id=2,
                nombre_usuario="doctor_martinez",
                nombre_completo="Dr. Carlos Martínez",
                email="carlos.martinez@hospital.com",
                password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY0bOvPm6vQF.7e",  # password: admin123
                es_admin=False,
                activo=True
            ),
            Usuario(
                usuario_id=3,
                nombre_usuario="enfermera_garcia",
                nombre_completo="Enfermera Ana García",
                email="ana.garcia@hospital.com",
                password_hash="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY0bOvPm6vQF.7e",  # password: admin123
                es_admin=False,
                activo=True
            )
        ]
        
        for usuario in usuarios:
            existing = db.query(Usuario).filter_by(usuario_id=usuario.usuario_id).first()
            if not existing:
                db.add(usuario)
        
        # 3. Instrumentos
        instrumentos = [
            Instrumento(
                instrumento_id=1,
                codigo_instrumento="INS001",
                nombre_instrumento="Bisturí Quirúrgico",
                descripcion="Bisturí para incisiones quirúrgicas",
                estado_id=1,
                contador_uso=45
            ),
            Instrumento(
                instrumento_id=2,
                codigo_instrumento="INS002",
                nombre_instrumento="Pinzas Kelly",
                descripcion="Pinzas hemostáticas Kelly",
                estado_id=1,
                contador_uso=23
            ),
            Instrumento(
                instrumento_id=3,
                codigo_instrumento="INS003",
                nombre_instrumento="Tijeras Mayo",
                descripcion="Tijeras quirúrgicas Mayo",
                estado_id=2,
                contador_uso=67
            ),
            Instrumento(
                instrumento_id=4,
                codigo_instrumento="INS004",
                nombre_instrumento="Porta Agujas",
                descripcion="Porta agujas para suturas",
                estado_id=1,
                contador_uso=89
            ),
            Instrumento(
                instrumento_id=5,
                codigo_instrumento="INS005",
                nombre_instrumento="Separador Farabeuf",
                descripcion="Separador de tejidos Farabeuf",
                estado_id=3,
                contador_uso=12
            )
        ]
        
        for instrumento in instrumentos:
            existing = db.query(Instrumento).filter_by(instrumento_id=instrumento.instrumento_id).first()
            if not existing:
                db.add(instrumento)
        
        # 4. Sets Quirúrgicos
        sets_quirurgicos = [
            SetQuirurgico(
                set_id=1,
                nombre_set="Set Cirugía General",
                numero_identificacion="SET001",
                tipo_procedimiento="Cirugía General",
                descripcion="Set básico para cirugías generales",
                activo=True
            ),
            SetQuirurgico(
                set_id=2,
                nombre_set="Set Cirugía Cardiovascular",
                numero_identificacion="SET002",
                tipo_procedimiento="Cirugía Cardiovascular",
                descripcion="Set especializado para cirugías cardiovasculares",
                activo=True
            ),
            SetQuirurgico(
                set_id=3,
                nombre_set="Set Cirugía Laparoscópica",
                numero_identificacion="SET003",
                tipo_procedimiento="Cirugía Laparoscópica",
                descripcion="Set para procedimientos laparoscópicos",
                activo=True
            )
        ]
        
        for set_quirurgico in sets_quirurgicos:
            existing = db.query(SetQuirurgico).filter_by(set_id=set_quirurgico.set_id).first()
            if not existing:
                db.add(set_quirurgico)
        
        # 5. Asociaciones Set-Instrumento
        asociaciones = [
            SetInstrumento(set_id=1, instrumento_id=1, cantidad=2, obligatorio=True),
            SetInstrumento(set_id=1, instrumento_id=2, cantidad=4, obligatorio=True),
            SetInstrumento(set_id=1, instrumento_id=3, cantidad=1, obligatorio=True),
            SetInstrumento(set_id=1, instrumento_id=4, cantidad=2, obligatorio=True),
            SetInstrumento(set_id=2, instrumento_id=1, cantidad=1, obligatorio=True),
            SetInstrumento(set_id=2, instrumento_id=2, cantidad=6, obligatorio=True),
            SetInstrumento(set_id=2, instrumento_id=5, cantidad=2, obligatorio=False),
            SetInstrumento(set_id=3, instrumento_id=3, cantidad=2, obligatorio=True),
            SetInstrumento(set_id=3, instrumento_id=4, cantidad=1, obligatorio=True),
        ]
        
        for asociacion in asociaciones:
            existing = db.query(SetInstrumento).filter_by(
                set_id=asociacion.set_id, 
                instrumento_id=asociacion.instrumento_id
            ).first()
            if not existing:
                db.add(asociacion)
        
        # 6. Procedimientos Quirúrgicos
        now = datetime.now()
        procedimientos = [
            ProcedimientoQuirurgico(
                procedimiento_id=1,
                set_id=1,
                usuario_responsable=2,
                fecha_procedimiento=now - timedelta(days=1),
                tipo_cirugia="Apendicectomía",
                paciente="Juan Pérez López",
                medico="Dr. Carlos Martínez",
                estado_procedimiento="FINALIZADO",
                conteo_inicial_completo=True,
                conteo_final_completo=True
            ),
            ProcedimientoQuirurgico(
                procedimiento_id=2,
                set_id=2,
                usuario_responsable=2,
                fecha_procedimiento=now,
                tipo_cirugia="Bypass Coronario",
                paciente="María González Ruiz",
                medico="Dr. Carlos Martínez",
                estado_procedimiento="EN_PROCESO",
                conteo_inicial_completo=True,
                conteo_final_completo=False
            ),
            ProcedimientoQuirurgico(
                procedimiento_id=3,
                set_id=3,
                usuario_responsable=3,
                fecha_procedimiento=now + timedelta(hours=2),
                tipo_cirugia="Colecistectomía Laparoscópica",
                paciente="Luis Rodríguez Sánchez",
                medico="Dr. Elena Torres",
                estado_procedimiento="PROGRAMADO",
                conteo_inicial_completo=False,
                conteo_final_completo=False
            )
        ]
        
        for procedimiento in procedimientos:
            existing = db.query(ProcedimientoQuirurgico).filter_by(procedimiento_id=procedimiento.procedimiento_id).first()
            if not existing:
                db.add(procedimiento)
        
        # 7. Conteos de Instrumentos
        conteos = [
            ConteoInstrumento(
                conteo_id=1,
                procedimiento_id=1,
                instrumento_id=1,
                tipo_conteo="INICIAL",
                cantidad_contada=2,
                cantidad_esperada=2,
                usuario_conteo=3,
                observaciones="Conteo inicial correcto",
                tiene_discrepancia=False,
                fecha_conteo=now - timedelta(days=1, hours=2)
            ),
            ConteoInstrumento(
                conteo_id=2,
                procedimiento_id=1,
                instrumento_id=1,
                tipo_conteo="FINAL",
                cantidad_contada=2,
                cantidad_esperada=2,
                usuario_conteo=3,
                observaciones="Conteo final correcto",
                tiene_discrepancia=False,
                fecha_conteo=now - timedelta(days=1, hours=1)
            ),
            ConteoInstrumento(
                conteo_id=3,
                procedimiento_id=2,
                instrumento_id=2,
                tipo_conteo="INICIAL",
                cantidad_contada=5,
                cantidad_esperada=6,
                usuario_conteo=3,
                observaciones="Falta una pinza Kelly",
                tiene_discrepancia=True,
                fecha_conteo=now - timedelta(hours=1)
            )
        ]
        
        for conteo in conteos:
            existing = db.query(ConteoInstrumento).filter_by(conteo_id=conteo.conteo_id).first()
            if not existing:
                db.add(conteo)
        
        # 8. Alertas
        alertas = [
            Alerta(
                alerta_id=1,
                tipo_alerta="DISCREPANCIA_CONTEO",
                mensaje="Discrepancia detectada en conteo de Pinzas Kelly",
                prioridad="ALTA",
                procedimiento_id=2,
                instrumento_id=2,
                resuelta=False,
                es_critica=True,
                esta_activa=True,
                fecha_creacion=now - timedelta(minutes=30)
            ),
            Alerta(
                alerta_id=2,
                tipo_alerta="MANTENIMIENTO_REQUERIDO",
                mensaje="Separador Farabeuf requiere mantenimiento",
                prioridad="MEDIA",
                instrumento_id=5,
                resuelta=False,
                es_critica=False,
                esta_activa=True,
                fecha_creacion=now - timedelta(hours=2)
            ),
            Alerta(
                alerta_id=3,
                tipo_alerta="PROCEDIMIENTO_INICIADO",
                mensaje="Bypass Coronario iniciado - verificar conteo inicial",
                prioridad="BAJA",
                procedimiento_id=2,
                resuelta=True,
                es_critica=False,
                esta_activa=False,
                fecha_creacion=now - timedelta(hours=1),
                fecha_resolucion=now - timedelta(minutes=45),
                usuario_resolucion=2
            )
        ]
        
        for alerta in alertas:
            existing = db.query(Alerta).filter_by(alerta_id=alerta.alerta_id).first()
            if not existing:
                db.add(alerta)
        
        # Commit de todos los cambios
        db.commit()
        print("✅ Datos de muestra insertados exitosamente")
        
        # Mostrar estadísticas
        print("\n📊 Estadísticas de la base de datos:")
        print(f"   • Usuarios: {db.query(Usuario).count()}")
        print(f"   • Estados de Instrumentos: {db.query(EstadoInstrumento).count()}")
        print(f"   • Instrumentos: {db.query(Instrumento).count()}")
        print(f"   • Sets Quirúrgicos: {db.query(SetQuirurgico).count()}")
        print(f"   • Asociaciones Set-Instrumento: {db.query(SetInstrumento).count()}")
        print(f"   • Procedimientos: {db.query(ProcedimientoQuirurgico).count()}")
        print(f"   • Conteos: {db.query(ConteoInstrumento).count()}")
        print(f"   • Alertas: {db.query(Alerta).count()}")
        
    except Exception as e:
        print(f"❌ Error insertando datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """Función principal"""
    print("🚀 Inicializando base de datos SQLite para EIVAI")
    print("=" * 50)
    
    try:
        # Verificar si el archivo de BD ya existe
        db_file = "eivai_local.db"
        if os.path.exists(db_file):
            response = input(f"⚠️ La base de datos '{db_file}' ya existe. ¿Recrear? (s/N): ")
            if response.lower() in ['s', 'si', 'yes', 'y']:
                os.remove(db_file)
                print(f"🗑️ Base de datos anterior eliminada")
            else:
                print("ℹ️ Manteniendo base de datos existente")
                return
        
        # Crear tablas e insertar datos
        create_tables()
        insert_sample_data()
        
        print("\n🎉 Base de datos SQLite inicializada exitosamente")
        print(f"📁 Archivo de base de datos: {os.path.abspath(db_file)}")
        print("\n👤 Usuarios de prueba:")
        print("   • admin / admin123 (Administrador)")
        print("   • doctor_martinez / admin123 (Doctor)")
        print("   • enfermera_garcia / admin123 (Enfermera)")
        
    except Exception as e:
        print(f"❌ Error durante la inicialización: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
