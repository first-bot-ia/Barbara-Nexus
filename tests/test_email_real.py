"""
🧪 TEST EMAIL REAL - CON TU EMAIL VERDADERO
Prueba específica usando jaircastillo2302@gmail.com para confirmar envío
"""

import requests
import json
import time
import uuid

def test_email_real():
    """Prueba con tu email real para confirmar que funciona"""
    
    base_url = "http://localhost:5000/test-chat"
    headers = {"Content-Type": "application/json"}
    
    # Generar teléfono único
    unique_id = uuid.uuid4().hex[:6]
    phone = f"+51EMAIL{unique_id}"  # Teléfono único
    
    print(f"🧪 PROBANDO CON TU EMAIL REAL")
    print(f"📱 Teléfono: {phone}")
    print("=" * 60)
    
    # Flujo paso a paso
    steps = [
        ("hola", "Saludo inicial"),
        ("Jair", "Tu nombre real"),
        ("quiero cotizar SOAT", "Solicitar cotización"),
        ("auto", "Tipo de vehículo"),
        ("2020", "Año del vehículo"), 
        ("particular", "Uso del vehículo"),
        ("Lima", "Ciudad - Generar cotización"),
        ("si envialo", "Confirmar envío email"),
        ("jaircastillo2302@gmail.com", "🎯 TU EMAIL REAL")
    ]
    
    for i, (message, description) in enumerate(steps, 1):
        try:
            print(f"\n--- PASO {i}: {description} ---")
            print(f"📤 Enviando: '{message}'")
            
            # Enviar mensaje
            payload = {"message": message, "phone": phone}
            response = requests.post(base_url, headers=headers, json=payload, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                barbara_response = data.get("bot_response", "Sin respuesta")
                print(f"📥 Barbara: {barbara_response[:100]}...")
                
                # VERIFICACIÓN FINAL
                if i == len(steps):
                    print("\n" + "="*60)
                    print("🎯 MOMENTO CRÍTICO - ENVÍO A TU EMAIL REAL")
                    print("="*60)
                    
                    if "enviado" in barbara_response.lower():
                        print("✅ BARBARA CONFIRMÓ EL ENVÍO!")
                        print("📧 Email enviado a: jaircastillo2302@gmail.com")
                        print("")
                        print("🔍 AHORA VERIFICA:")
                        print("   1. Tu bandeja de entrada en Gmail")
                        print("   2. Tu carpeta de SPAM")
                        print("   3. Espera 2-3 minutos por si hay demora")
                        print("")
                        print("📱 Si NO llega, hay un problema con Mailtrap")
                    else:
                        print("❌ BARBARA NO CONFIRMÓ EL ENVÍO")
                        print("🔍 PROBLEMA CON LA CONFIGURACIÓN")
                
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error en paso {i}: {e}")
    
    print(f"\n🧪 PRUEBA COMPLETADA - Teléfono: {phone}")

if __name__ == "__main__":
    test_email_real() 