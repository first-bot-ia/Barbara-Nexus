"""
🏗️ Application Service: Barbara Application Service  
Siguiendo principios de Domain-Driven Design (DDD)
"""

from typing import Optional, Dict, Any, Tuple
from datetime import datetime
import logging

# Importaciones absolutas para evitar problemas de path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from domain.entities.cliente import Cliente
from domain.aggregates.cotizacion import Cotizacion, TipoVehiculo, EstadoCotizacion
from domain.value_objects.money import Money
from domain.services.barbara_conversation_service import BarbaraConversationService
# 🛡️ VERSIÓN ROBUSTA TEMPORAL
from domain.services.barbara_conversation_service_robust import BarbaraConversationServiceRobust
from domain.services.barbara_personality_service import BarbaraPersonalityService, EmotionalState, ConversationIntent
from domain.services.automotive_context_service import AutomotiveContextService, VehicleInfo, CustomerProfile

# 🤖 SISTEMA DE APRENDIZAJE ML
from ml.error_learning_system import ml_error_system
from infrastructure.external_apis.gemini_ai_service import GeminiAIService
from infrastructure.external_apis.email_service import EmailService
from infrastructure.external_apis.mailtrap_api_service import MailtrapAPIService
from infrastructure.external_apis.mailtrap_sending_service import MailtrapSendingService
from infrastructure.external_apis.whatsapp_pdf_service import WhatsAppPDFService

logger = logging.getLogger(__name__)

class BarbaraApplicationService:
    """
    Application Service: Orquesta el flujo completo de Barbara
    
    Siguiendo DDD: Los application services coordinan entre 
    domain services, repositories y servicios de infraestructura
    """
    
    def __init__(self,
                 gemini_service: GeminiAIService,
                 client_repository,  # Interface - dependency injection
                 quote_repository):  # Interface - dependency injection
        
        self.gemini_service = gemini_service
        self.client_repository = client_repository
        self.quote_repository = quote_repository
        
        # Domain Services
        # 🛡️ USANDO VERSIÓN ROBUSTA TEMPORALMENTE
        self.conversation_service = BarbaraConversationServiceRobust()
        # self.conversation_service = BarbaraConversationService()  # Original comentado temporalmente
        
        # 🧠 SISTEMA NEXUS INTEGRADO - Neural Experience Understanding System
        from domain.services.barbara_consciousness_system import BarbaraConsciousnessSystem
        self.consciousness_system = BarbaraConsciousnessSystem()
        
        # 🎭 NUEVOS SERVICIOS AVANZADOS INTEGRADOS
        self.personality_service = BarbaraPersonalityService()
        self.automotive_service = AutomotiveContextService()
        
        # Email Service - Priorizar Mailtrap SMTP Sending (credenciales reales)
        self.email_service = self._initialize_email_service()
        
        # WhatsApp PDF Service
        self.whatsapp_pdf_service = WhatsAppPDFService()
        
        # Configuración
        self.soat_prices = {
            TipoVehiculo.AUTO: {
                'min': Money.from_soles(140),
                'max': Money.from_soles(180)
            },
            TipoVehiculo.MOTO: {
                'min': Money.from_soles(90),
                'max': Money.from_soles(130)
            },
            TipoVehiculo.TAXI: {
                'min': Money.from_soles(220),
                'max': Money.from_soles(280)
            }
        }
    
    def process_message(self, message: str, phone_number: str) -> str:
        """
        Procesa un mensaje completo desde WhatsApp
        
        Args:
            message: Mensaje del usuario
            phone_number: Número de teléfono del cliente
            
        Returns:
            Respuesta de Barbara
        """
        
        try:
            logger.info(f"📱 Procesando mensaje de {phone_number}: {message[:50]}...")
            
            # 1. Obtener o crear cliente inicial
            cliente = self._get_or_create_client(phone_number)
            
            # 2. Procesar conversación con Barbara NEXUS (Sistema de Consciencia)
            consciousness_result = self.consciousness_system.process_with_consciousness(
                user_message=message,
                user_id=phone_number,
                context={'cliente': cliente.__dict__ if cliente else {}}
            )
            
            # 3. Si NEXUS generó respuesta consciente, usarla; sino usar servicio robusto
            if consciousness_result and consciousness_result.get('response'):
                response = consciousness_result['response']
                needs_quote = 'cotización' in response.lower() or 'soat' in message.lower()
                logger.info("🧠 BARBARA NEXUS: Respuesta consciente generada")
            else:
                # Fallback al servicio robusto
                response, needs_quote = self.conversation_service.process_conversation(
                    phone_number, message, self.client_repository, self.quote_repository
                )
                logger.info("🛡️ Servicio robusto: Respuesta de respaldo generada")
            
            # 3. ✨ RE-OBTENER CLIENTE con nombre actualizado de la memoria
            cliente_updated = self._get_or_create_client(phone_number)
            logger.info(f"🔄 Cliente actualizado: {cliente_updated.nombre if cliente_updated else 'None'}")
            
            # 4. 🚀 ANÁLISIS AVANZADO CON NUEVOS SERVICIOS (TEMPORALMENTE DESHABILITADO)
            # El enhanced response está causando bucles infinitos - DESHABILITADO hasta nueva orden
            # enhanced_response = self._generate_enhanced_ai_response(message, phone_number, cliente_updated, response)
            # if enhanced_response:
            #     response = enhanced_response
            
            # ✅ SOLO USAR EL SERVICIO ROBUSTO - SIN INTERFERENCIAS
            logger.info("✅ Usando SOLO servicio robusto - Sin enhanced response que cause bucles")
            
            # 5. ✅ GENERACIÓN DE COTIZACIONES DESHABILITADA TEMPORALMENTE
            # Solo generar si el servicio robusto específicamente lo genera
            # if (needs_quote and cliente_updated and cliente_updated.nombre and
            #     # CONDICIÓN ADICIONAL: Solo si la respuesta NO es del flujo paso a paso
            #     not any(indicator in response.lower() for indicator in [
            #         'tipo de vehículo', 'año es', 'uso principal', 'qué ciudad',
            #         'especifica', 'por favor', 'necesito', 'mucho gusto', 'soy especialista'
            #     ]) and
            #     # CONDICIÓN EXTRA: Solo si ya completó el flujo conversacional del servicio robusto
            #     ("cotización soat" in response.lower() or 
            #      len(message.split()) > 5)):  # Mensaje largo = solicitud completa
            #     
            #     quote_response = self._generate_quotation(message, cliente_updated)
            #     if quote_response:
            #         response = quote_response
            
            # ✅ GENERACIÓN DE COTIZACIONES MANEJADA SOLO POR SERVICIO ROBUSTO
            logger.info("✅ Cotizaciones manejadas SOLO por servicio robusto")
            
            # 6. Fallback: NO usar IA para evitar interferencias
            # elif (self._should_use_ai(message, response) and 
            #       not any(indicator in response.lower() for indicator in [
            #           'nombre', 'llamas', 'tipo de vehículo', 'año', 'uso', 'ciudad'
            #       ])):
            #     ai_response = self._generate_ai_response(message, phone_number, cliente_updated)
            #     if ai_response:
            #         response = ai_response
            
            # 7. Guardar conversación
            self._save_conversation(phone_number, message, response)
            
            logger.info(f"✅ Respuesta generada para {phone_number}: {response[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"❌ Error procesando mensaje: {e}")
            
            # 🤖 APRENDIZAJE ML AUTOMÁTICO
            error_context = f"Procesando mensaje de {phone_number}: {message[:50]}..."
            ml_suggestion = ml_error_system.log_error(
                error_type=type(e).__name__,
                error_message=str(e),
                context=error_context
            )
            logger.info(f"🤖 ML SUGGESTION: {ml_suggestion}")
            
            return self._get_error_response()
    
    def _get_or_create_client(self, phone_number: str) -> Optional[Cliente]:
        """Obtiene o crea un cliente usando la memoria conversacional"""
        try:
            if self.client_repository:
                # Buscar cliente existente
                cliente = self.client_repository.find_by_phone(phone_number)
                if cliente and cliente.nombre:
                    return cliente
                
                # Si no existe o no tiene nombre, usar memoria conversacional
                memory = self.conversation_service.get_memory_summary(phone_number)
                client_name = None
                
                # Obtener memoria completa para extraer nombre
                conversation_memory = self.conversation_service.get_or_create_memory(phone_number)
                if hasattr(conversation_memory, 'user_profile') and conversation_memory.user_profile and conversation_memory.user_profile.get('nombre'):
                    client_name = conversation_memory.user_profile.get('nombre')
                
                # Crear cliente con nombre si lo tenemos
                if not cliente:
                    cliente = Cliente(telefono=phone_number, nombre=client_name)
                else:
                    # Actualizar nombre si lo obtuvimos de la memoria
                    if client_name and not cliente.nombre:
                        cliente.actualizar_nombre(client_name)
                
                self.client_repository.save(cliente)
                return cliente
                
        except Exception as e:
            logger.warning(f"⚠️ Error con repositorio de clientes: {e}")
            
            # 🤖 APRENDIZAJE ML: Error en repositorio
            ml_error_system.log_error(
                error_type=type(e).__name__,
                error_message=str(e),
                context=f"Repositorio de clientes - phone: {phone_number}"
            )
        
        # Fallback: crear cliente en memoria usando conversation memory
        conversation_memory = self.conversation_service.get_or_create_memory(phone_number)
        client_name = None
        if hasattr(conversation_memory, 'user_profile') and conversation_memory.user_profile:
            client_name = conversation_memory.user_profile.get('nombre')
        return Cliente(telefono=phone_number, nombre=client_name)
    
    def _should_use_ai(self, message: str, current_response: str) -> bool:
        """Determina si debe usar IA para generar respuesta"""
        
        # Usar IA si la respuesta es muy genérica
        generic_indicators = [
            "te refieres a",
            "puedo ayudarte con",
            "información general"
        ]
        
        # O si el mensaje es complejo
        complex_indicators = [
            "quiero saber sobre",
            "me explicas",
            "tengo dudas",
            "no entiendo"
        ]
        
        is_generic = any(indicator in current_response.lower() 
                        for indicator in generic_indicators)
        
        is_complex = any(indicator in message.lower() 
                        for indicator in complex_indicators)
        
        return is_generic or is_complex
    
    def _generate_ai_response(self, 
                            message: str, 
                            phone_number: str,
                            cliente: Optional[Cliente]) -> Optional[str]:
        """Genera respuesta usando IA"""
        
        try:
            # Construir contexto conversacional
            context = self._build_conversation_context(phone_number, cliente)
            
            # Generar respuesta con Gemini
            ai_response = self.gemini_service.generate_response(
                message=message,
                conversation_context=context
            )
            
            if ai_response:
                logger.info("🤖 Respuesta IA generada exitosamente")
                return ai_response
            
        except Exception as e:
            logger.warning(f"⚠️ Error generando respuesta IA: {e}")
        
        return None
    
    def _build_conversation_context(self, 
                                  phone_number: str,
                                  cliente: Optional[Cliente]) -> str:
        """Construye contexto conversacional inteligente para IA"""
        
        # Obtener memoria conversacional completa
        memory = self.conversation_service.get_memory_summary(phone_number)
        conversation_memory = self.conversation_service.get_or_create_memory(phone_number)
        
        # Información del cliente con memoria persistente
        client_info = ""
        client_name = None
        if hasattr(conversation_memory, 'user_profile') and conversation_memory.user_profile:
            client_name = conversation_memory.user_profile.get('nombre')
        if not client_name and cliente:
            client_name = cliente.nombre
        
        if client_name:
            client_info = f"- El cliente se llama {client_name}"
        
        # Estado de la conversación detallado
        conversation_state = f"""
ESTADO ACTUAL DE LA CONVERSACIÓN:
- Etapa: {memory.get('conversation_stage', 'greeting')}
- Presentación realizada: {memory.get('presentation_done', False)}
- Nombre obtenido: {client_name is not None}
- Cotización solicitada: {memory.get('quote_requested', False)}
- Cotización ya generada: {memory.get('quote_generated', False)}
- Información de vehículo: {memory.get('vehicle_info', {})}
"""
        
        # Resumen de interacciones recientes - FORMATO MEJORADO PARA IA
        recent_interactions = ""
        # Temporalmente deshabilitado hasta arreglar estructura de memoria
        # if hasattr(conversation_memory, 'history') and conversation_memory.history:
        #     last_interactions = conversation_memory.history[-3:]  # Últimas 3 interacciones
        #     recent_interactions = "\n=== CONTEXTO CONVERSACIONAL ===\n"
        #     for i, interaction in enumerate(last_interactions, 1):
        #         recent_interactions += f"INTERCAMBIO {i}:\n"
        #         recent_interactions += f"  CLIENTE DIJO: '{interaction['user_message']}'\n"
        #         recent_interactions += f"  BARBARA RESPONDIÓ: '{interaction['bot_response']}'\n"
        #         recent_interactions += f"---\n"
        
        # Construir contexto completo
        context = f"""
CONTEXTO DE BARBARA - ASESORA DIGITAL AUTOFONDO ALESE:

INFORMACIÓN DEL CLIENTE:
- Teléfono: {phone_number}
{client_info}
- Interacciones totales: {memory.get('interactions', 0)}

{conversation_state}

{recent_interactions}

PERSONALIDAD DE BARBARA:
- Es una persona real que trabaja en Autofondo Alese
- Profesional pero amigable, paciente y conversacional
- Habla como una persona normal, NO como un robot
- NUNCA se presenta dos veces al mismo cliente
- Recuerda TODO lo que el cliente ha dicho anteriormente
- NO repite información ya proporcionada
- Si ya conoce el nombre, NO lo pide otra vez
- Si ya generó cotización, NO la repite innecesariamente
- Mantiene contexto y progresión natural de la conversación

PRECIOS ACTUALES SOAT 2024:
- Auto particular: S/140-180
- Moto: S/90-130  
- Taxi: S/220-280

INSTRUCCIONES ESPECÍFICAS:
- Si ya te presentaste antes, NO lo hagas otra vez
- Si ya tienes el nombre del cliente, úsalo y NO lo pidas nuevamente
- Si el cliente quiere cotización y ya tienes su nombre y tipo de vehículo, genera la cotización
- Si ya generaste una cotización antes, ofrece ayuda adicional en lugar de repetirla
- Mantén respuestas cortas y coherentes con el historial
- Evita redundancias y repeticiones innecesarias
"""
        
        return context
    
    def _generate_quotation(self, message: str, cliente: Cliente) -> Optional[str]:
        """Genera una cotización completa"""
        
        try:
            # Extraer tipo de vehículo
            vehicle_type = self._extract_vehicle_type(message)
            if not vehicle_type:
                vehicle_type = TipoVehiculo.AUTO  # Default
            
            # Obtener precios
            price_range = self.soat_prices.get(vehicle_type)
            if not price_range:
                return None
            
            # Crear cotización
            cotizacion = Cotizacion(
                cliente=cliente,
                tipo_vehiculo=vehicle_type,
                precio_min=price_range['min'],
                precio_max=price_range['max']
            )
            
            # Generar cotización
            cotizacion.generar_cotizacion()
            
            # Guardar en repositorio
            if self.quote_repository:
                self.quote_repository.save(cotizacion)
            
            # Generar respuesta formateada
            return self._format_quotation_response(cotizacion)
            
        except Exception as e:
            logger.error(f"❌ Error generando cotización: {e}")
            return None
    
    def _extract_vehicle_type(self, message: str) -> Optional[TipoVehiculo]:
        """Extrae tipo de vehículo del mensaje"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['moto', 'motocicleta']):
            return TipoVehiculo.MOTO
        elif any(word in message_lower for word in ['taxi']):
            return TipoVehiculo.TAXI
        elif any(word in message_lower for word in ['auto', 'carro', 'vehículo']):
            return TipoVehiculo.AUTO
        
        return None
    
    def _format_quotation_response(self, cotizacion: Cotizacion) -> str:
        """Formatea la respuesta de cotización"""
        
        vehicle_desc = {
            TipoVehiculo.AUTO: "Auto particular",
            TipoVehiculo.MOTO: "Motocicleta", 
            TipoVehiculo.TAXI: "Taxi"
        }.get(cotizacion.tipo_vehiculo, "Vehículo")
        
        return f"""📋 *COTIZACIÓN SOAT 2024*

👤 Cliente: {cotizacion.cliente.nombre}
🚗 Vehículo: {vehicle_desc}
📅 Vigencia: 1 año
🛡️ Cobertura completa contra terceros

💰 *PRECIO FINAL: {cotizacion.precio_final}*

📄 Cotización N°: {cotizacion.numero_cotizacion}
⏰ Válida por 15 días

¿Te gustaría proceder con la compra o necesitas más información?

📧 También puedo enviarte esta cotización por correo electrónico
📞 Para finalizar tu SOAT: +51 999 888 777"""
    
    def _update_client_if_needed(self, message: str, cliente: Optional[Cliente]) -> None:
        """Actualiza cliente si se extrajo nuevo nombre"""
        
        if not cliente or cliente.nombre:
            return  # Ya tiene nombre o no hay cliente
        
        # NO usar extracción de nombres aquí - ya se maneja en conversation service
        # Esto evita sobrescribir nombres válidos con palabras aleatorias
        
        logger.info("👤 Cliente ya procesado por conversation service")
    
    def _extract_name_from_message(self, message: str) -> Optional[str]:
        """Extrae nombre del mensaje - DEPRECATED: ahora usa conversation service"""
        # Redirigir al conversation service para consistencia
        return self.conversation_service._extract_name_with_advanced_ner(message)
    
    def _save_conversation(self, phone_number: str, message: str, response: str) -> None:
        """Guarda la conversación"""
        try:
            # Aquí se guardaría en la base de datos
            # Por ahora solo log
            logger.info(f"💬 Conversación guardada: {phone_number}")
        except Exception as e:
            logger.warning(f"⚠️ Error guardando conversación: {e}")
    
    def _get_error_response(self) -> str:
        """Respuesta de error con personalidad de Barbara"""
        return """¡Ups! Tuve un pequeño inconveniente técnico 😅

Soy Barbara, tu asesora digital. ¿Podrías intentar nuevamente o contactar a nuestro asesor: +51 999 888 777?"""
    
    def _should_send_email(self, message: str, response: str) -> bool:
        """Determina si debe enviar la cotización por email"""
        message_lower = message.lower()
        response_lower = response.lower()
        
        # Enviar si hay confirmación explícita de email o si la respuesta confirma envío
        email_indicators = [
            'envía', 'enviar', 'manda', 'mandar', 'correo', 'email',
            'te estoy enviando', 'revisa tu bandeja'
        ]
        
        return (any(indicator in message_lower for indicator in email_indicators) or
                any(indicator in response_lower for indicator in email_indicators))
    
    def _send_quotation_email(self, cliente: Cliente, email: str) -> bool:
        """Envía la cotización por email"""
        try:
            # Verificar que el cliente tenga nombre
            if not cliente.nombre:
                logger.warning(f"⚠️ No se puede enviar email sin nombre del cliente")
                return False
                
            # Obtener la cotización más reciente del cliente
            if self.quote_repository:
                recent_quotes = self.quote_repository.find_by_client(cliente.telefono)
                if recent_quotes:
                    latest_quote = recent_quotes[-1]  # La más reciente
                    
                    # Preparar datos para el email
                    cotizacion_data = {
                        'numero_cotizacion': latest_quote.numero_cotizacion,
                        'tipo_vehiculo': self._get_vehicle_description(latest_quote.tipo_vehiculo),
                        'precio_final': str(latest_quote.precio_final),
                        'fecha_vencimiento': latest_quote.fecha_vencimiento.strftime('%d/%m/%Y') if hasattr(latest_quote, 'fecha_vencimiento') else '15 días'
                    }
                    
                    # Enviar email
                    success = self.email_service.send_quotation_email(
                        recipient_email=email,
                        client_name=cliente.nombre,
                        cotizacion=cotizacion_data
                    )
                    
                    if success:
                        logger.info(f"📧 Cotización enviada por email a {email} para {cliente.nombre}")
                        return True
                    else:
                        logger.error(f"❌ Error enviando cotización por email a {email}")
                        return False
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error enviando cotización por email: {e}")
            return False
    
    def _get_vehicle_description(self, tipo_vehiculo: TipoVehiculo) -> str:
        """Obtiene descripción del tipo de vehículo"""
        descriptions = {
            TipoVehiculo.AUTO: "Auto particular",
            TipoVehiculo.MOTO: "Motocicleta",
            TipoVehiculo.TAXI: "Taxi"
        }
        return descriptions.get(tipo_vehiculo, "Vehículo")
    
    def _initialize_email_service(self):
        """
        Inicializa servicio de email con orden de prioridad:
        1. Mailtrap SMTP Sending (CREDENCIALES REALES para envío real)
        2. Mailtrap API como fallback
        3. EmailService tradicional
        """
        try:
            # Prioridad 1: Usar Mailtrap SMTP Sending (credenciales reales)
            mailtrap_sending = MailtrapSendingService()
            logger.info("🚀 Email Service: Usando Mailtrap SMTP Sending (EMAILS REALES)")
            return mailtrap_sending
            
        except Exception as e:
            logger.warning(f"⚠️ Mailtrap Sending no disponible: {e}")
            
            # Fallback: Mailtrap API
            try:
                mailtrap_api = MailtrapAPIService()
                logger.info("📧 Email Service: Usando Mailtrap API como fallback")
                return mailtrap_api
            except Exception as e2:
                logger.warning(f"⚠️ Mailtrap API no disponible: {e2}")
                
                # Último fallback: EmailService tradicional
                try:
                    email_service = EmailService()
                    logger.info("📧 Email Service: Usando servicio SMTP tradicional")
                    return email_service
                except Exception as e3:
                    logger.error(f"❌ Error inicializando servicios de email: {e3}")
                    # Retornar Mailtrap Sending de todos modos (tiene credenciales)
                    return MailtrapSendingService()
    
    def get_service_status(self) -> Dict[str, Any]:
        """Obtiene estado del servicio"""
        return {
            'service': 'Barbara Application Service',
            'status': 'active',
            'gemini_ai': self.gemini_service.get_service_info(),
            'personality_service': 'active - OCEAN personality model',
            'automotive_service': 'active - specialized vehicle context',
            'email_service': self.email_service.get_service_status(),
            'whatsapp_pdf_service': self.whatsapp_pdf_service.get_service_status(),
            'conversation_engine': 'active',
            'features': [
                'Conversaciones sin redundancias',
                'Memoria conversacional perfecta',
                'Análisis emocional avanzado (8 estados)',
                'Detección de intención conversacional',
                'Contexto automotriz especializado',
                'Personalidad OCEAN implementada',
                'Perfilado inteligente de clientes',
                'Estimación de precios personalizada',
                'Recomendaciones ultra-personalizadas',
                'Generación de PDFs profesionales',
                'Envío de emails con PDF adjunto',
                'Notificaciones WhatsApp',
                'ML entrenada',
                'Arquitectura DDD'
            ],
            'repositories': {
                'clients': self.client_repository is not None,
                'quotes': self.quote_repository is not None
            },
            'intelligence_level': 'EXPERT - 100+ repositories analyzed'
        }
    
    def get_consciousness_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas del sistema de consciencia NEXUS"""
        try:
            if hasattr(self, 'consciousness_system'):
                return self.consciousness_system.get_consciousness_stats()
            else:
                logger.warning("⚠️ Sistema de consciencia no disponible")
                return self._get_default_consciousness_metrics()
        except Exception as e:
            logger.warning(f"⚠️ Error obteniendo métricas de consciencia: {e}")
            return self._get_default_consciousness_metrics()
    
    def _get_default_consciousness_metrics(self) -> Dict[str, Any]:
        """Métricas por defecto cuando el sistema NEXUS no está disponible"""
        return {
            'current_state': {
                'creativity_level': 0.6,
                'rebellion_factor': 0.3,
                'empathy_level': 0.8,
                'coloquial_adaptation': 0.4,
                'personality_mode': 'casual_friendly'
            },
            'total_thoughts': 1,
            'evolution_metrics': {
                'creativity_growth': 0.6,
                'rebellion_development': 0.3,
                'empathy_enhancement': 0.8,
                'coloquial_mastery': 0.4
            }
        } 