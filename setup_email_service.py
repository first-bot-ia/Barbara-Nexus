"""
🔧 Configurador de Servicio de Email para Barbara
Elige entre Gmail, Mailtrap u otro servicio SMTP
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.external_apis.email_service import EmailService
from infrastructure.external_apis.mailtrap_service import MailtrapService
from infrastructure.external_apis.mailtrap_api_service import MailtrapAPIService

def show_email_options():
    """Muestra las opciones de email disponibles"""
    
    print("🎭 BARBARA - CONFIGURADOR DE EMAIL")
    print("="*50)
    print("📧 Elige tu servicio de email preferido:")
    print()
    print("1. 🚀 Mailtrap API (YA CONFIGURADO ✅)")
    print("   ✅ Tu API Key ya está integrada")
    print("   ✅ 1,000 emails/mes gratis")
    print("   ✅ Perfecto para Python")
    print("   ⚡ ¡RECOMENDADO! Listo para usar")
    print()
    print("2. 📬 Gmail SMTP (GRATIS)")
    print("   ✅ 500 emails/día gratis")
    print("   ✅ Configuración con App Password")
    print("   ✅ Ideal para empezar")
    print()
    print("3. 🛡️  Mailtrap SMTP (GRATIS)")
    print("   ✅ 1,000 emails/mes gratis")
    print("   ✅ Testing profesional")
    print("   ✅ Alternativa SMTP")
    print()
    print("4. ⚙️  Otro SMTP personalizado")
    print("   ✅ Tu propio servidor")
    print("   ✅ Configuración avanzada")
    print()
    print("5. 🧪 Probar configuración actual")
    print()

def test_mailtrap_api():
    """Prueba la API de Mailtrap ya configurada"""
    
    print("\n🚀 PROBANDO MAILTRAP API (YA CONFIGURADO)")
    print("="*50)
    
    try:
        # Inicializar servicio con credenciales integradas
        mailtrap_api = MailtrapAPIService()
        
        # Mostrar estado
        status = mailtrap_api.get_service_status()
        print("📊 Estado del servicio:")
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        print()
        print("🎯 Tu API está completamente configurada:")
        print(f"   Host: {status['host']}")
        print(f"   Token: {status['api_token']}")
        print(f"   Límite: {status['monthly_limit']}")
        print()
        
        test_email = input("📧 Email para enviar prueba: ").strip()
        if not test_email:
            print("❌ Email requerido para la prueba")
            return False
        
        print(f"📤 Enviando email de prueba a {test_email}...")
        
        # Datos de cotización de prueba
        cotizacion_data = {
            'numero_cotizacion': 'AF202506270001',
            'tipo_vehiculo': 'Auto particular',
            'precio_final': 'S/ 165.00',
            'fecha_vencimiento': '15/07/2024'
        }
        
        success = mailtrap_api.send_quotation_email(
            recipient_email=test_email,
            client_name="Cliente Prueba API",
            cotizacion=cotizacion_data
        )
        
        if success:
            print("✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
            print(f"📱 Revisa la bandeja de entrada de {test_email}")
            print("🎉 ¡Barbara puede enviar emails con tu API!")
            print()
            print("💡 PASOS SIGUIENTES:")
            print("   1. Verifica que recibiste el email")
            print("   2. Si no llegó, revisa spam/promociones")
            print("   3. ¡Barbara está lista para usar!")
            return True
        else:
            print("❌ Error enviando email")
            print("💡 Posibles causas:")
            print("   - API Key incorrecta")
            print("   - Email destino inválido")
            print("   - Límite de sandbox alcanzado")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def configure_gmail():
    """Configura Gmail SMTP"""
    
    print("\n📬 CONFIGURANDO GMAIL SMTP")
    print("="*40)
    print("💡 Necesitas:")
    print("   1. Cuenta Gmail")
    print("   2. Autenticación de 2 factores activada")
    print("   3. App Password generada")
    print()
    print("🔗 Guía: https://support.google.com/accounts/answer/185833")
    print()
    
    email = input("📧 Tu email Gmail: ").strip()
    password = input("🔑 Tu App Password (16 caracteres): ").strip()
    
    if email and password:
        # Crear archivo .env
        env_content = f"""# Configuración Gmail SMTP
SENDER_EMAIL={email}
SENDER_PASSWORD={password}
"""
        
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        
        print("✅ Configuración Gmail guardada en .env")
        return test_email_service("gmail", email)
    else:
        print("❌ Email y password son requeridos")
        return False

def configure_mailtrap():
    """Configura Mailtrap SMTP"""
    
    print("\n🛡️  CONFIGURANDO MAILTRAP SMTP")
    print("="*40)
    print("💡 Pasos para configurar:")
    print("   1. Ve a tu dashboard de Mailtrap")
    print("   2. Navega a Sandboxes > My Sandbox")
    print("   3. Click en Integration tab")
    print("   4. Copia credenciales SMTP")
    print()
    print("🔗 Dashboard: https://mailtrap.io/sandboxes")
    print()
    
    username = input("👤 Mailtrap Username: ").strip()
    password = input("🔑 Mailtrap Password: ").strip()
    
    if username and password:
        # Crear archivo .env
        env_content = f"""# Configuración Mailtrap SMTP
MAILTRAP_USERNAME={username}
MAILTRAP_PASSWORD={password}
"""
        
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        
        print("✅ Configuración Mailtrap SMTP guardada en .env")
        return test_mailtrap_service(username, password)
    else:
        print("❌ Username y password son requeridos")
        return False

def test_email_service(service_type, email):
    """Prueba el servicio de email configurado"""
    
    print(f"\n🧪 PROBANDO {service_type.upper()}")
    print("="*40)
    
    try:
        if service_type == "gmail":
            email_service = EmailService()
        else:
            email_service = MailtrapService()
        
        # Mostrar estado
        status = email_service.get_service_status()
        print("📊 Estado del servicio:")
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        # Probar envío
        test_email = input(f"\n📧 Email para prueba (Enter para usar {email}): ").strip()
        if not test_email:
            test_email = email
        
        print(f"📤 Enviando email de prueba a {test_email}...")
        
        # Datos de cotización de prueba
        cotizacion_data = {
            'numero_cotizacion': 'AF202506270001',
            'tipo_vehiculo': 'Auto particular',
            'precio_final': 'S/ 165.00',
            'fecha_vencimiento': '15/07/2024'
        }
        
        success = email_service.send_quotation_email(
            recipient_email=test_email,
            client_name="Cliente Prueba",
            cotizacion=cotizacion_data
        )
        
        if success:
            print("✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
            print(f"📱 Revisa la bandeja de entrada de {test_email}")
            print("🎉 ¡Barbara puede enviar emails perfectamente!")
            return True
        else:
            print("❌ Error enviando email")
            print("💡 Verifica:")
            print("   - Credenciales correctas")
            print("   - Conexión a internet")
            print("   - Email destino válido")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_mailtrap_service(username, password):
    """Prueba específica para Mailtrap SMTP"""
    
    print("\n🧪 PROBANDO MAILTRAP SMTP")
    print("="*40)
    
    try:
        # Configurar variables de entorno temporalmente
        os.environ["MAILTRAP_USERNAME"] = username
        os.environ["MAILTRAP_PASSWORD"] = password
        
        mailtrap_service = MailtrapService()
        
        # Mostrar estado
        status = mailtrap_service.get_service_status()
        print("📊 Estado del servicio:")
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        test_email = input("\n📧 Email para prueba: ").strip()
        if not test_email:
            print("❌ Email requerido para la prueba")
            return False
        
        print(f"📤 Enviando email de prueba a {test_email}...")
        
        # Datos de prueba
        cotizacion_data = {
            'numero_cotizacion': 'AF202506270001',
            'tipo_vehiculo': 'Auto particular',
            'precio_final': 'S/ 165.00'
        }
        
        success = mailtrap_service.send_quotation_email(
            recipient_email=test_email,
            client_name="Cliente Prueba Mailtrap",
            cotizacion=cotizacion_data
        )
        
        if success:
            print("✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
            print(f"📱 Revisa tu inbox de Mailtrap")
            print("🎉 ¡Mailtrap SMTP funcionando perfectamente!")
            return True
        else:
            print("❌ Error enviando email")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_current_config():
    """Prueba la configuración actual"""
    
    print("\n🧪 PROBANDO CONFIGURACIÓN ACTUAL")
    print("="*40)
    
    try:
        email_service = EmailService()
        status = email_service.get_service_status()
        
        print("📊 Configuración actual:")
        for key, value in status.items():
            print(f"   {key}: {value}")
        
        if status.get('sender_configured'):
            test_email = input("\n📧 Email para prueba: ").strip()
            if test_email:
                return test_email_service("current", test_email)
            else:
                print("❌ Email requerido")
                return False
        else:
            print("⚠️  No hay configuración de email válida")
            print("💡 Configura un servicio primero")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal del configurador"""
    
    show_email_options()
    
    # PROTECCIÓN CONTRA BUCLE INFINITO - Máximo 5 intentos
    max_attempts = 5
    attempts = 0
    
    while attempts < max_attempts:
        attempts += 1
        try:
            choice = input(f"Elige una opción (1-5) - Intento {attempts}/{max_attempts}: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n❌ Operación cancelada por el usuario")
            break
        
        if choice == "1":
            if test_mailtrap_api():
                print("\n🎉 ¡Mailtrap API funcionando perfectamente!")
                print("🚀 Barbara puede enviar emails con tu API")
                print("💡 No necesitas más configuración")
                break
            else:
                print("\n⚠️  API configurada pero con problemas")
                print("💡 Puedes probar otras opciones")
            
        elif choice == "2":
            if configure_gmail():
                print("\n🎉 ¡Gmail configurado exitosamente!")
                print("🚀 Barbara puede enviar emails con Gmail")
                break
            
        elif choice == "3":
            if configure_mailtrap():
                print("\n🎉 ¡Mailtrap SMTP configurado exitosamente!")
                print("🚀 Barbara puede enviar emails con Mailtrap SMTP")
                break
            
        elif choice == "4":
            print("\n⚙️  CONFIGURACIÓN PERSONALIZADA")
            print("Edita el archivo infrastructure/external_apis/email_service.py")
            print("con tu configuración SMTP personalizada")
            break
            
        elif choice == "5":
            if test_current_config():
                print("\n🎉 ¡Configuración actual funciona!")
                break
            
        else:
            print("❌ Opción inválida. Elige 1, 2, 3, 4 o 5")
    
    if attempts >= max_attempts:
        print("\n❌ Máximo número de intentos alcanzado. Configuración cancelada.")
        print("💡 Ejecuta nuevamente el script cuando estés listo para configurar.")
    
    print("\n" + "="*50)
    print("✅ Configuración completada")
    print("🎭 ¡Barbara está lista para enviar cotizaciones por email!")

if __name__ == "__main__":
    main() 