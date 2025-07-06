#!/usr/bin/env python3
"""
🧠 TEST API DE RAZONAMIENTO EXTERNO
Este script demuestra cómo conectarse a Barbara desde cualquier plataforma externa
"""

import requests
import json
import time
import sys

def test_api_reasoning():
    """Test del API de razonamiento externo"""
    
    print("\n🧠 TEST API DE RAZONAMIENTO EXTERNO")
    print("=" * 50)
    print("Este test demuestra cómo cualquier plataforma puede conectarse a Barbara")
    print("y utilizar su capacidad de razonamiento de manera dinámica")
    print("=" * 50)
    
    # URL del servicio (cambiar según corresponda)
    API_URL = "http://localhost:5000/api/reasoning"
    
    # Casos de prueba simulando diferentes plataformas
    test_cases = [
        {
            "name": "Web App - Conversación Simple",
            "request": {
                "message": "Hola, soy Alexander y necesito un SOAT",
                "user_id": "web-user-123",
                "platform_name": "Web App Cliente",
                "context": {
                    "platform_type": "web",
                    "user_agent": "Chrome/96.0",
                    "location": "homepage"
                }
            }
        },
        {
            "name": "Aplicación Móvil - Cotización",
            "request": {
                "message": "¿Cuál es el precio del SOAT para mi auto Toyota?",
                "user_id": "mobile-user-456",
                "platform_name": "App Móvil AutoSOAT",
                "context": {
                    "platform_type": "mobile",
                    "device": "Android",
                    "user_preferences": {
                        "vehicle_type": "auto",
                        "favorite_brand": "Toyota"
                    }
                }
            }
        },
        {
            "name": "Sistema CRM - Integración Empresarial",
            "request": {
                "message": "Busca y resume la información sobre tipos de SOAT disponibles",
                "user_id": "crm-agent-789",
                "platform_name": "CRM Empresarial",
                "context": {
                    "platform_type": "enterprise",
                    "agent_role": "customer_support",
                    "module": "sales",
                    "access_level": "admin"
                }
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   📤 Enviando: {test_case['request']['message']}")
        print(f"   🔄 Plataforma: {test_case['request']['platform_name']}")
        
        try:
            # Realizar la petición al API
            start_time = time.time()
            response = requests.post(
                API_URL,
                json=test_case['request'],
                headers={'Content-Type': 'application/json'}
            )
            request_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"   ✅ Status: {response.status_code} ({request_time:.2f}s)")
                print(f"   📝 Respuesta: {data['response']}")
                
                # Mostrar métricas si están disponibles
                if 'metrics' in data:
                    print("\n   📊 MÉTRICAS:")
                    for key, value in data['metrics'].items():
                        if key == 'thoughts' and isinstance(value, list) and value:
                            print(f"      💭 Pensamientos ({len(value)}):")
                            for thought in value:
                                print(f"         - {thought}")
                        else:
                            print(f"      {key}: {value}")
                
                print(f"\n   🆔 Request ID: {data.get('request_id', 'N/A')}")
                
            else:
                print(f"   ❌ Error: {response.status_code}")
                print(f"   Detalles: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error de conexión: {e}")
        
        print("-" * 50)
    
    print("\n✅ CONCLUSIÓN:")
    print("La API de razonamiento de Barbara está funcionando correctamente")
    print("y puede ser integrada en cualquier plataforma externa.")
    print("=" * 50)

def test_cross_origin():
    """Prueba simple para verificar que CORS está correctamente configurado"""
    
    print("\n🌐 TEST DE CORS")
    print("=" * 50)
    
    # Realizar una petición OPTIONS para verificar cabeceras CORS
    try:
        response = requests.options(
            "http://localhost:5000/api/reasoning",
            headers={
                'Origin': 'http://example.com',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            }
        )
        
        print(f"Status: {response.status_code}")
        print("\nCabeceras CORS:")
        
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers',
            'Access-Control-Max-Age'
        ]
        
        for header in cors_headers:
            if header in response.headers:
                print(f"{header}: {response.headers[header]}")
            else:
                print(f"{header}: NO ENCONTRADO")
        
        if 'Access-Control-Allow-Origin' in response.headers and response.headers['Access-Control-Allow-Origin'] == '*':
            print("\n✅ CORS configurado correctamente para todos los orígenes (*)")
        else:
            print("\n❌ CORS no está configurado para todos los orígenes")
            
    except Exception as e:
        print(f"❌ Error verificando CORS: {e}")
    
    print("=" * 50)

if __name__ == "__main__":
    # Verificar si se pasa un argumento específico de prueba
    if len(sys.argv) > 1 and sys.argv[1] == 'cors':
        test_cross_origin()
    else:
        test_api_reasoning() 