"""
📧 TEST MAILTRAP DIRECTO
Prueba directa del servicio de Mailtrap para identificar problemas específicos
"""

from infrastructure.external_apis.mailtrap_sending_service import MailtrapSendingService
import logging

# Configurar logging para ver todos los detalles
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_mailtrap_direct():
    """Prueba directa del servicio Mailtrap"""
    
    print("📧 INICIANDO PRUEBA DIRECTA DE MAILTRAP")
    print("=" * 50)
    
    try:
        # Inicializar servicio
        print("🔧 Inicializando servicio Mailtrap...")
        service = MailtrapSendingService()
        print("✅ Servicio inicializado")
        
        # Mostrar configuración
        status = service.get_service_status()
        print(f"\n📊 CONFIGURACIÓN MAILTRAP:")
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        # Datos de cotización de prueba
        cotizacion_test = {
            'numero_cotizacion': 'TEST20250627001',
            'tipo_vehiculo': 'Auto 2023 Particular',
            'precio_final': 'S/ 180'
        }
        
        print(f"\n📋 DATOS DE PRUEBA:")
        for key, value in cotizacion_test.items():
            print(f"   {key}: {value}")
        
        # Verificar validación
        print(f"\n🔍 Validando datos...")
        is_valid = service._validate_cotizacion_data(cotizacion_test)
        if is_valid:
            print("✅ Datos válidos para envío")
        else:
            print("❌ Datos inválidos - no se puede enviar")
            return
        
        # Intentar envío real
        email_destino = "jaircastillo2302@gmail.com"  # Tu email real
        print(f"\n📧 ENVIANDO EMAIL A: {email_destino}")
        print("⏳ Intentando envío...")
        
        success = service.send_quotation_email(
            recipient_email=email_destino,
            client_name="TestDirecto", 
            cotizacion=cotizacion_test,
            attach_pdf=False  # Sin PDF para simplificar
        )
        
        if success:
            print("🎉 ¡EMAIL ENVIADO EXITOSAMENTE!")
            print(f"📬 Revisa tu bandeja de entrada: {email_destino}")
            print("📨 También verifica la carpeta de SPAM")
        else:
            print("❌ ERROR EN EL ENVÍO")
            print("🔍 Revisar logs arriba para detalles del error")
        
    except Exception as e:
        print(f"❌ EXCEPCIÓN DURANTE LA PRUEBA: {e}")
        import traceback
        print(f"📜 Stack trace: {traceback.format_exc()}")

if __name__ == "__main__":
    test_mailtrap_direct() 