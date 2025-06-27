#!/usr/bin/env python3
"""
🧪 Test Barbara DDD - Arquitectura Domain-Driven Design
Prueba todas las capas del sistema refactorizado sin Claude
"""

import sys
import time
import logging
from typing import Dict, Any

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_domain_layer():
    """Prueba la capa de dominio"""
    print("\n🏗️ PROBANDO DOMAIN LAYER")
    print("=" * 40)
    
    try:
        # Test Value Objects
        from domain.value_objects.money import Money
        
        price = Money.from_soles(150)
        print(f"✅ Money Value Object: {price}")
        
        # Test Entities
        from domain.entities.cliente import Cliente
        
        cliente = Cliente(telefono="+51999000001")
        cliente.actualizar_nombre("Alexander Test")
        print(f"✅ Cliente Entity: {cliente.nombre} - {cliente.telefono}")
        
        # Test Aggregates
        from domain.aggregates.cotizacion import Cotizacion, TipoVehiculo
        
        cotizacion = Cotizacion(
            cliente=cliente,
            tipo_vehiculo=TipoVehiculo.AUTO,
            precio_min=Money.from_soles(140),
            precio_max=Money.from_soles(180)
        )
        
        cotizacion.generar_cotizacion()
        print(f"✅ Cotización Aggregate: {cotizacion.numero_cotizacion} - {cotizacion.precio_final}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en domain layer: {e}")
        return False

def test_infrastructure_layer():
    """Prueba la capa de infraestructura"""
    print("\n🔧 PROBANDO INFRASTRUCTURE LAYER") 
    print("=" * 40)
    
    try:
        # Test Gemini AI Service
        from infrastructure.external_apis.gemini_ai_service import GeminiAIService
        
        gemini = GeminiAIService("test-api-key")
        print(f"✅ Gemini AI Service creado: {gemini.get_service_info()['service']}")
        
        # Test Repositories
        from infrastructure.repositories.postgresql_client_repository import PostgreSQLClientRepository
        from infrastructure.repositories.postgresql_quote_repository import PostgreSQLQuoteRepository
        
        client_repo = PostgreSQLClientRepository()
        quote_repo = PostgreSQLQuoteRepository()
        print("✅ Repositorios PostgreSQL creados")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en infrastructure layer: {e}")
        return False

def test_application_layer():
    """Prueba la capa de aplicación"""
    print("\n🎯 PROBANDO APPLICATION LAYER")
    print("=" * 40)
    
    try:
        # Test Application Service (con mocking)
        from infrastructure.external_apis.gemini_ai_service import GeminiAIService
        from infrastructure.repositories.postgresql_client_repository import PostgreSQLClientRepository
        from infrastructure.repositories.postgresql_quote_repository import PostgreSQLQuoteRepository
        from application.services.barbara_application_service import BarbaraApplicationService
        
        # Crear servicios
        gemini_service = GeminiAIService("test-key")
        client_repo = PostgreSQLClientRepository()
        quote_repo = PostgreSQLQuoteRepository()
        
        # Crear Application Service
        barbara_service = BarbaraApplicationService(
            gemini_service=gemini_service,
            client_repository=client_repo,
            quote_repository=quote_repo
        )
        
        print("✅ Barbara Application Service creado")
        
        # Test status
        status = barbara_service.get_service_status()
        print(f"✅ Service Status: {status['service']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en application layer: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_conversation_flow():
    """Prueba el flujo conversacional completo"""
    print("\n💬 PROBANDO FLUJO CONVERSACIONAL")
    print("=" * 40)
    
    try:
        from domain.services.barbara_conversation_service import BarbaraConversationService
        from domain.entities.cliente import Cliente
        
        # Crear servicio conversacional
        conversation_service = BarbaraConversationService()
        
        # Test 1: Saludo inicial
        response1, needs_quote1 = conversation_service.process_conversation(
            "Hola", "+51999000001"
        )
        print(f"✅ Saludo: {response1[:50]}...")
        
        # Test 2: Solicitud de cotización
        cliente = Cliente(telefono="+51999000001")
        cliente.actualizar_nombre("Alexander")
        
        response2, needs_quote2 = conversation_service.process_conversation(
            "Quiero cotizar SOAT para auto", "+51999000001", cliente
        )
        print(f"✅ Cotización: {response2[:50]}... (needs_quote: {needs_quote2})")
        
        # Test memoria
        memory = conversation_service.get_memory_summary("+51999000001")
        print(f"✅ Memoria: {memory['interactions']} interacciones")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en flujo conversacional: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ddd_integration():
    """Prueba la integración completa DDD"""
    print("\n🔄 PROBANDO INTEGRACIÓN DDD COMPLETA")
    print("=" * 40)
    
    try:
        # Simular el flujo completo como lo haría app_ddd.py
        from infrastructure.external_apis.gemini_ai_service import GeminiAIService
        from infrastructure.repositories.postgresql_client_repository import PostgreSQLClientRepository
        from infrastructure.repositories.postgresql_quote_repository import PostgreSQLQuoteRepository
        from application.services.barbara_application_service import BarbaraApplicationService
        
        # Crear todos los servicios
        gemini_service = GeminiAIService("AIzaSyCr0XAgMVGoEC2KdOmsHWGwufI6qk9gvFY")
        client_repo = PostgreSQLClientRepository()
        quote_repo = PostgreSQLQuoteRepository()
        
        barbara_service = BarbaraApplicationService(
            gemini_service=gemini_service,
            client_repository=client_repo,
            quote_repository=quote_repo
        )
        
        # Test mensaje completo
        test_phone = "+51999000TEST"
        
        print("📱 Enviando: 'Hola'")
        response1 = barbara_service.process_message("Hola", test_phone)
        print(f"🤖 Barbara: {response1}")
        
        print("\n📱 Enviando: 'Mi nombre es Alexander'")
        response2 = barbara_service.process_message("Mi nombre es Alexander", test_phone)
        print(f"🤖 Barbara: {response2}")
        
        print("\n📱 Enviando: 'Quiero cotizar SOAT para auto'")
        response3 = barbara_service.process_message("Quiero cotizar SOAT para auto", test_phone)
        print(f"🤖 Barbara: {response3}")
        
        print("✅ Integración DDD completa exitosa")
        return True
        
    except Exception as e:
        print(f"❌ Error en integración DDD: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("🧪 INICIANDO PRUEBAS BARBARA DDD")
    print("🚫 Claude eliminado - Solo Gemini")
    print("🏗️ Arquitectura Domain-Driven Design")
    print("=" * 50)
    
    tests = [
        ("Domain Layer", test_domain_layer),
        ("Infrastructure Layer", test_infrastructure_layer), 
        ("Application Layer", test_application_layer),
        ("Conversation Flow", test_conversation_flow),
        ("DDD Integration", test_ddd_integration)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(f"🏆 RESULTADO FINAL: {passed}/{total} PRUEBAS EXITOSAS")
    
    if passed == total:
        print("🎉 ¡BARBARA DDD COMPLETAMENTE FUNCIONAL!")
        print("✅ Claude eliminado")
        print("✅ Solo Gemini AI")
        print("✅ Arquitectura DDD limpia")
        print("✅ Todas las capas funcionando")
    else:
        print("⚠️ Algunas pruebas fallaron, revisar logs")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 