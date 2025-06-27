"""
🧪 TEST BARBARA CORREGIDA
Prueba el sistema para verificar que no haya bucles infinitos
"""

import requests
import json
import time

def test_barbara_conversation():
    """Prueba el flujo conversacional completo"""
    
    base_url = "http://localhost:5000/test-chat"
    headers = {"Content-Type": "application/json"}
    phone = "+51999CORREGIDA"
    
    # Secuencia de prueba
    messages = [
        "hola",
        "Juan",
        "si",
        "si quiero",
        "auto",
        "2020",
        "particular",
        "Lima"
    ]
    
    print("🧪 INICIANDO PRUEBA BARBARA CORREGIDA")
    print("=" * 50)
    
    for i, message in enumerate(messages, 1):
        try:
            # Enviar mensaje
            payload = {"message": message, "phone": phone}
            response = requests.post(base_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get("bot_response", "Sin respuesta")
                
                print(f"\n{i}. Usuario: '{message}'")
                print(f"   Barbara: '{bot_response[:100]}...' " if len(bot_response) > 100 else f"   Barbara: '{bot_response}'")
                
                # Verificar si hay bucle
                if i > 2 and "¿Necesitas una cotización SOAT?" in bot_response:
                    print("   ❌ POSIBLE BUCLE DETECTADO!")
                elif "tipo de vehículo" in bot_response or "año" in bot_response or "uso" in bot_response:
                    print("   ✅ FLUJO PASO A PASO FUNCIONANDO")
                elif "COTIZACIÓN SOAT" in bot_response:
                    print("   ✅ COTIZACIÓN GENERADA CORRECTAMENTE")
                
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                
            time.sleep(0.5)  # Pausa corta
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🧪 PRUEBA COMPLETADA")

if __name__ == "__main__":
    test_barbara_conversation() 