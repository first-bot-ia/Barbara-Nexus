#!/usr/bin/env python3
"""
🧪 Test simple del Chatbot Dinámico
"""

import requests
import json

def test_chat():
    """Prueba simple del chat"""
    
    url = "http://localhost:5001/chat"
    
    # Test 1: Pregunta sobre Cusco
    print("🧪 Probando chat dinámico...")
    print("=" * 40)
    
    data = {
        "message": "Que aventuras recomiendas en Cusco?",
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat funcionando!")
            print(f"📝 Mensaje: {data['message']}")
            print(f"🤖 Respuesta: {result['response']}")
            print(f"⏱️ Tiempo: {result['processing_time_seconds']:.2f}s")
            print(f"🎯 Contexto: {result['context']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_externa():
    """Prueba la API externa"""
    
    url = "http://localhost:5001/api/chat"
    
    print("\n🔌 Probando API externa...")
    print("=" * 30)
    
    data = {
        "message": "Cuales son los mejores destinos para trekking en Peru?",
        "user_id": "api_user",
        "platform": "test_platform"
    }
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API externa funcionando!")
            print(f"📝 Mensaje: {data['message']}")
            print(f"🤖 Respuesta: {result['response']}")
            print(f"🖥️ Plataforma: {result['metadata']['platform']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    print("🚀 TESTEANDO CHATBOT DINÁMICO")
    print("Asegúrate de que el servidor esté ejecutándose en puerto 5001")
    print("=" * 50)
    
    test_chat()
    test_api_externa()
    
    print("\n🎉 ¡Pruebas completadas!")
    print("✅ Puedes acceder a la interfaz web en: http://localhost:5001/chat-web") 