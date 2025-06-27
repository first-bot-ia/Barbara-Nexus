"""
🔍 TEST DIAGNÓSTICO - PROBLEMA EMAIL BARBARA
============================================

Este test demuestra exactamente por qué no funcionan los emails en conversación real
y cómo solucionarlo.

PROBLEMA IDENTIFICADO:
- Mailtrap está en modo Demo
- Solo acepta emails al propietario: jaircastillo2302@gmail.com  
- Rechaza cualquier otro email (fernando.test@gmail.com, etc.)

SOLUCIÓN:
- Usar siempre jaircastillo2302@gmail.com en las pruebas
- O actualizar la cuenta Mailtrap para envíos sin restricciones
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.external_apis.mailtrap_sending_service import MailtrapSendingService

def test_problema_email():
    """Demuestra el problema de Mailtrap Demo"""
    
    print("🔍 DIAGNÓSTICO DEL PROBLEMA DE EMAILS")
    print("="*60)
    
    service = MailtrapSendingService()
    
    cotizacion_test = {
        'numero_cotizacion': 'DIAGNOSTICO001',
        'tipo_vehiculo': 'Auto 2023 Particular',
        'precio_final': 'S/ 185'
    }
    
    print("PROBLEMA: Probando con email externo (debería fallar)")
    print("-"*55)
    
    # 1. Probar con email externo (debería fallar)
    email_externo = "fernando.test@gmail.com"
    print(f"📧 Probando envío a: {email_externo}")
    
    success_externo = service.send_quotation_email(
        recipient_email=email_externo,
        client_name="Fernando Test",
        cotizacion=cotizacion_test,
        attach_pdf=True
    )
    
    if success_externo:
        print("❌ INESPERADO: Email externo funcionó")
    else:
        print("✅ ESPERADO: Email externo falló (Mailtrap Demo restriction)")
    
    print("\n" + "="*60)
    print("SOLUCIÓN: Probando con email del propietario (debería funcionar)")
    print("-"*60)
    
    # 2. Probar con email del propietario (debería funcionar)
    email_propietario = "jaircastillo2302@gmail.com"
    print(f"📧 Probando envío a: {email_propietario}")
    
    cotizacion_test['numero_cotizacion'] = 'SOLUCION001'
    
    success_propietario = service.send_quotation_email(
        recipient_email=email_propietario,
        client_name="Jair Castillo",
        cotizacion=cotizacion_test,
        attach_pdf=True
    )
    
    if success_propietario:
        print("✅ ÉXITO: Email del propietario funcionó perfectamente")
        print("📎 Con PDF adjunto incluido")
    else:
        print("❌ ERROR INESPERADO: Email del propietario falló")
    
    print("\n" + "="*60)
    print("📋 RESUMEN DEL DIAGNÓSTICO:")
    print("="*60)
    print(f"❌ Email externo ({email_externo}): {'FUNCIONÓ' if success_externo else 'FALLÓ (esperado)'}")
    print(f"✅ Email propietario ({email_propietario}): {'FUNCIONÓ' if success_propietario else 'FALLÓ'}")
    
    print("\n🎯 CONCLUSIÓN:")
    print("- Mailtrap está en modo Demo")
    print("- Solo acepta emails al propietario de la cuenta")
    print("- Para usar otros emails necesitas actualizar la cuenta Mailtrap")
    print("- Mientras tanto, usa jaircastillo2302@gmail.com para pruebas")
    
    print("\n💡 PARA CONVERSACIÓN REAL:")
    print("- Barbara debe detectar si el email no es del propietario")
    print("- Y enviar solo al email permitido (jaircastillo2302@gmail.com)")
    print("- O mostrar mensaje explicativo sobre la limitación")

if __name__ == "__main__":
    test_problema_email() 