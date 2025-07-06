#!/usr/bin/env python3
"""
📦 INSTALADOR DE DEPENDENCIAS BÁSICAS
Script para instalar las dependencias mínimas necesarias para Barbara
Basado en las mejores prácticas de gestión de dependencias de Python
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"   Salida: {e.stdout}")
        print(f"   Error: {e.stderr}")
        return False

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

def upgrade_pip():
    """Actualiza pip y setuptools"""
    print("\n📦 Actualizando herramientas de instalación...")
    
    commands = [
        (f"{sys.executable} -m pip install --upgrade pip", "Actualizando pip"),
        (f"{sys.executable} -m pip install --upgrade setuptools", "Actualizando setuptools")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            print(f"⚠️ {description} falló, pero continuando...")

def install_basic_dependencies():
    """Instala las dependencias básicas"""
    print("\n📦 Instalando dependencias básicas...")
    
    basic_deps = [
        "flask>=2.3.0",
        "flask-cors>=4.0.0", 
        "requests>=2.30.0",
        "python-dotenv>=1.0.0",
        "twilio>=8.0.0"
    ]
    
    for dep in basic_deps:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Instalando {dep}"):
            print(f"⚠️ Error instalando {dep}, pero continuando...")

def install_optional_dependencies():
    """Instala dependencias opcionales"""
    print("\n🔍 Instalando dependencias opcionales...")
    
    optional_deps = [
        "markdown>=3.4.0",
        "jinja2>=3.0.0"
    ]
    
    for dep in optional_deps:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Instalando {dep}"):
            print(f"⚠️ Error instalando {dep} (opcional)")

def create_requirements_file():
    """Crea un archivo requirements.txt básico"""
    print("\n📄 Creando archivo requirements.txt...")
    
    requirements_content = """# Dependencias básicas para Barbara
flask>=2.3.0
flask-cors>=4.0.0
requests>=2.30.0
python-dotenv>=1.0.0
twilio>=8.0.0
markdown>=3.4.0
jinja2>=3.0.0

# Dependencias opcionales (comentadas para evitar problemas)
# spacy>=3.8.0
# psycopg2-binary>=2.9.0
# openai>=1.0.0
"""
    
    try:
        with open("requirements_basic.txt", "w") as f:
            f.write(requirements_content)
        print("✅ Archivo requirements_basic.txt creado")
        return True
    except Exception as e:
        print(f"❌ Error creando requirements_basic.txt: {e}")
        return False

def test_imports():
    """Prueba que las importaciones funcionen"""
    print("\n🧪 Probando importaciones...")
    
    test_imports = [
        ("flask", "Flask"),
        ("flask_cors", "CORS"),
        ("requests", "requests"),
        ("dotenv", "load_dotenv")
    ]
    
    failed_imports = []
    
    for module, import_name in test_imports:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️ Importaciones fallidas: {', '.join(failed_imports)}")
        return False
    else:
        print("\n✅ Todas las importaciones funcionan correctamente")
        return True

def main():
    """Función principal"""
    print("📦 INSTALADOR DE DEPENDENCIAS BÁSICAS PARA BARBARA")
    print("=" * 50)
    print("Basado en las mejores prácticas de gestión de dependencias de Python")
    print("Referencia: https://levelup.gitconnected.com/10-ways-to-fix-python-dependency-problems-53db25ccfef2")
    print("=" * 50)
    
    # Verificar versión de Python
    if not check_python_version():
        print("\n❌ Versión de Python incompatible. Saliendo...")
        return
    
    # Actualizar herramientas
    upgrade_pip()
    
    # Instalar dependencias básicas
    install_basic_dependencies()
    
    # Instalar dependencias opcionales
    install_optional_dependencies()
    
    # Crear archivo de requirements
    create_requirements_file()
    
    # Probar importaciones
    if test_imports():
        print("\n🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
        print("=" * 50)
        print("✅ Dependencias básicas instaladas")
        print("✅ Herramientas actualizadas")
        print("✅ Archivo requirements_basic.txt creado")
        print("✅ Todas las importaciones funcionan")
        print("\n🚀 Ahora puedes ejecutar:")
        print("   python app_simple.py")
        print("\n📖 Para más información sobre gestión de dependencias:")
        print("   https://levelup.gitconnected.com/10-ways-to-fix-python-dependency-problems-53db25ccfef2")
    else:
        print("\n⚠️ Algunas dependencias no se instalaron correctamente")
        print("   Revisa los errores anteriores e intenta instalar manualmente")

if __name__ == "__main__":
    main() 