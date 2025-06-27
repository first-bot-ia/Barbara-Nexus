"""
🚀 Prueba Rápida de EmailJS - Barbara
Prueba directa del sistema de envío con tus credenciales
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.external_apis.emailjs_service import EmailJSService
import time

def test_emailjs_quick():
    """Prueba rápida de EmailJS"""
    
    print("🎭 BARBARA - PRUEBA RÁPIDA EMAILJS")
    print("="*50)
    print("🔧 Usando tus credenciales existentes")
    print("="*50)
    
    # Crear servicio EmailJS
    emailjs = EmailJSService()
    
    # Mostrar configuración
    status = emailjs.get_service_status()
    print("📊 CONFIGURACIÓN:")
    print(f"   ✅ Service: {status['service_id']}")
    print(f"   ✅ Template: {status['template_id']}")
    print(f"   ✅ Key: {status['public_key']}")
    print(f"   ✅ Límite: {status['monthly_limit']}")
    print(f"   ✅ Costo: {status['cost']}")
    print()
    
    # Solicitar email para prueba
    email_destino = input("📧 Ingresa tu email para la prueba: ").strip()
    
    if not email_destino:
        print("❌ Email requerido para la prueba")
        return
    
    print(f"\n🚀 ENVIANDO COTIZACIÓN DE PRUEBA A: {email_destino}")
    print("="*50)
    
    # Datos de cotización de prueba
    cotizacion_data = {
        'numero_cotizacion': 'AF202506270001',
        'tipo_vehiculo': 'Auto particular',
        'precio_final': 'S/ 165.00',
        'fecha_vencimiento': '15/07/2024'
    }
    
    # Enviar email
    print("📤 Enviando email con EmailJS...")
    
    try:
        success = emailjs.send_quotation_email(
            recipient_email=email_destino,
            client_name="Cliente Prueba",
            cotizacion=cotizacion_data
        )
        
        if success:
            print("✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
            print(f"   📧 Destinatario: {email_destino}")
            print(f"   📋 Cotización: {cotizacion_data['numero_cotizacion']}")
            print(f"   💰 Precio: {cotizacion_data['precio_final']}")
            print("\n🎉 ¡EmailJS funcionando perfectamente!")
            print("📱 Revisa tu bandeja de entrada")
            
        else:
            print("❌ Error enviando email")
            print("💡 Posibles causas:")
            print("   - Conexión a internet")
            print("   - Credenciales EmailJS")
            print("   - Email destino inválido")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print("\n🔍 DEBUGGING:")
        print("   - Verifica conexión a internet")
        print("   - Confirma credenciales EmailJS")
        print("   - Revisa que el email destino sea válido")
    
    print("\n" + "="*50)
    print("✅ Prueba completada")

if __name__ == "__main__":
    test_emailjs_quick() 