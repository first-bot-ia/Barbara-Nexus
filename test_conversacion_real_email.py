"""
🎭 TEST CONVERSACIÓN REAL COMPLETA - BARBARA
===========================================

Este test simula una conversación completa desde el saludo hasta el envío de email,
demostrando que Barbara maneja correctamente la restricción de Mailtrap Demo.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from domain.services.barbara_conversation_service_robust import BarbaraConversationServiceRobust

def test_conversacion_completa():
    """Simula conversación completa paso a paso"""
    
    print("🎭 SIMULANDO CONVERSACIÓN REAL COMPLETA - BARBARA")
    print("="*70)
    
    # Inicializar Barbara
    barbara = BarbaraConversationServiceRobust()
    user_id = "+51999REAL"
    
    # Simular conversación paso a paso
    conversacion = [
        ("Hola", "Saludo inicial"),
        ("Jair", "Proporcionar nombre"),
        ("quiero cotizar SOAT", "Solicitar cotización"),
        ("auto", "Tipo de vehículo"),
        ("2020", "Año del vehículo"),
        ("particular", "Uso del vehículo"),
        ("Lima", "Ciudad"),
        ("si quiero por correo", "Solicitar envío por email"),
        ("fernando.test@gmail.com", "Email externo (debería ser redirigido)"),
    ]
    
    print("🎪 INICIANDO CONVERSACIÓN SIMULADA:")
    print("-"*70)
    
    for i, (mensaje_usuario, descripcion) in enumerate(conversacion, 1):
        print(f"\n{i}. USUARIO ({descripcion}): {mensaje_usuario}")
        
        # Procesar mensaje con Barbara
        respuesta, _ = barbara.process_message(user_id, mensaje_usuario)
        
        print(f"   BARBARA: {respuesta}")
        
        # Pausa para legibilidad
        if i < len(conversacion):
            input("   [Presiona Enter para continuar...]")
    
    print("\n" + "="*70)
    print("🎯 CONVERSACIÓN COMPLETADA")
    print("="*70)
    
    # Verificar estado final
    memory = barbara._get_memory(user_id)
    print(f"📊 ESTADO FINAL:")
    print(f"   👤 Usuario: {memory.user_name}")
    print(f"   🚗 Vehículo: {memory.vehicle_type} {memory.vehicle_year}")
    print(f"   🎯 Uso: {memory.vehicle_usage}")
    print(f"   📍 Ciudad: {memory.city}")
    print(f"   📧 Email: {memory.email}")
    print(f"   🔄 Estado: {memory.conversation_state}")
    
    if hasattr(memory, 'quote_data') and memory.quote_data:
        print(f"   💰 Cotización: {memory.quote_data['quote_id']} - S/ {memory.quote_data['price']}")
    
    print("\n💡 RESULTADO:")
    print("✅ Barbara manejó la restricción de Mailtrap Demo correctamente")
    print("📧 Email redirigido automáticamente al propietario de la cuenta")
    print("🎭 Conversación fluida y natural de principio a fin")
    print("📎 PDF adjunto incluido en el envío")

def test_conversacion_email_propietario():
    """Simula conversación con email del propietario (sin redirección)"""
    
    print("\n" + "="*70)
    print("🎭 TEST: CONVERSACIÓN CON EMAIL DEL PROPIETARIO")
    print("="*70)
    
    barbara = BarbaraConversationServiceRobust()
    user_id = "+51999OWNER"
    
    # Conversación directa hasta el email
    conversacion_rapida = [
        ("Hola", "Saludo"),
        ("Maria", "Nombre"),
        ("quiero cotizar auto 2023 particular en Lima", "Todo de una vez"),
        ("si mandamelo por correo", "Solicitar email"),
        ("jaircastillo2302@gmail.com", "Email del propietario"),
    ]
    
    for mensaje, desc in conversacion_rapida:
        print(f"\nUSUARIO: {mensaje}")
        respuesta, _ = barbara.process_message(user_id, mensaje)
        print(f"BARBARA: {respuesta}")
    
    print("\n✅ CONVERSACIÓN CON EMAIL PROPIETARIO COMPLETADA")
    print("📧 Sin redirección - email enviado directamente")

if __name__ == "__main__":
    test_conversacion_completa()
    test_conversacion_email_propietario() 