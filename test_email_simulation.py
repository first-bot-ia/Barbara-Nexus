"""
Simulacion directa del problema de envio de email
Replica exactamente lo que esta pasando en el flujo conversacional
"""

import logging
from domain.services.barbara_conversation_service_robust import BarbaraConversationServiceRobust, RobustConversationMemory

# Configurar logging detallado
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def simulate_email_problem():
    """Simula el problema exacto del envío de email"""
    
    print("🔍 SIMULANDO PROBLEMA DE EMAIL EXACTO")
    print("=" * 50)
    
    try:
        # Crear servicio robusto
        service = BarbaraConversationServiceRobust()
        print("✅ Servicio conversacional creado")
        
        # Crear memoria simulada con datos exactos del flujo
        user_id = "+519TEST_SIMULATION"
        memory = service._get_memory(user_id)
        
        # Simular datos recopilados en el flujo
        memory.user_name = "Fernando"
        memory.vehicle_type = "auto"
        memory.vehicle_year = "2023"
        memory.vehicle_usage = "particular"
        memory.city = "Lima"
        
        # Simular generación de cotización
        print("\n🔧 Simulando generación de cotización...")
        quote_response = service._generate_complete_quote(memory)
        print(f"✅ Cotización generada: {quote_response[:100]}...")
        
        # Verificar datos de cotización generados
        print(f"\n📊 DATOS EN MEMORIA:")
        print(f"   user_name: {memory.user_name}")
        print(f"   vehicle_type: {memory.vehicle_type}")
        print(f"   vehicle_year: {memory.vehicle_year}")
        print(f"   vehicle_usage: {memory.vehicle_usage}")
        print(f"   city: {memory.city}")
        print(f"   quote_data: {getattr(memory, 'quote_data', 'NO EXISTE')}")
        
        # Simular envío de email exacto
        print(f"\n📧 SIMULANDO ENVÍO DE EMAIL...")
        email_test = "fernando.test@gmail.com"
        
        success = service._send_email_via_mailtrap(memory, email_test)
        
        if success:
            print("🎉 EMAIL ENVIADO EXITOSAMENTE!")
        else:
            print("❌ ERROR EN ENVÍO - REVISAR LOGS ARRIBA")
        
    except Exception as e:
        print(f"❌ EXCEPCIÓN EN SIMULACIÓN: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simulate_email_problem() 