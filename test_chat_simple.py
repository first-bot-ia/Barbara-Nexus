#!/usr/bin/env python3
"""
Test Chat Simple
"""

import requests
import json

print("🔧 TEST CHAT SIMPLE")
print("=" * 30)

# Payload simple
payload = {
    'message': 'hola',
    'phone': '+51999TEST'
}

try:
    print("📤 Enviando mensaje simple...")
    
    response = requests.post("http://localhost:5000/test-chat", 
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"📥 Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ ÉXITO!")
        print(f"📝 Respuesta: {data.get('bot_response', 'N/A')[:50]}...")
        
        if 'nexus_metrics' in data:
            print("📊 MÉTRICAS REALES ENCONTRADAS!")
            metrics = data['nexus_metrics']
            for key, value in metrics.items():
                print(f"   {key}: {value}")
        else:
            print("⚠️ No hay métricas")
            
    else:
        print("❌ ERROR!")
        print(response.text)
        
except Exception as e:
    print(f"❌ Error: {e}") 