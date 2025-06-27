#!/usr/bin/env python3
"""
🧪 PRUEBA DIRECTA DE TWILIO
Verificar si las credenciales y configuración funcionan
"""

from twilio.rest import Client
from dotenv import load_dotenv
import os

# Cargar credenciales
load_dotenv('.environment')

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

print("🧪 PRUEBA DIRECTA DE TWILIO")
print("=" * 40)

# Verificar credenciales
if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_WHATSAPP_NUMBER:
    print("❌ ERROR: Credenciales faltantes")
    print(f"Account SID: {'✅' if TWILIO_ACCOUNT_SID else '❌'}")
    print(f"Auth Token: {'✅' if TWILIO_AUTH_TOKEN else '❌'}")
    print(f"WhatsApp Number: {'✅' if TWILIO_WHATSAPP_NUMBER else '❌'}")
    exit(1)

print(f"Account SID: {TWILIO_ACCOUNT_SID}")
print(f"Auth Token: {TWILIO_AUTH_TOKEN[:10]}...")
print(f"WhatsApp Number: {TWILIO_WHATSAPP_NUMBER}")
print("=" * 40)

try:
    # Inicializar cliente Twilio
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    print("✅ Cliente Twilio inicializado correctamente")
    
    # Enviar mensaje de prueba
    message = client.messages.create(
        body="🧪 PRUEBA DIRECTA DE TWILIO: Este es un mensaje de prueba enviado directamente desde Python. Si recibes esto, las credenciales funcionan correctamente.",
        from_=TWILIO_WHATSAPP_NUMBER,
        to='whatsapp:+51960454985'
    )
    
    print(f"✅ Mensaje enviado exitosamente!")
    print(f"📱 SID del mensaje: {message.sid}")
    print(f"📤 Estado: {message.status}")
    print(f"📊 Dirección: {message.direction}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\nPosibles causas:")
    print("1. Credenciales incorrectas")
    print("2. Número no verificado en sandbox")
    print("3. Problema con la cuenta de Twilio") 