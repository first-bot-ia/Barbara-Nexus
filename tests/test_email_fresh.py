"""
🔄 TEST EMAIL FRESH - CON TELÉFONO NUEVO
Prueba el flujo completo con número totalmente nuevo para evitar memoria corrupta
"""

import requests
import json
import time
import uuid

def test_email_fresh():
    """Prueba con teléfono completamente nuevo"""
    
    base_url = "http://localhost:5000/test-chat"
    headers = {"Content-Type": "application/json"}
    
    # Generar teléfono único
    unique_id = uuid.uuid4().hex[:6]
    phone = f"+519{unique_id}"  # Teléfono único cada vez
    
    print(f"🔄 INICIANDO PRUEBA FRESH CON TELÉFONO: {phone}")
    print("=" * 60)
    
    # Flujo paso a paso CORRECTO
    steps = [
        ("hola", "Saludo inicial"),
        ("Fernando", "Proporcionar nombre"),
        ("quiero cotizar SOAT", "Solicitar cotización"), 
        ("auto", "Tipo de vehículo"),
        ("2023", "Año del vehículo"),
        ("particular", "Uso del vehículo"),
        ("Lima", "Ciudad - Generar cotización"),
        ("si quiero por correo", "Confirmar envío email"),
        ("fernando.test@gmail.com", "🎯 EMAIL REAL - MOMENTO CRÍTICO")
    ]
    
    for i, (message, description) in enumerate(steps, 1):
        try:
            print(f"\n--- PASO {i}: {description} ---")
            print(f"📤 Enviando: '{message}' al teléfono {phone}")
            
            # Enviar mensaje
            payload = {"message": message, "phone": phone}
            response = requests.post(base_url, headers=headers, json=payload, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                barbara_response = data.get("bot_response", "Sin respuesta")
                print(f"📥 Barbara: {barbara_response[:150]}...")
                
                # 🎯 VERIFICACIÓN ESPECIAL EN ÚLTIMO PASO
                if i == len(steps):
                    print("\n" + "="*50)
                    print("🚨 MOMENTO CRÍTICO - VERIFICANDO ENVÍO")
                    print("="*50)
                    
                    if "enviado" in barbara_response.lower() or "he enviado" in barbara_response.lower():
                        print("✅ BARBARA CONFIRMÓ EL ENVÍO!")
                        print("🔔 VERIFICAR LOGS DEL SERVIDOR PARA:")
                        print("   - 🚀 INICIANDO ENVÍO DE EMAIL VIA MAILTRAP")
                        print("   - 📧 ENVIANDO EMAIL REAL")
                        print("   - 🎉 EMAIL ENVIADO EXITOSAMENTE")
                        print(f"📧 EMAIL: fernando.test@gmail.com")
                    else:
                        print("❌ BARBARA NO CONFIRMÓ EL ENVÍO")
                    
                    print(f"\n🔍 RESPUESTA COMPLETA:")
                    print(f"{barbara_response}")
                
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                
            # Pausa más corta
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error en paso {i}: {e}")
    
    print(f"\n🔄 PRUEBA FRESH COMPLETADA - Teléfono: {phone}")

if __name__ == "__main__":
    test_email_fresh() 