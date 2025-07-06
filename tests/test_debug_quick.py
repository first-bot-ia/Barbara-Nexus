#!/usr/bin/env python3
"""
🔍 DEBUG RÁPIDO - Métricas NEXUS
"""

import requests
import json

def test_debug_quick():
    """Test rápido para ver debug de métricas"""
    
    print("🔍 DEBUG RÁPIDO - MÉTRICAS NEXUS")
    print("=" * 40)
    
    try:
        response = requests.post("http://localhost:5000/test-chat", 
            json={
                'message': 'Test debug',
                'phone': '+51999DEBUG'
            })
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Respuesta recibida")
            print(f"📊 Métricas en respuesta: {'nexus_metrics' in data}")
            
            if 'nexus_metrics' in data:
                print(f"📊 Métricas: {data['nexus_metrics']}")
            else:
                print("❌ No hay métricas en la respuesta")
                print(f"🔍 Keys disponibles: {list(data.keys())}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_debug_quick() 