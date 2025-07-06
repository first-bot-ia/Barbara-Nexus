#!/usr/bin/env python3
"""
🔍 DIAGNÓSTICO COMPLETO DEL SERVIDOR BARBARA
Este script identifica exactamente qué está causando que el servidor no se inicie
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    else:
        print("✅ Versión de Python compatible")
        return True

def check_environment_file():
    """Verifica el archivo de variables de entorno"""
    print("\n🔧 Verificando archivo .environment...")
    
    env_file = Path(".environment")
    if not env_file.exists():
        print("❌ Archivo .environment no encontrado")
        return False
    
    try:
        with open(env_file, 'r') as f:
            content = f.read()
        
        if "GEMINI_API_KEY=" in content:
            print("✅ GEMINI_API_KEY encontrada")
            return True
        else:
            print("❌ GEMINI_API_KEY no encontrada en .environment")
            return False
    except Exception as e:
        print(f"❌ Error leyendo .environment: {e}")
        return False

def check_dependencies():
    """Verifica las dependencias principales"""
    print("\n📦 Verificando dependencias...")
    
    dependencies = [
        'flask',
        'flask_cors', 
        'requests',
        'python-dotenv',
        'twilio'
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep.replace('-', '_'))
            print(f"   ✅ {dep}")
        except ImportError:
            print(f"   ❌ {dep} - FALTANTE")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️ Dependencias faltantes: {', '.join(missing)}")
        print("   Ejecuta: pip install " + " ".join(missing))
        return False
    
    return True

def check_optional_dependencies():
    """Verifica dependencias opcionales que pueden causar problemas"""
    print("\n🔍 Verificando dependencias opcionales...")
    
    optional_deps = [
        'spacy',
        'psycopg2',
        'openai'
    ]
    
    for dep in optional_deps:
        try:
            __import__(dep.replace('-', '_'))
            print(f"   ✅ {dep} - Instalada")
        except ImportError:
            print(f"   ⚠️ {dep} - No instalada (opcional)")

def test_server_startup():
    """Intenta iniciar el servidor y captura errores específicos"""
    print("\n🚀 Probando inicio del servidor...")
    
    try:
        # Intentar importar el módulo principal
        print("   Importando app_ddd...")
        import app_ddd
        print("   ✅ app_ddd importado correctamente")
        
        # Verificar que la aplicación Flask se creó
        if hasattr(app_ddd, 'app'):
            print("   ✅ Aplicación Flask creada")
        else:
            print("   ❌ Aplicación Flask no encontrada")
            return False
        
        # Verificar que Barbara se inicializó
        if hasattr(app_ddd, 'barbara'):
            print("   ✅ Barbara inicializada")
        else:
            print("   ❌ Barbara no inicializada")
            return False
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error durante inicialización: {e}")
        return False

def test_server_health():
    """Prueba si el servidor responde en el puerto 5000"""
    print("\n🏥 Probando health check...")
    
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Servidor respondiendo correctamente")
            return True
        else:
            print(f"   ❌ Servidor respondió con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ No se puede conectar al servidor (puerto 5000)")
        return False
    except Exception as e:
        print(f"   ❌ Error en health check: {e}")
        return False

def main():
    """Función principal de diagnóstico"""
    print("🔍 DIAGNÓSTICO COMPLETO DEL SERVIDOR BARBARA")
    print("=" * 50)
    
    # Verificaciones básicas
    if not check_python_version():
        return
    
    if not check_environment_file():
        return
    
    if not check_dependencies():
        return
    
    check_optional_dependencies()
    
    # Verificar inicio del servidor
    if not test_server_startup():
        print("\n❌ El servidor no puede iniciarse debido a errores de importación/inicialización")
        print("   Revisa los errores anteriores y asegúrate de que todas las dependencias estén instaladas")
        return
    
    # Verificar si el servidor está ejecutándose
    if not test_server_health():
        print("\n⚠️ El servidor no está ejecutándose en el puerto 5000")
        print("   Ejecuta: python app_ddd.py")
        return
    
    print("\n✅ DIAGNÓSTICO COMPLETADO - TODO FUNCIONANDO")
    print("   El servidor está listo para usar")

if __name__ == "__main__":
    main() 