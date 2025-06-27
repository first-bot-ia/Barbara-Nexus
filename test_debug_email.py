"""
🔍 TEST DEBUG EMAIL - DIAGNÓSTICO ESPECÍFICO
Prueba paso a paso para identificar el problema del envío de emails
"""

import requests
import json
import time

def test_debug_email_flow():
    """Prueba específica para debug del flujo de email"""
    
    base_url = "http://localhost:5000/test-chat"
    headers = {"Content-Type": "application/json"}
    phone = "+51999DEBUG"  # Teléfono único para debug
    
    print("🔍 INICIANDO DEBUG DEL FLUJO DE EMAIL")
    print("=" * 60)
    
    # Flujo paso a paso para debug
    steps = [
        ("hola", "🔹 Saludo inicial"),
        ("TestUser", "🔹 Proporcionar nombre"),
        ("quiero cotizar", "🔹 Solicitar cotización"),
        ("auto", "🔹 Tipo de vehículo"),
        ("2022", "🔹 Año del vehículo"),
        ("particular", "🔹 Uso del vehículo"),
        ("Lima", "🔹 Ciudad (debería generar cotización)"),
        ("si envialo", "🔹 Confirmar envío por email"),
        ("debug@test.com", "🔹 EMAIL DEBUG - AQUÍ DEBERÍA ENVIARSE")
    ]
    
    for i, (message, description) in enumerate(steps, 1):
        try:
            print(f"\n--- PASO {i}: {description} ---")
            print(f"📤 Enviando: '{message}'")
            
            # Enviar mensaje
            payload = {"message": message, "phone": phone}
            response = requests.post(base_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                barbara_response = data.get("bot_response", "Sin respuesta")
                print(f"📥 Barbara responde: {barbara_response[:100]}...")
                
                # PUNTO CRÍTICO: Verificar si menciona envío de email
                if i == len(steps):  # Último paso - envío de email
                    print("\n🚨 MOMENTO CRÍTICO: VERIFICANDO ENVÍO DE EMAIL")
                    if "enviado" in barbara_response.lower():
                        print("✅ Barbara dice que envió el email - REVISAR LOGS")
                    else:
                        print("❌ Barbara NO confirmó el envío")
                        print(f"🔍 Respuesta completa: {barbara_response}")
                
            else:
                print(f"❌ Error HTTP: {response.status_code}")
                
            # Pausa entre mensajes
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error en paso {i}: {e}")
    
    print("\n🔍 DEBUG COMPLETADO")
    print("=" * 60)
    print("🔔 REVISAR LOGS DEL SERVIDOR PARA:")
    print("   - 🚀 INICIANDO ENVÍO DE EMAIL VIA MAILTRAP")
    print("   - ✅ Servicio Mailtrap importado")
    print("   - 📧 ENVIANDO EMAIL REAL")
    print("   - 🎉 EMAIL ENVIADO EXITOSAMENTE")

if __name__ == "__main__":
    # Esperar a que el servidor esté listo
    print("⏳ Esperando 3 segundos para que el servidor esté listo...")
    time.sleep(3)
    
    test_debug_email_flow() 