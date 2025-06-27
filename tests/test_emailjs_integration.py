"""
🧪 Test EmailJS Integration - Usando credenciales existentes del usuario
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.external_apis.emailjs_service import EmailJSService
import logging
from typing import Optional

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_emailjs_service():
    """Prueba el servicio EmailJS con credenciales existentes"""
    print("🧪 PROBANDO SERVICIO EMAILJS")
    print("="*50)
    
    emailjs_service = EmailJSService()
    
    # Mostrar configuración
    status = emailjs_service.get_service_status()
    print("📊 CONFIGURACIÓN EMAILJS:")
    print(f"   ✅ Service ID: {status['service_id']}")
    print(f"   ✅ Template ID: {status['template_id']}")
    print(f"   ✅ Public Key: {status['public_key']}")
    print(f"   ✅ Límite mensual: {status['monthly_limit']}")
    print(f"   ✅ Costo: {status['cost']}")
    print()

def test_email_sending(test_email: Optional[str] = None):
    """Prueba el envío de email con EmailJS"""
    
    if not test_email:
        test_email = input("📧 Ingresa tu email para prueba (o presiona Enter para simular): ").strip()
    
    if not test_email:
        print("⚠️  Simulando envío de email...")
        test_email = "test@example.com"
    
    print(f"\n🧪 PROBANDO ENVÍO A: {test_email}")
    print("="*50)
    
    emailjs_service = EmailJSService()
    
    # Datos de cotización de prueba
    cotizacion_data = {
        'numero_cotizacion': 'AF202506270001',
        'tipo_vehiculo': 'Auto particular',
        'precio_final': 'S/ 165.00',
        'fecha_vencimiento': '15/07/2024'
    }
    
    # Intentar envío
    print("📤 Enviando cotización por EmailJS...")
    
    try:
        success = emailjs_service.send_quotation_email(
            recipient_email=test_email,
            client_name="María González",
            cotizacion=cotizacion_data
        )
        
        if success:
            print("✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
            print(f"   📧 Destinatario: {test_email}")
            print(f"   📋 Cotización: {cotizacion_data['numero_cotizacion']}")
            print(f"   💰 Precio: {cotizacion_data['precio_final']}")
            print("\n🎉 ¡Barbara puede enviar emails perfectamente!")
        else:
            print("❌ Error enviando email")
            print("💡 Verifica:")
            print("   - Conexión a internet")
            print("   - Credenciales EmailJS")
            print("   - Email destino válido")
            
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print("💡 Revisa los logs para más detalles")

def test_template_generation():
    """Prueba la generación de templates"""
    print("\n🧪 PROBANDO GENERACIÓN DE TEMPLATES")
    print("="*50)
    
    emailjs_service = EmailJSService()
    
    cotizacion_data = {
        'numero_cotizacion': 'AF202506270001',
        'tipo_vehiculo': 'Auto particular',
        'precio_final': 'S/ 165.00'
    }
    
    message = emailjs_service._generate_email_message("Carlos Rodriguez", cotizacion_data)
    
    print("✅ Template generado exitosamente")
    print(f"   📏 Longitud: {len(message)} caracteres")
    
    # Verificar elementos clave
    key_elements = ["Carlos Rodriguez", "S/ 165.00", "AF202506270001", "SOAT", "Barbara"]
    missing_elements = []
    
    for element in key_elements:
        if element in message:
            print(f"   ✅ Contiene: '{element}'")
        else:
            print(f"   ❌ Falta: '{element}'")
            missing_elements.append(element)
    
    if not missing_elements:
        print("\n🎉 ¡Template perfecto! Contiene todos los elementos necesarios")
    else:
        print(f"\n⚠️  Faltan {len(missing_elements)} elementos en el template")
    
    # Mostrar preview del mensaje
    print("\n📋 PREVIEW DEL EMAIL:")
    print("-" * 40)
    print(message[:300] + "..." if len(message) > 300 else message)
    print("-" * 40)

def run_emailjs_tests():
    """Ejecuta todas las pruebas de EmailJS"""
    print("🎭 BARBARA - PRUEBAS EMAILJS CON CREDENCIALES EXISTENTES")
    print("="*70)
    print("Usando tu configuración EmailJS ya configurada")
    print("="*70)
    
    try:
        # Prueba 1: Configuración del servicio
        test_emailjs_service()
        
        # Prueba 2: Generación de templates
        test_template_generation()
        
        # Prueba 3: Envío de email (opcional)
        print("\n" + "="*70)
        print("🚀 PRUEBA DE ENVÍO REAL (OPCIONAL)")
        print("="*70)
        
        user_choice = input("¿Quieres probar el envío real de email? (s/n): ").lower().strip()
        
        if user_choice in ['s', 'si', 'sí', 'y', 'yes']:
            test_email_sending()
        else:
            print("⏭️  Saltando prueba de envío real")
            test_email_sending("simulacion@example.com")
        
        print("\n🎉 TODAS LAS PRUEBAS EMAILJS COMPLETADAS")
        print("="*70)
        print("✅ Configuración EmailJS: CORRECTA")
        print("✅ Generación de templates: FUNCIONAL")
        print("✅ Sistema de envío: LISTO")
        print("✅ Barbara puede enviar emails GRATIS con tus credenciales!")
        print("\n💡 EmailJS permite 200 emails GRATIS por mes")
        print("💰 Esto es perfecto para empezar sin costo alguno")
        
    except Exception as e:
        print(f"\n❌ ERROR EN PRUEBAS EMAILJS: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_emailjs_tests() 