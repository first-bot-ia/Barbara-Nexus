"""
🚀 PRUEBA MAILTRAP SMTP SENDING - EMAILS REALES
==============================================

Este script prueba las credenciales REALES de Mailtrap SMTP Sending:
- Host: live.smtp.mailtrap.io  
- API Token: 3ad4786fc1d172fb1f2bac6a8ee017c2
- Username: smtp@mailtrap.io
- Port: 587 con STARTTLS

¡ESTOS EMAILS VAN A DIRECCIONES REALES!
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.external_apis.mailtrap_sending_service import MailtrapSendingService

def main():
    print("🚀 PRUEBA MAILTRAP SMTP SENDING - BARBARA")
    print("="*60)
    print("⚡ CREDENCIALES REALES DE ENVÍO")
    print("📧 Los emails van a direcciones reales")
    print("🎯 Dominio verificado: demomailtrap.co")
    print()
    
    # Inicializar servicio
    print("🔧 Inicializando Mailtrap SMTP Sending Service...")
    try:
        mailtrap_sending = MailtrapSendingService()
        print("✅ Servicio inicializado correctamente")
        
        # Mostrar estado
        status = mailtrap_sending.get_service_status()
        print("\n📊 ESTADO DEL SERVICIO:")
        print(f"   Servicio: {status['service']}")
        print(f"   Estado: {status['status']}")
        print(f"   Provider: {status['provider']}")
        print(f"   Host: {status['host']}")
        print(f"   Puerto: {status['port']}")
        print(f"   Username: {status['username']}")
        print(f"   API Token: {status['api_token']}")
        print(f"   Sender Email: {status['sender_email']}")
        print(f"   Costo: {status['cost']}")
        print(f"   Límite mensual: {status['monthly_limit']}")
        print(f"   Tipo de email: {status['email_type']}")
        print(f"   Perfecto para: {status['perfect_for']}")
        
    except Exception as e:
        print(f"❌ Error inicializando servicio: {e}")
        return
    
    # Solicitar email para prueba
    print("\n📧 ENVIAR EMAIL REAL DE PRUEBA")
    print("-"*40)
    print("⚠️  IMPORTANTE: Este email se enviará REALMENTE")
    
    # PROTECCIÓN CONTRA BUCLE INFINITO - Máximo 3 intentos
    max_attempts = 3
    attempts = 0
    
    while attempts < max_attempts:
        attempts += 1
        try:
            test_email = input(f"Ingresa tu email para recibir la cotización real (intento {attempts}/{max_attempts}): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n❌ Operación cancelada por el usuario")
            return
        
        if not test_email:
            print("❌ Email requerido")
            continue
            
        if "@" not in test_email:
            print("❌ Email debe tener formato válido")
            continue
        
        # Confirmar envío
        try:
            print(f"\n⚠️  ¿Confirmas enviar email REAL a {test_email}? (s/n): ", end="")
            confirm = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n❌ Operación cancelada por el usuario")
            return
        
        if confirm in ['s', 'si', 'sí', 'y', 'yes']:
            break
        elif confirm in ['n', 'no']:
            print("❌ Operación cancelada")
            return
        else:
            print("❌ Respuesta inválida. Usa 's' para sí o 'n' para no")
    
    if attempts >= max_attempts:
        print("❌ Máximo número de intentos alcanzado. Operación cancelada.")
        return
    
    # Datos de cotización REAL de prueba
    print(f"\n📤 Enviando cotización REAL a {test_email}...")
    print("🔄 Procesando...")
    
    cotizacion_data = {
        'numero_cotizacion': 'AF202506270002',
        'tipo_vehiculo': 'Auto particular',
        'precio_final': 'S/ 165.00',
        'fecha_vencimiento': '12/07/2024'
    }
    
    # Enviar email REAL
    try:
        success = mailtrap_sending.send_quotation_email(
            recipient_email=test_email,
            client_name="Cliente Prueba REAL",
            cotizacion=cotizacion_data
        )
        
        if success:
            print("✅ ¡EMAIL REAL ENVIADO EXITOSAMENTE!")
            print()
            print("🎉 RESULTADO DE LA PRUEBA:")
            print(f"   📧 Email enviado a: {test_email}")
            print(f"   🚀 Servicio: Mailtrap SMTP Sending")
            print(f"   🎯 Host: live.smtp.mailtrap.io")
            print(f"   💰 Costo: GRATIS (1,000 emails/mes)")
            print(f"   📨 Tipo: EMAIL REAL enviado a bandeja real")
            print()
            print("📱 PASOS SIGUIENTES:")
            print("   1. Revisa tu bandeja de entrada")
            print("   2. Si no llegó en 1-2 minutos, verifica spam")
            print("   3. El email tiene diseño profesional HTML")
            print("   4. ¡Barbara puede enviar cotizaciones reales!")
            print()
            print("🎭 BARBARA - EMAIL REAL CONFIGURADO ✅")
            print("   ✅ Mailtrap SMTP Sending funcionando")
            print("   ✅ Emails reales a clientes reales")
            print("   ✅ Sin configuración adicional necesaria")
            print("   ✅ Dominio verificado: demomailtrap.co")
            
        else:
            print("❌ ERROR ENVIANDO EMAIL REAL")
            print()
            print("💡 POSIBLES CAUSAS:")
            print("   - API Token incorrecto")
            print("   - Email destino con problemas")
            print("   - Límite de envío alcanzado") 
            print("   - Dominio no verificado correctamente")
            print("   - Problemas de conexión SMTP")
            print()
            print("🔧 SOLUCIONES:")
            print("   1. Verifica credenciales en Mailtrap dashboard")
            print("   2. Confirma que el dominio esté verificado")
            print("   3. Prueba con otro email")
            print("   4. Revisa logs de Mailtrap")
            
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")
        print()
        print("🔧 DEPURACIÓN:")
        print(f"   - Host: {mailtrap_sending.smtp_host}")
        print(f"   - Puerto: {mailtrap_sending.smtp_port}")
        print(f"   - Username: {mailtrap_sending.smtp_username}")
        print(f"   - API Token: {mailtrap_sending.smtp_password[:10]}...")
        print(f"   - Sender: {mailtrap_sending.sender_email}")
        print(f"   - Email destino: {test_email}")
        print()
        print("💡 VERIFICA:")
        print("   1. Todas las credenciales son correctas")
        print("   2. El dominio demomailtrap.co está verificado")
        print("   3. No hay firewall bloqueando puerto 587")

if __name__ == "__main__":
    main() 