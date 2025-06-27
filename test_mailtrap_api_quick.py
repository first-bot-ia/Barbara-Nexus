"""
🚀 PRUEBA RÁPIDA - MAILTRAP API
===============================

Este script prueba la API de Mailtrap con tus credenciales ya configuradas:
- API Token: 1d7cb5e1a481fd392258b77261b63bea
- Host: sandbox.api.mailtrap.io

Solo necesitas proporcionar un email para recibir la prueba.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.external_apis.mailtrap_api_service import MailtrapAPIService

def main():
    print("🚀 PRUEBA MAILTRAP API - BARBARA")
    print("="*50)
    print("🎯 Tu API Key ya está configurada")
    print("💡 Solo necesitas un email para la prueba")
    print()
    
    # Inicializar servicio
    print("🔧 Inicializando Mailtrap API Service...")
    try:
        mailtrap_api = MailtrapAPIService()
        print("✅ Servicio inicializado correctamente")
        
        # Mostrar estado
        status = mailtrap_api.get_service_status()
        print("\n📊 ESTADO DEL SERVICIO:")
        print(f"   Servicio: {status['service']}")
        print(f"   Estado: {status['status']}")
        print(f"   Provider: {status['provider']}")
        print(f"   Host: {status['host']}")
        print(f"   API Token: {status['api_token']}")
        print(f"   Costo: {status['cost']}")
        print(f"   Límite mensual: {status['monthly_limit']}")
        print(f"   Perfecto para: {status['perfect_for']}")
        
    except Exception as e:
        print(f"❌ Error inicializando servicio: {e}")
        return
    
    # Solicitar email para prueba
    print("\n📧 ENVIAR EMAIL DE PRUEBA")
    print("-"*30)
    
    while True:
        test_email = input("Ingresa tu email para recibir la prueba: ").strip()
        
        if not test_email:
            print("❌ Email requerido")
            continue
            
        if "@" not in test_email:
            print("❌ Email debe tener formato válido")
            continue
            
        break
    
    # Datos de cotización de prueba
    print(f"\n📤 Enviando cotización de prueba a {test_email}...")
    
    cotizacion_data = {
        'numero_cotizacion': 'AF202506270001',
        'tipo_vehiculo': 'Auto particular',
        'precio_final': 'S/ 165.00',
        'fecha_vencimiento': '12/07/2024'
    }
    
    # Enviar email
    try:
        success = mailtrap_api.send_quotation_email(
            recipient_email=test_email,
            client_name="Cliente Prueba API",
            cotizacion=cotizacion_data
        )
        
        if success:
            print("✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
            print()
            print("🎉 RESULTADO DE LA PRUEBA:")
            print(f"   📧 Email enviado a: {test_email}")
            print(f"   🚀 Servicio: Mailtrap API")
            print(f"   🎯 API Token: Funcionando correctamente")
            print(f"   💰 Costo: GRATIS (1,000 emails/mes)")
            print()
            print("📱 PASOS SIGUIENTES:")
            print("   1. Revisa tu bandeja de entrada")
            print("   2. Si no llegó, verifica spam/promociones")
            print("   3. ¡Barbara está lista para enviar cotizaciones!")
            print()
            print("🎭 BARBARA - CONFIGURACIÓN COMPLETA ✅")
            print("   ✅ Mailtrap API funcionando")
            print("   ✅ Emails profesionales listos")
            print("   ✅ Sin configuración adicional necesaria")
            
        else:
            print("❌ ERROR ENVIANDO EMAIL")
            print()
            print("💡 POSIBLES CAUSAS:")
            print("   - API Key incorrecta")
            print("   - Email destino inválido")
            print("   - Límite de sandbox alcanzado")
            print("   - Problemas de conexión")
            print()
            print("🔧 SOLUCIONES:")
            print("   1. Verifica que tu API Key sea correcta")
            print("   2. Prueba con otro email")
            print("   3. Revisa tu cuenta de Mailtrap")
            
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        print()
        print("🔧 DEPURACIÓN:")
        print(f"   - API Token: {mailtrap_api.api_token[:10]}...")
        print(f"   - Host: {mailtrap_api.host}")
        print(f"   - URL: {mailtrap_api.api_url}")
        print(f"   - Email destino: {test_email}")

if __name__ == "__main__":
    main() 