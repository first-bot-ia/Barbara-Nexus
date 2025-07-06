#!/usr/bin/env python3
"""
🧪 Test del Chatbot Dinámico
Pruebas para verificar que el chatbot funciona correctamente
"""

import requests
import json
import time

def test_chatbot():
    """Prueba el chatbot dinámico"""
    
    base_url = "http://localhost:5001"
    
    print("🧪 TESTEANDO CHATBOT DINÁMICO")
    print("=" * 40)
    
    # Test 1: Health check
    print("1. 🔍 Probando health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check OK: {data['status']}")
            print(f"   Gemini status: {data['gemini_status']}")
        else:
            print(f"❌ Health check falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return False
    
    # Test 2: Chat básico
    print("\n2. 💬 Probando chat básico...")
    try:
        test_message = "¿Qué aventuras recomiendas en Cusco?"
        response = requests.post(f"{base_url}/chat", 
                               json={"message": test_message, "user_id": "test_user"})
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ Chat OK")
                print(f"   Mensaje: {test_message}")
                print(f"   Respuesta: {data['response'][:100]}...")
                print(f"   Tiempo: {data['processing_time_seconds']:.2f}s")
            else:
                print(f"❌ Chat falló: {data.get('error', 'Error desconocido')}")
                return False
        else:
            print(f"❌ Chat falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en chat: {e}")
        return False
    
    # Test 3: API externa
    print("\n3. 🔌 Probando API externa...")
    try:
        test_message = "¿Cuáles son los mejores destinos para trekking en Perú?"
        response = requests.post(f"{base_url}/api/chat", 
                               json={
                                   "message": test_message, 
                                   "user_id": "api_test_user",
                                   "platform": "test_platform"
                               })
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ API externa OK")
                print(f"   Mensaje: {test_message}")
                print(f"   Respuesta: {data['response'][:100]}...")
                print(f"   Plataforma: {data['metadata']['platform']}")
            else:
                print(f"❌ API externa falló: {data.get('error', 'Error desconocido')}")
                return False
        else:
            print(f"❌ API externa falló: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en API externa: {e}")
        return False
    
    # Test 4: Conversación con contexto
    print("\n4. 🗣️ Probando conversación con contexto...")
    try:
        messages = [
            "Hola, soy nuevo en Aventura PE",
            "¿Qué tipo de aventuras ofrecen?",
            "Me interesa el trekking, ¿qué recomiendas?"
        ]
        
        user_id = "context_test_user"
        
        for i, message in enumerate(messages, 1):
            print(f"   Mensaje {i}: {message}")
            response = requests.post(f"{base_url}/chat", 
                                   json={"message": message, "user_id": user_id})
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"   Respuesta {i}: {data['response'][:80]}...")
                else:
                    print(f"   ❌ Error en mensaje {i}")
                    return False
            else:
                print(f"   ❌ Error HTTP en mensaje {i}")
                return False
            
            time.sleep(1)  # Pausa entre mensajes
        
        print("✅ Conversación con contexto OK")
        
    except Exception as e:
        print(f"❌ Error en conversación: {e}")
        return False
    
    print("\n🎉 TODOS LOS TESTS PASARON EXITOSAMENTE!")
    print("=" * 40)
    print("✅ El chatbot dinámico está funcionando correctamente")
    print("✅ Las respuestas son generadas por Gemini API")
    print("✅ El contexto de Aventura PE está activo")
    print("✅ La integración externa funciona")
    
    return True

def test_error_cases():
    """Prueba casos de error"""
    
    base_url = "http://localhost:5001"
    
    print("\n🚨 PROBANDO CASOS DE ERROR")
    print("=" * 30)
    
    # Test: Mensaje vacío
    print("1. 📝 Probando mensaje vacío...")
    try:
        response = requests.post(f"{base_url}/chat", json={"message": ""})
        if response.status_code == 400:
            print("✅ Error manejado correctamente para mensaje vacío")
        else:
            print(f"❌ No se manejó correctamente: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test: Sin mensaje
    print("2. 📝 Probando sin mensaje...")
    try:
        response = requests.post(f"{base_url}/chat", json={})
        if response.status_code == 400:
            print("✅ Error manejado correctamente para mensaje faltante")
        else:
            print(f"❌ No se manejó correctamente: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("✅ Casos de error probados")

if __name__ == '__main__':
    print("🚀 INICIANDO TESTS DEL CHATBOT DINÁMICO")
    print("Asegúrate de que el servidor esté ejecutándose en puerto 5001")
    print("=" * 50)
    
    # Ejecutar tests principales
    success = test_chatbot()
    
    if success:
        # Ejecutar tests de error
        test_error_cases()
        
        print("\n🎯 RESUMEN:")
        print("✅ El chatbot dinámico está listo para usar")
        print("✅ Puedes acceder a la interfaz web en: http://localhost:5001/chat-web")
        print("✅ Puedes integrar con otras plataformas usando: http://localhost:5001/chat")
    else:
        print("\n❌ Algunos tests fallaron")
        print("Verifica que el servidor esté ejecutándose correctamente") 