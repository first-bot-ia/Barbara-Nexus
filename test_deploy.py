#!/usr/bin/env python3
"""
Script de prueba para verificar que la aplicación funciona correctamente
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.env')

def test_app_import():
    """Prueba que la aplicación se puede importar correctamente"""
    try:
        from chatbot_dinamico import app
        print("✅ Importación de la aplicación exitosa")
        return True
    except Exception as e:
        print(f"❌ Error importando la aplicación: {e}")
        return False

def test_env_variables():
    """Prueba que las variables de entorno están configuradas"""
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("✅ GEMINI_API_KEY configurada")
        return True
    else:
        print("❌ GEMINI_API_KEY no configurada")
        return False

def test_app_routes():
    """Prueba que las rutas de la aplicación están definidas"""
    try:
        from chatbot_dinamico import app
        
        # Verificar rutas principales
        routes = ['/', '/health', '/chat', '/api/chat', '/chat-web']
        for route in routes:
            if route in [str(rule) for rule in app.url_map.iter_rules()]:
                print(f"✅ Ruta {route} encontrada")
            else:
                print(f"❌ Ruta {route} no encontrada")
                return False
        return True
    except Exception as e:
        print(f"❌ Error verificando rutas: {e}")
        return False

def test_local_server():
    """Prueba que el servidor local funciona"""
    try:
        from chatbot_dinamico import app
        
        # Crear un cliente de prueba
        with app.test_client() as client:
            # Probar health check
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ Health check funcionando")
            else:
                print(f"❌ Health check falló: {response.status_code}")
                return False
            
            # Probar página principal
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Página principal funcionando")
            else:
                print(f"❌ Página principal falló: {response.status_code}")
                return False
                
        return True
    except Exception as e:
        print(f"❌ Error probando servidor local: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 Iniciando pruebas de la aplicación...")
    print("=" * 50)
    
    tests = [
        ("Importación de la aplicación", test_app_import),
        ("Variables de entorno", test_env_variables),
        ("Rutas de la aplicación", test_app_routes),
        ("Servidor local", test_local_server)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Probando: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} falló")
    
    print("\n" + "=" * 50)
    print(f"📊 Resultados: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! La aplicación está lista para desplegar.")
        return True
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores antes de desplegar.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 