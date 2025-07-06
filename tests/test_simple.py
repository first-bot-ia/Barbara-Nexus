#!/usr/bin/env python3
"""
🔧 Test Ultra Simple - Solo verificar que el servidor responde
"""

import requests
import json

def test_health():
    """Prueba simple del endpoint de health"""
    try:
        print("🔍 Probando endpoint de health...")
        # Usar 127.0.0.1 en lugar de localhost
        response = requests.get("http://127.0.0.1:5000/aventurape/health", timeout=3)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Respuesta: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_generate_content():
    """Prueba simple del endpoint de generación de contenido"""
    try:
        print("\n🔍 Probando generación de contenido...")
        data = {
            "context": "Aventura de senderismo en Cusco por 2 días, incluyendo visitas a sitios arqueológicos y paisajes montañosos"
        }
        
        response = requests.post(
            "http://127.0.0.1:5000/aventurape/generate-content",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
            timeout=10
        )
        
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Respuesta: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                content = result.get('content', {})
                print(f"🎯 Título generado: {content.get('title', 'N/A')}")
                print(f"📝 Descripción generada: {content.get('description', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 PRUEBA RÁPIDA DE BARBARA-NEXUS AVENTURAPE")
    print("=" * 50)
    
    # Probar health endpoint
    health_ok = test_health()
    
    # Probar generación de contenido
    content_ok = test_generate_content()
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS:")
    print(f"Health endpoint: {'✅ OK' if health_ok else '❌ FALLÓ'}")
    print(f"Generación de contenido: {'✅ OK' if content_ok else '❌ FALLÓ'}")
    
    if health_ok and content_ok:
        print("\n🎉 ¡Todo funciona perfectamente!")
    else:
        print("\n⚠️  Algunas pruebas fallaron") 