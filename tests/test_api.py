#!/usr/bin/env python3
"""
🧪 Test API - Prueba simple del endpoint de API de Barbara
"""

import requests
import json

def test_health_endpoint():
    """Prueba el endpoint de health"""
    try:
        print("Intentando conectar al servidor...")
        response = requests.get("http://localhost:5000/aventurape/health", timeout=5)
        print(f"Health endpoint status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except requests.exceptions.Timeout:
        print("❌ Timeout: El servidor no respondió en 5 segundos")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ Error testing health endpoint: {e}")
        return False

def test_generate_content():
    """Prueba el endpoint de generación de contenido"""
    try:
        data = {
            "activity_type": "hiking",
            "location": "Cusco",
            "duration": "2 days"
        }
        
        print("Intentando generar contenido...")
        response = requests.post(
            "http://localhost:5000/aventurape/generate-content",
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
            timeout=10
        )
        
        print(f"Generate content status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Generated title: {result.get('title', 'N/A')}")
            print(f"Generated description: {result.get('description', 'N/A')}")
        
        return response.status_code == 200
    except requests.exceptions.Timeout:
        print("❌ Timeout: El servidor no respondió en 10 segundos")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Error de conexión: No se pudo conectar al servidor")
        return False
    except Exception as e:
        print(f"❌ Error testing generate content: {e}")
        return False

def main():
    """Función principal"""
    print("🧪 TEST API DE BARBARA")
    print("=" * 40)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    health_ok = test_health_endpoint()
    
    # Test generate content endpoint
    print("\n2. Testing generate content endpoint...")
    content_ok = test_generate_content()
    
    print(f"\n=== Results ===")
    print(f"Health endpoint: {'✅ OK' if health_ok else '❌ FAILED'}")
    print(f"Generate content: {'✅ OK' if content_ok else '❌ FAILED'}")
    
    if health_ok and content_ok:
        print("\n🎉 All tests passed! Barbara-Nexus is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the server logs for more details.")

if __name__ == "__main__":
    main() 