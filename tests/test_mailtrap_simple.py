"""
Test simple de Mailtrap para debugging
"""

try:
    print("Iniciando test de Mailtrap...")
    
    from infrastructure.external_apis.mailtrap_sending_service import MailtrapSendingService
    
    # Inicializar servicio
    service = MailtrapSendingService()
    print("Servicio inicializado correctamente")
    
    # Datos de prueba simples
    cotizacion_test = {
        'numero_cotizacion': 'TEST001',
        'tipo_vehiculo': 'Auto 2023',
        'precio_final': 'S/ 180'
    }
    
    print("Datos de prueba preparados")
    
    # Validar datos
    is_valid = service._validate_cotizacion_data(cotizacion_test)
    print(f"Validacion de datos: {is_valid}")
    
    if is_valid:
        # Intentar envio CON PDF para que tenga adjunto
        print("Intentando envio de email...")
        success = service.send_quotation_email(
            recipient_email="jaircastillo2302@gmail.com",
            client_name="TestUser",
            cotizacion=cotizacion_test,
            attach_pdf=True
        )
        
        if success:
            print("SUCCESS: Email enviado correctamente!")
        else:
            print("ERROR: Fallo en el envio de email")
    else:
        print("ERROR: Datos invalidos")

except Exception as e:
    print(f"EXCEPCION: {e}")
    import traceback
    traceback.print_exc() 