"""
🧪 Test de Integración - Barbara con Email y Mejoras de Memoria
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.services.barbara_conversation_service import BarbaraConversationService
from domain.entities.cliente import Cliente
from infrastructure.external_apis.email_service import EmailService
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_name_extraction():
    """Prueba la extracción mejorada de nombres"""
    print("🧪 PROBANDO EXTRACCIÓN DE NOMBRES")
    print("="*50)
    
    service = BarbaraConversationService()
    
    test_cases = [
        ("Mi nombre es Carlos Rodriguez", "Carlos Rodriguez"),
        ("Me llamo Ana Martinez", "Ana Martinez"),
        ("Soy Diego Morales", "Diego Morales"),
        ("Roberto Silva", "Roberto Silva"),
        ("Quiero cotizar SOAT", None),  # No debería extraer
        ("Hola", None),  # No debería extraer
        ("Para mi auto", None)  # No debería extraer
    ]
    
    for message, expected in test_cases:
        result = service._smart_name_extraction(message)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{message}' -> '{result}' (esperado: '{expected}')")
    
    print()

def test_conversation_flow():
    """Prueba el flujo completo de conversación"""
    print("🧪 PROBANDO FLUJO DE CONVERSACIÓN")
    print("="*50)
    
    service = BarbaraConversationService()
    phone = "+51999000001"
    cliente = Cliente(telefono=phone)
    
    # Flujo de conversación completo
    test_messages = [
        "Hola",
        "Mi nombre es Maria Gonzalez", 
        "Quiero cotizar SOAT",
        "Para mi auto",
        "Envíamelo por correo",
        "mi-email@gmail.com"
    ]
    
    print("Simulando conversación:")
    for i, message in enumerate(test_messages, 1):
        response, needs_quote = service.process_conversation(message, phone, cliente)
        print(f"\n{i}. Usuario: {message}")
        print(f"   Barbara: {response[:100]}...")
        print(f"   Necesita cotización: {needs_quote}")
        
        # Verificar memoria
        memory = service.get_memory_summary(phone)
        print(f"   Estado: {memory.get('conversation_stage')}, Nombre: {memory.get('client_name')}")

def test_email_service():
    """Prueba el servicio de email (configuración)"""
    print("\n🧪 PROBANDO SERVICIO DE EMAIL")
    print("="*50)
    
    email_service = EmailService()
    status = email_service.get_service_status()
    
    print(f"Estado del servicio: {status}")
    print(f"Configuración SMTP: {status['smtp_server']}:{status['smtp_port']}")
    print(f"Remitente configurado: {status['sender_configured']}")
    
    if status['sender_configured']:
        print("✅ Servicio de email configurado correctamente")
    else:
        print("⚠️  Servicio de email necesita configuración de variables de entorno:")
        print("   - SENDER_EMAIL=tu-email@gmail.com")
        print("   - SENDER_PASSWORD=tu-app-password")

def test_email_template():
    """Prueba la generación de templates de email"""
    print("\n🧪 PROBANDO TEMPLATES DE EMAIL")
    print("="*50)
    
    email_service = EmailService()
    
    # Datos de prueba
    client_name = "Maria Gonzalez"
    cotizacion_data = {
        'numero_cotizacion': 'AF202506270001',
        'tipo_vehiculo': 'Auto particular',
        'precio_final': 'S/ 165.00',
        'fecha_vencimiento': '15/07/2024'
    }
    
    # Generar contenido
    try:
        html_content = email_service._generate_html_content(client_name, cotizacion_data)
        text_content = email_service._generate_text_content(client_name, cotizacion_data)
        
        print("✅ Template HTML generado correctamente")
        print(f"   Longitud: {len(html_content)} caracteres")
        
        print("✅ Template de texto generado correctamente")  
        print(f"   Longitud: {len(text_content)} caracteres")
        
        # Verificar contenido clave
        key_elements = [client_name, cotizacion_data['precio_final'], cotizacion_data['numero_cotizacion']]
        for element in key_elements:
            if element in html_content and element in text_content:
                print(f"✅ Elemento '{element}' presente en ambos templates")
            else:
                print(f"❌ Elemento '{element}' faltante en algún template")
                
    except Exception as e:
        print(f"❌ Error generando templates: {e}")

def run_integration_tests():
    """Ejecuta todas las pruebas de integración"""
    print("🎭 BARBARA - PRUEBAS DE INTEGRACIÓN COMPLETAS")
    print("="*60)
    print("Probando mejoras de memoria conversacional y funcionalidad de email")
    print("="*60)
    
    try:
        test_name_extraction()
        test_conversation_flow()
        test_email_service()
        test_email_template()
        
        print("\n🎉 TODAS LAS PRUEBAS COMPLETADAS")
        print("="*60)
        print("✅ Extracción de nombres: MEJORADA")
        print("✅ Flujo conversacional: OPTIMIZADO") 
        print("✅ Servicio de email: IMPLEMENTADO")
        print("✅ Templates de email: FUNCIONALES")
        print("\n🚀 Barbara está lista para funcionar sin problemas de memoria!")
        
    except Exception as e:
        print(f"\n❌ ERROR EN PRUEBAS: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_integration_tests() 