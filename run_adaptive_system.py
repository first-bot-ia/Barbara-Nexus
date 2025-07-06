#!/usr/bin/env python3
"""
🚀 SCRIPT PARA EJECUTAR BARBARA ADAPTIVE SYSTEM
Este script ejecuta Barbara con el sistema adaptativo y configura ngrok
"""

import os
import sys
import subprocess
import time
import requests
import json
from pathlib import Path

def check_requirements():
    """Verifica que los requisitos estén instalados"""
    print("🔍 Verificando requisitos...")
    
    try:
        import flask
        import flask_cors
        import requests
        print("✅ Dependencias Python OK")
    except ImportError as e:
        print(f"❌ Falta dependencia: {e}")
        print("Ejecuta: pip install -r config/requirements.txt")
        return False
    
    # Verificar archivo .env
    if not os.path.exists('.env'):
        print("⚠️ Archivo .env no encontrado")
        print("Crea un archivo .env con:")
        print("GEMINI_API_KEY=tu_api_key_aqui")
        return False
    
    return True

def setup_ngrok():
    """Configura ngrok para exponer el servicio"""
    print("\n🌐 Configurando ngrok...")
    
    ngrok_path = Path("ngrok/ngrok.exe")
    if not ngrok_path.exists():
        print("❌ ngrok.exe no encontrado en la carpeta ngrok/")
        print("Descarga ngrok desde: https://ngrok.com/download")
        return None
    
    try:
        # Verificar si ngrok está configurado
        result = subprocess.run([str(ngrok_path), "version"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ ngrok encontrado y funcional")
            
            # Iniciar ngrok en segundo plano
            print("🚀 Iniciando ngrok...")
            ngrok_process = subprocess.Popen([
                str(ngrok_path), "http", "5000"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Esperar a que ngrok se inicie
            time.sleep(3)
            
            # Obtener URL pública
            try:
                response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
                if response.status_code == 200:
                    tunnels = response.json()['tunnels']
                    if tunnels:
                        public_url = tunnels[0]['public_url']
                        print(f"✅ ngrok iniciado: {public_url}")
                        return ngrok_process, public_url
            except:
                pass
            
            print("⚠️ No se pudo obtener la URL de ngrok, pero el proceso está ejecutándose")
            return ngrok_process, "http://localhost:5000"
            
        else:
            print("❌ Error con ngrok")
            return None
            
    except Exception as e:
        print(f"❌ Error configurando ngrok: {e}")
        return None

def start_barbara_server():
    """Inicia el servidor de Barbara"""
    print("\n🧠 Iniciando Barbara Adaptive System...")
    
    try:
        # Ejecutar el servidor Flask
        server_process = subprocess.Popen([
            sys.executable, "app_ddd.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar a que el servidor se inicie
        time.sleep(5)
        
        # Verificar que el servidor esté funcionando
        try:
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Servidor Barbara iniciado correctamente")
                return server_process
            else:
                print("❌ Servidor no responde correctamente")
                return None
        except:
            print("❌ No se pudo conectar al servidor")
            return None
            
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
        return None

def test_adaptive_system():
    """Prueba el sistema adaptativo"""
    print("\n🧪 Probando sistema adaptativo...")
    
    test_cases = [
        {
            "name": "🛒 E-commerce",
            "message": "¿Tienes productos en oferta?",
            "context": {"platform_type": "ecommerce"}
        },
        {
            "name": "🎧 Servicio al Cliente", 
            "message": "Tengo un problema con mi cuenta",
            "context": {"platform_type": "customer_service"}
        },
        {
            "name": "📚 Educativa",
            "message": "¿Puedes explicarme cómo funciona esto?",
            "context": {"platform_type": "educational"}
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}:")
        print(f"  Mensaje: {test_case['message']}")
        
        try:
            response = requests.post("http://localhost:5000/api/reasoning", 
                                   json={
                                       "message": test_case['message'],
                                       "user_id": "test_user",
                                       "context": test_case['context']
                                   }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"  ✅ Respuesta: {data['response'][:80]}...")
                    print(f"  🎯 Plataforma: {data.get('platform_detected', 'N/A')}")
                    print(f"  🎭 Personalidad: {data.get('personality_adapted', 'N/A')}")
                else:
                    print(f"  ❌ Error: {data.get('error', 'Error desconocido')}")
            else:
                print(f"  ❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        time.sleep(1)

def show_usage_info(public_url):
    """Muestra información de uso"""
    print("\n" + "="*60)
    print("🎉 ¡BARBARA ADAPTIVE SYSTEM ESTÁ FUNCIONANDO!")
    print("="*60)
    
    print(f"\n🌐 URLs de acceso:")
    print(f"  📱 Chat Adaptativo: {public_url}/chat-adaptive")
    print(f"  🧠 Chat Avanzado: {public_url}/chat-advanced")
    print(f"  💬 Chat Básico: {public_url}/chat-test")
    print(f"  🏠 Página Principal: {public_url}/")
    print(f"  📚 Documentación API: {public_url}/api-docs")
    
    print(f"\n🔧 API Endpoints:")
    print(f"  🧠 Razonamiento: POST {public_url}/api/reasoning")
    print(f"  📊 Info del Servicio: GET {public_url}/service-info")
    print(f"  ❤️ Health Check: GET {public_url}/health")
    
    print(f"\n🧪 Pruebas:")
    print(f"  📋 Ejecutar pruebas: python tests/test_adaptive_system.py")
    print(f"  🔥 Escenarios masivos: POST {public_url}/run-scenarios")
    
    print(f"\n📖 Documentación:")
    print(f"  📄 Sistema Adaptativo: ADAPTIVE_SYSTEM_README.md")
    print(f"  🔗 Integración API: API_INTEGRATION.md")
    
    print(f"\n⚠️ IMPORTANTE:")
    print(f"  • Mantén esta terminal abierta para que el servidor siga funcionando")
    print(f"  • Para detener: Ctrl+C")
    print(f"  • Los logs aparecerán en esta terminal")

def main():
    """Función principal"""
    print("🚀 INICIANDO BARBARA ADAPTIVE SYSTEM")
    print("="*50)
    
    # Verificar requisitos
    if not check_requirements():
        print("\n❌ No se pueden cumplir los requisitos. Saliendo...")
        return
    
    # Iniciar servidor Barbara
    server_process = start_barbara_server()
    if not server_process:
        print("\n❌ No se pudo iniciar el servidor. Saliendo...")
        return
    
    # Configurar ngrok
    ngrok_result = setup_ngrok()
    if ngrok_result:
        ngrok_process, public_url = ngrok_result
    else:
        ngrok_process = None
        public_url = "http://localhost:5000"
        print("⚠️ ngrok no disponible, usando localhost")
    
    # Probar sistema adaptativo
    test_adaptive_system()
    
    # Mostrar información de uso
    show_usage_info(public_url)
    
    try:
        # Mantener el script ejecutándose
        print(f"\n🔄 Servidor ejecutándose... Presiona Ctrl+C para detener")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Deteniendo servicios...")
        
        # Detener procesos
        if server_process:
            server_process.terminate()
            print("✅ Servidor Barbara detenido")
        
        if ngrok_process:
            ngrok_process.terminate()
            print("✅ ngrok detenido")
        
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    main() 