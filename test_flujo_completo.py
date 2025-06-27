"""
🧪 TEST FLUJO COMPLETO BARBARA
Prueba el flujo exacto que quiere el usuario incluyendo correo
"""

import requests
import json
import time

def test_flujo_completo_correo():
    """Prueba el flujo conversacional completo con correo"""
    
    base_url = "http://localhost:5000/test-chat"
    headers = {"Content-Type": "application/json"}
    phone = "+51999FLUJO"
    
    # Secuencia de prueba COMPLETA
    conversacion = [
        ("hola", "✅ Saludo inicial"),
        ("Pedro", "✅ Captura nombre"),
        ("si cotizar", "✅ Confirma cotización"),
        ("auto", "✅ Especifica vehículo"),
        ("2023", "✅ Especifica año"),
        ("particular", "✅ Especifica uso"),
        ("Lima", "✅ Especifica ciudad + genera cotización"),
        ("si mandalo", "✅ Confirma envío por correo"),
        ("pedro123@gmail.com", "✅ Proporciona correo")
    ]
    
    print("🧪 PROBANDO FLUJO COMPLETO CON CORREO")
    print("=" * 60)
    
    for i, (mensaje, descripcion) in enumerate(conversacion, 1):
        try:
            # Enviar mensaje
            payload = {"message": mensaje, "phone": phone}
            response = requests.post(base_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                bot_response = data.get("bot_response", "Sin respuesta")
                
                print(f"\n{i}. Usuario: '{mensaje}'")
                print(f"   {descripcion}")
                
                # Mostrar respuesta de Barbara (truncada)
                if len(bot_response) > 150:
                    print(f"   Barbara: '{bot_response[:150]}...'")
                else:
                    print(f"   Barbara: '{bot_response}'")
                
                # Verificaciones específicas
                if i == 7:  # Después de Lima
                    if "correo electrónico" in bot_response.lower():
                        print("   🎯 ¡PERFECTO! Pregunta por correo automáticamente")
                    else:
                        print("   ❌ ERROR: No pregunta por correo")
                        
                elif i == 8:  # Después de confirmar correo
                    if "correo electrónico" in bot_response.lower() or "@" in bot_response:
                        print("   ✅ Solicita dirección de correo")
                    else:
                        print("   ❌ ERROR: No solicita correo específico")
                        
                elif i == 9:  # Después de dar correo
                    if "enviado" in bot_response.lower() or "bandeja" in bot_response.lower():
                        print("   🎉 ¡ÉXITO! Confirma envío por correo")
                    else:
                        print("   ❌ ERROR: No confirma envío")
                
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                break
                
            time.sleep(0.8)  # Pausa realista
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            break
    
    print("\n" + "=" * 60)
    print("🧪 PRUEBA FLUJO COMPLETO TERMINADA")

if __name__ == "__main__":
    test_flujo_completo_correo() 