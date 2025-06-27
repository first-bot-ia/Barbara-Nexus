"""
🧪 TEST FLUJO EMAIL REAL MAILTRAP
Prueba específica para verificar envío real de emails con Mailtrap
"""

import requests
import json
import time

def test_flujo_email_mailtrap():
    """Prueba flujo completo con envío real de email via Mailtrap"""
    
    base_url = "http://localhost:5000/test-chat"
    headers = {"Content-Type": "application/json"}
    phone = "+51999EMAIL"  # Teléfono único para esta prueba
    
    print("🧪 PROBANDO FLUJO COMPLETO CON MAILTRAP REAL")
    print("=" * 60)
    
    # Secuencia paso a paso manteniendo contexto
    steps = [
        ("hola", "Saludo inicial"),
        ("Roberto", "Proporcionar nombre"),
        ("quiero cotizar", "Solicitar cotización"),
        ("auto", "Tipo de vehículo"),
        ("2022", "Año del vehículo"),
        ("particular", "Uso del vehículo"),
        ("Lima", "Ciudad del vehículo"),
        ("si mandalo", "Confirmar envío por correo"),
        ("roberto.test@gmail.com", "Proporcionar correo - ENVÍO REAL")
    ]
    
    for i, (mensaje, descripcion) in enumerate(steps, 1):
        try:
            print(f"\n{i}. 👤 Usuario: '{mensaje}'")
            print(f"   📝 {descripcion}")
            
            # Enviar mensaje (siempre el mismo teléfono)
            payload = {"message": mensaje, "phone": phone}
            response = requests.post(base_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get("bot_response", "Sin respuesta")
                
                # Mostrar respuesta completa para debug
                print(f"   🤖 Barbara: '{bot_response[:200]}...' " if len(bot_response) > 200 else f"   🤖 Barbara: '{bot_response}'")
                
                # Verificaciones específicas por paso
                if i == 7:  # Después de Lima - debería generar cotización + preguntar por correo
                    if "correo electrónico" in bot_response.lower():
                        print("   ✅ CORRECTO: Pregunta por correo después de cotización")
                    else:
                        print("   ❌ ERROR: No pregunta por correo")
                        
                elif i == 8:  # Después de "si mandalo" - debería pedir correo específico
                    if "correo electrónico" in bot_response.lower() or "email" in bot_response.lower():
                        print("   ✅ CORRECTO: Pide correo específico")
                    else:
                        print("   ❌ ERROR: No pide correo específico")
                        
                elif i == 9:  # Después del correo - ENVÍO REAL
                    if "✅" in bot_response and "enviado" in bot_response.lower():
                        print("   🎉 ¡ÉXITO! EMAIL ENVIADO REALMENTE VIA MAILTRAP")
                        print("   📧 Verifica tu bandeja de entrada en roberto.test@gmail.com")
                    elif "problema" in bot_response.lower() or "error" in bot_response.lower():
                        print("   ⚠️ ERROR EN ENVÍO: Mailtrap reportó fallo")
                    else:
                        print("   ❌ RESPUESTA INESPERADA")
                
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                break
                
            # Pausa entre mensajes
            time.sleep(1.2)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            break
    
    print("\n" + "=" * 60)
    print("🧪 PRUEBA MAILTRAP TERMINADA")
    print("📧 Si ves '✅ EMAIL ENVIADO', verifica tu correo real!")

if __name__ == "__main__":
    test_flujo_email_mailtrap() 