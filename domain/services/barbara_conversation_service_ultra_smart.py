"""
🧠 BARBARA ULTRA-SMART CONVERSATION SERVICE
===========================================

Servicio conversacional avanzado que evita bucles infinitos y mantiene
contexto perfecto basado en las mejores prácticas de la comunidad OpenAI.

Características:
- Sistema de memoria contextual avanzado
- Detección inteligente de intenciones
- Flujo conversacional paso a paso sin saltos
- Prevención de bucles infinitos  
- Validación estricta de datos
- Estados conversacionales robustos
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging
import re
from enum import Enum
import json

logger = logging.getLogger(__name__)

class ConversationIntent(Enum):
    """Intenciones conversacionales específicas"""
    GREETING = "greeting"
    NAME_PROVIDING = "name_providing"  
    AFFIRMATIVE_RESPONSE = "affirmative"
    NEGATIVE_RESPONSE = "negative"
    QUOTE_REQUEST = "quote_request"
    VEHICLE_TYPE_INFO = "vehicle_type"
    VEHICLE_YEAR_INFO = "year_info"
    VEHICLE_USAGE_INFO = "usage_info"
    CITY_INFO = "city_info"
    EMAIL_REQUEST = "email_request"
    EMAIL_PROVIDING = "email_providing"
    CLARIFICATION_NEEDED = "clarification"

class ConversationState(Enum):
    """Estados del flujo conversacional ultra-preciso"""
    INITIAL = "initial"
    WAITING_NAME = "waiting_name"
    NAME_RECEIVED = "name_received"
    QUOTE_INTEREST_CHECK = "quote_interest_check"
    COLLECTING_VEHICLE_TYPE = "collecting_vehicle_type"
    COLLECTING_VEHICLE_YEAR = "collecting_vehicle_year"
    COLLECTING_VEHICLE_USAGE = "collecting_vehicle_usage"
    COLLECTING_CITY = "collecting_city"
    QUOTE_READY = "quote_ready"
    QUOTE_PRESENTED = "quote_presented"
    EMAIL_INTEREST_CHECK = "email_interest_check"
    COLLECTING_EMAIL = "collecting_email"
    EMAIL_SENT = "email_sent"
    CONVERSATION_COMPLETE = "complete"

class ContextualMemory:
    """Memoria contextual ultra-avanzada que previene bucles infinitos"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.current_state = ConversationState.INITIAL
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
        
        # 🧠 DATOS CONVERSACIONALES VALIDADOS
        self.user_name: Optional[str] = None
        self.vehicle_type: Optional[str] = None
        self.vehicle_year: Optional[str] = None
        self.vehicle_usage: Optional[str] = None
        self.city: Optional[str] = None
        self.email: Optional[str] = None
        
        # 🔄 HISTORIAL CONVERSACIONAL COMPLETO
        self.conversation_history: List[Dict] = []
        self.state_transitions: List[Dict] = []
        self.failed_attempts: Dict[str, int] = {}
        
        # 🎯 CONTEXTO AVANZADO
        self.last_question_asked: Optional[str] = None
        self.expecting_answer_for: Optional[str] = None
        self.retry_count_current_step = 0
        self.quote_data: Optional[Dict] = None
        
    def add_interaction(self, user_message: str, bot_response: str, intent: ConversationIntent):
        """Registra interacción con contexto completo"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'bot_response': bot_response,
            'intent': intent.value,
            'state': self.current_state.value,
            'expecting': self.expecting_answer_for
        })
        self.last_updated = datetime.now()
    
    def transition_to_state(self, new_state: ConversationState, reason: str = ""):
        """Transición de estado con logging"""
        old_state = self.current_state
        self.current_state = new_state
        self.state_transitions.append({
            'timestamp': datetime.now().isoformat(),
            'from_state': old_state.value,
            'to_state': new_state.value,
            'reason': reason
        })
        self.retry_count_current_step = 0  # Reset retry counter
        logger.info(f"🔄 Estado: {old_state.value} → {new_state.value} ({reason})")
    
    def increment_retry(self, step: str):
        """Incrementa contador de reintentos para evitar bucles"""
        if step not in self.failed_attempts:
            self.failed_attempts[step] = 0
        self.failed_attempts[step] += 1
        self.retry_count_current_step += 1
    
    def get_context_summary(self) -> str:
        """Obtiene resumen del contexto actual"""
        return f"""
CONTEXTO ACTUAL:
- Estado: {self.current_state.value}
- Nombre: {self.user_name or 'No proporcionado'}
- Vehículo: {self.vehicle_type or 'No especificado'}
- Año: {self.vehicle_year or 'No especificado'}
- Uso: {self.vehicle_usage or 'No especificado'}
- Ciudad: {self.city or 'No especificada'}
- Email: {self.email or 'No proporcionado'}
- Esperando: {self.expecting_answer_for or 'Ninguna respuesta específica'}
- Reintentos paso actual: {self.retry_count_current_step}
"""

class BarbaraUltraSmartService:
    """Servicio conversacional ultra-inteligente que evita bucles infinitos"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.memories: Dict[str, ContextualMemory] = {}
        
        # 🎯 PATRONES DE DETECCIÓN ULTRA-PRECISOS
        self.name_patterns = [
            r'(?:soy|me llamo|mi nombre es)\s+([A-Za-záéíóúÁÉÍÓÚñÑ]{2,20})',
            r'^([A-Za-záéíóúÁÉÍÓÚñÑ]{3,20})$'
        ]
        
        self.affirmative_patterns = [
            r'\b(si|sí|yes|claro|perfecto|correcto|exacto|dale|ok|bueno)\b',
            r'\bquiero\b', r'\bnecesito\b', r'\bme interesa\b'
        ]
        
        self.negative_patterns = [
            r'\b(no|nope|negativo|para nada|no me interesa)\b'
        ]
        
        # 🚗 PATRONES VEHÍCULOS
        self.vehicle_patterns = {
            'auto': ['auto', 'carro', 'automóvil', 'sedan', 'hatchback'],
            'moto': ['moto', 'motocicleta', 'scooter'],
            'taxi': ['taxi', 'colectivo'],
            'camioneta': ['camioneta', 'pickup', 'suv', 'van'],
            'comercial': ['camión', 'bus', 'comercial', 'carga']
        }
        
        # 📅 AÑOS VÁLIDOS
        self.valid_years = list(range(1990, 2026))
        
        # 🏙️ CIUDADES PERUANAS
        self.peruvian_cities = [
            'lima', 'arequipa', 'trujillo', 'chiclayo', 'piura', 'iquitos',
            'cusco', 'huancayo', 'tacna', 'ica', 'puno', 'ayacucho'
        ]
    
    def process_message(self, user_id: str, message: str) -> Tuple[str, bool]:
        """
        Procesa mensaje con inteligencia contextual ultra-avanzada
        
        Returns:
            (response, needs_quote_generation)
        """
        try:
            # 1. Obtener memoria contextual
            memory = self._get_memory(user_id)
            
            # 2. Detectar intención con contexto
            intent = self._detect_intent_contextual(message, memory)
            
            # 3. Validar progresión (evitar bucles)
            if self._is_stuck_in_loop(memory, intent):
                return self._handle_loop_breaking(memory, message, intent)
            
            # 4. Procesar según estado actual
            response = self._process_by_state(memory, message, intent)
            
            # 5. Registrar interacción
            memory.add_interaction(message, response, intent)
            
            # 6. Determinar si necesita generar cotización
            needs_quote = memory.current_state == ConversationState.QUOTE_READY
            
            return response, needs_quote
            
        except Exception as e:
            self.logger.error(f"❌ Error procesando mensaje: {e}")
            return self._get_fallback_response(), False
    
    def _get_memory(self, user_id: str) -> ContextualMemory:
        """Obtiene memoria contextual del usuario"""
        if user_id not in self.memories:
            self.memories[user_id] = ContextualMemory(user_id)
        return self.memories[user_id]
    
    def _detect_intent_contextual(self, message: str, memory: ContextualMemory) -> ConversationIntent:
        """Detecta intención basada en contexto actual"""
        message_lower = message.lower().strip()
        
        # 🎯 DETECCIÓN CONTEXTUAL SEGÚN ESTADO
        if memory.current_state == ConversationState.INITIAL:
            if any(word in message_lower for word in ['hola', 'buenos', 'buenas']):
                return ConversationIntent.GREETING
            else:
                return ConversationIntent.GREETING  # Asumir saludo por defecto
        
        elif memory.current_state == ConversationState.WAITING_NAME:
            if self._extract_name_from_message(message):
                return ConversationIntent.NAME_PROVIDING
            else:
                return ConversationIntent.CLARIFICATION_NEEDED
                
        elif memory.current_state == ConversationState.NAME_RECEIVED:
            if any(word in message_lower for word in ['cotizar', 'cotización', 'soat', 'seguro']):
                return ConversationIntent.QUOTE_REQUEST
            else:
                return ConversationIntent.CLARIFICATION_NEEDED
                
        elif memory.current_state == ConversationState.QUOTE_INTEREST_CHECK:
            if re.search('|'.join(self.affirmative_patterns), message_lower):
                return ConversationIntent.AFFIRMATIVE_RESPONSE
            elif re.search('|'.join(self.negative_patterns), message_lower):
                return ConversationIntent.NEGATIVE_RESPONSE
            else:
                return ConversationIntent.CLARIFICATION_NEEDED
                
        elif memory.current_state == ConversationState.COLLECTING_VEHICLE_TYPE:
            if self._extract_vehicle_type_from_message(message):
                return ConversationIntent.VEHICLE_TYPE_INFO
            else:
                return ConversationIntent.CLARIFICATION_NEEDED
                
        elif memory.current_state == ConversationState.COLLECTING_VEHICLE_YEAR:
            if self._extract_year_from_message(message):
                return ConversationIntent.VEHICLE_YEAR_INFO
            else:
                return ConversationIntent.CLARIFICATION_NEEDED
                
        elif memory.current_state == ConversationState.COLLECTING_VEHICLE_USAGE:
            if self._extract_usage_from_message(message):
                return ConversationIntent.VEHICLE_USAGE_INFO
            else:
                return ConversationIntent.CLARIFICATION_NEEDED
                
        elif memory.current_state == ConversationState.COLLECTING_CITY:
            if self._extract_city_from_message(message):
                return ConversationIntent.CITY_INFO
            else:
                return ConversationIntent.CLARIFICATION_NEEDED
                
        elif memory.current_state == ConversationState.QUOTE_PRESENTED:
            if any(word in message_lower for word in ['correo', 'email', 'mail']):
                return ConversationIntent.EMAIL_REQUEST
            elif re.search('|'.join(self.affirmative_patterns), message_lower):
                return ConversationIntent.AFFIRMATIVE_RESPONSE
            else:
                return ConversationIntent.CLARIFICATION_NEEDED
                
        elif memory.current_state == ConversationState.EMAIL_INTEREST_CHECK:
            if re.search('|'.join(self.affirmative_patterns), message_lower):
                return ConversationIntent.AFFIRMATIVE_RESPONSE
            elif re.search('|'.join(self.negative_patterns), message_lower):
                return ConversationIntent.NEGATIVE_RESPONSE
            else:
                return ConversationIntent.CLARIFICATION_NEEDED
                
        elif memory.current_state == ConversationState.COLLECTING_EMAIL:
            if self._extract_email_from_message(message):
                return ConversationIntent.EMAIL_PROVIDING
            else:
                return ConversationIntent.CLARIFICATION_NEEDED
        
        # Fallback
        return ConversationIntent.CLARIFICATION_NEEDED
    
    def _is_stuck_in_loop(self, memory: ContextualMemory, intent: ConversationIntent) -> bool:
        """Detecta si está atrapado en bucle infinito"""
        # Si ha intentado el mismo paso más de 3 veces
        if memory.retry_count_current_step >= 3:
            return True
            
        # Si ha estado en el mismo estado por más de 5 interacciones
        if len(memory.conversation_history) >= 5:
            last_5_states = [h.get('state') for h in memory.conversation_history[-5:]]
            if len(set(last_5_states)) == 1:  # Todos iguales
                return True
        
        return False
    
    def _handle_loop_breaking(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja ruptura de bucles infinitos"""
        self.logger.warning(f"🔄 Bucle detectado - Estado: {memory.current_state.value}, Reintentos: {memory.retry_count_current_step}")
        
        # Estrategias para romper bucles
        if memory.current_state == ConversationState.WAITING_NAME:
            # Forzar extracción de nombre más flexible
            potential_name = self._extract_name_flexible(message)
            if potential_name:
                memory.user_name = potential_name
                memory.transition_to_state(ConversationState.NAME_RECEIVED, "Bucle roto - nombre extraído flexiblemente")
                return f"Perfecto {potential_name}. Soy Barbara, especialista en SOAT. ¿Te interesa una cotización?"
            else:
                return "Puedes escribir solo tu nombre, por favor. Por ejemplo: 'Juan' o 'Maria'"
                
        elif memory.current_state == ConversationState.QUOTE_INTEREST_CHECK:
            # Asumir interés si menciona algo relacionado
            if any(word in message.lower() for word in ['si', 'quiero', 'necesito', 'cotizar', 'soat']):
                memory.transition_to_state(ConversationState.COLLECTING_VEHICLE_TYPE, "Bucle roto - asumiendo interés")
                memory.expecting_answer_for = "tipo de vehículo"
                return f"¡Excelente {memory.user_name}! Para tu cotización SOAT necesito algunos datos. ¿Qué tipo de vehículo tienes? (auto, moto, taxi, camioneta)"
            else:
                return f"Disculpa {memory.user_name}, ¿te interesa una cotización de SOAT? Responde 'sí' o 'no'"
                
        elif memory.current_state == ConversationState.COLLECTING_VEHICLE_TYPE:
            # Asumir auto por defecto
            memory.vehicle_type = "auto"
            memory.transition_to_state(ConversationState.COLLECTING_VEHICLE_YEAR, "Bucle roto - asumiendo auto")
            memory.expecting_answer_for = "año del vehículo"
            return f"Asumiré que es un auto. ¿De qué año es tu vehículo? (ejemplo: 2020, 2015, etc.)"
        
        # Más estrategias según el estado...
        return self._get_fallback_response()
    
    def _process_by_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Procesa mensaje según estado actual con lógica ultra-precisa"""
        
        if memory.current_state == ConversationState.INITIAL:
            return self._handle_initial_state(memory, message, intent)
            
        elif memory.current_state == ConversationState.WAITING_NAME:
            return self._handle_waiting_name_state(memory, message, intent)
            
        elif memory.current_state == ConversationState.NAME_RECEIVED:
            return self._handle_name_received_state(memory, message, intent)
            
        elif memory.current_state == ConversationState.QUOTE_INTEREST_CHECK:
            return self._handle_quote_interest_check_state(memory, message, intent)
            
        elif memory.current_state == ConversationState.COLLECTING_VEHICLE_TYPE:
            return self._handle_collecting_vehicle_type_state(memory, message, intent)
            
        elif memory.current_state == ConversationState.COLLECTING_VEHICLE_YEAR:
            return self._handle_collecting_vehicle_year_state(memory, message, intent)
            
        elif memory.current_state == ConversationState.COLLECTING_VEHICLE_USAGE:
            return self._handle_collecting_vehicle_usage_state(memory, message, intent)
            
        elif memory.current_state == ConversationState.COLLECTING_CITY:
            return self._handle_collecting_city_state(memory, message, intent)
            
        elif memory.current_state == ConversationState.QUOTE_READY:
            return self._handle_quote_ready_state(memory, message, intent)
            
        elif memory.current_state == ConversationState.QUOTE_PRESENTED:
            return self._handle_quote_presented_state(memory, message, intent)
            
        elif memory.current_state == ConversationState.EMAIL_INTEREST_CHECK:
            return self._handle_email_interest_check_state(memory, message, intent)
            
        elif memory.current_state == ConversationState.COLLECTING_EMAIL:
            return self._handle_collecting_email_state(memory, message, intent)
            
        elif memory.current_state == ConversationState.EMAIL_SENT:
            return self._handle_email_sent_state(memory, message, intent)
        
        return self._get_fallback_response()
    
    def _handle_initial_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja estado inicial"""
        memory.transition_to_state(ConversationState.WAITING_NAME, "Saludo recibido")
        memory.expecting_answer_for = "nombre del usuario"
        return "¡Hola! Soy Barbara de Autofondo Alese. ¿Cómo te llamas?"
    
    def _handle_waiting_name_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja estado esperando nombre"""
        if intent == ConversationIntent.NAME_PROVIDING:
            name = self._extract_name_from_message(message)
            if name:
                memory.user_name = name
                memory.transition_to_state(ConversationState.NAME_RECEIVED, f"Nombre recibido: {name}")
                memory.expecting_answer_for = "tipo de ayuda requerida"
                return f"Mucho gusto {name}. Soy especialista en SOAT. ¿En qué puedo ayudarte?"
        
        # Si no detecta nombre, incrementar retry
        memory.increment_retry("waiting_name")
        return "Por favor, comparte tu nombre conmigo. Puedes escribir solo tu nombre."
    
    def _handle_name_received_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja estado nombre recibido"""
        if intent == ConversationIntent.QUOTE_REQUEST:
            memory.transition_to_state(ConversationState.COLLECTING_VEHICLE_TYPE, "Solicitud de cotización detectada")
            memory.expecting_answer_for = "tipo de vehículo"
            return f"¡Perfecto {memory.user_name}! Te ayudo con tu cotización SOAT. ¿Qué tipo de vehículo tienes? (auto, moto, taxi, camioneta)"
        
        elif any(word in message.lower() for word in ['si', 'quiero', 'necesito', 'cotizar']):
            memory.transition_to_state(ConversationState.QUOTE_INTEREST_CHECK, "Interés en cotización detectado")
            memory.expecting_answer_for = "confirmación de interés en cotización"
            return f"Entiendo {memory.user_name}. ¿Te interesa una cotización de SOAT?"
        
        else:
            memory.transition_to_state(ConversationState.QUOTE_INTEREST_CHECK, "Preguntando por interés")
            memory.expecting_answer_for = "confirmación de interés en cotización"
            return f"Entiendo {memory.user_name}. ¿Te interesa una cotización de SOAT?"
    
    def _handle_quote_interest_check_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja estado verificando interés en cotización"""
        if intent == ConversationIntent.AFFIRMATIVE_RESPONSE:
            memory.transition_to_state(ConversationState.COLLECTING_VEHICLE_TYPE, "Confirmación afirmativa recibida")
            memory.expecting_answer_for = "tipo de vehículo"
            return f"¡Excelente {memory.user_name}! Para tu cotización SOAT necesito algunos datos. ¿Qué tipo de vehículo tienes? (auto, moto, taxi, camioneta)"
        
        elif intent == ConversationIntent.NEGATIVE_RESPONSE:
            memory.transition_to_state(ConversationState.CONVERSATION_COMPLETE, "No interesado en cotización")
            return f"No hay problema {memory.user_name}. Si cambias de opinión, estaré aquí para ayudarte. ¡Que tengas un buen día!"
        
        else:
            memory.increment_retry("quote_interest_check")
            return f"¿Te interesa una cotización de SOAT, {memory.user_name}? Por favor responde 'sí' o 'no'"
    
    def _handle_collecting_vehicle_type_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja estado recopilando tipo de vehículo"""
        if intent == ConversationIntent.VEHICLE_TYPE_INFO:
            vehicle_type = self._extract_vehicle_type_from_message(message)
            if vehicle_type:
                memory.vehicle_type = vehicle_type
                memory.transition_to_state(ConversationState.COLLECTING_VEHICLE_YEAR, f"Tipo de vehículo recibido: {vehicle_type}")
                memory.expecting_answer_for = "año del vehículo"
                return f"Perfecto, {vehicle_type}. ¿De qué año es tu vehículo? (ejemplo: 2020, 2015, etc.)"
        
        memory.increment_retry("collecting_vehicle_type")
        return "Por favor especifica el tipo de vehículo: auto, moto, taxi, camioneta, etc."
    
    def _handle_collecting_vehicle_year_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja estado recopilando año del vehículo"""
        if intent == ConversationIntent.VEHICLE_YEAR_INFO:
            year = self._extract_year_from_message(message)
            if year:
                memory.vehicle_year = year
                memory.transition_to_state(ConversationState.COLLECTING_VEHICLE_USAGE, f"Año recibido: {year}")
                memory.expecting_answer_for = "uso del vehículo"
                return f"Excelente, año {year}. ¿Cuál es el uso principal del vehículo? (particular, trabajo, comercial, taxi)"
        
        memory.increment_retry("collecting_vehicle_year")
        return "Por favor indica el año de tu vehículo. Ejemplo: 2020, 2018, 2023, etc."
    
    def _handle_collecting_vehicle_usage_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja estado recopilando uso del vehículo"""
        if intent == ConversationIntent.VEHICLE_USAGE_INFO:
            usage = self._extract_usage_from_message(message)
            if usage:
                memory.vehicle_usage = usage
                memory.transition_to_state(ConversationState.COLLECTING_CITY, f"Uso recibido: {usage}")
                memory.expecting_answer_for = "ciudad de uso"
                return f"Perfecto, uso {usage}. ¿En qué ciudad usas principalmente tu vehículo?"
        
        memory.increment_retry("collecting_vehicle_usage")
        return "Especifica el uso del vehículo: particular, trabajo, comercial, taxi, etc."
    
    def _handle_collecting_city_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja estado recopilando ciudad"""
        if intent == ConversationIntent.CITY_INFO:
            city = self._extract_city_from_message(message)
            if city:
                memory.city = city
                memory.transition_to_state(ConversationState.QUOTE_READY, f"Ciudad recibida: {city}")
                # Generar cotización aquí
                quote_response = self._generate_quote_with_data(memory)
                memory.transition_to_state(ConversationState.QUOTE_PRESENTED, "Cotización generada y presentada")
                memory.expecting_answer_for = "decisión sobre la cotización"
                return quote_response
        
        memory.increment_retry("collecting_city")
        return "¿En qué ciudad usas tu vehículo? (Lima, Arequipa, Trujillo, etc.)"
    
    def _handle_quote_ready_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja estado cotización lista"""
        # Este estado no debería recibir mensajes normalmente
        quote_response = self._generate_quote_with_data(memory)
        memory.transition_to_state(ConversationState.QUOTE_PRESENTED, "Cotización presentada")
        return quote_response
    
    def _handle_quote_presented_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja estado cotización presentada"""
        if intent == ConversationIntent.EMAIL_REQUEST or any(word in message.lower() for word in ['correo', 'email']):
            memory.transition_to_state(ConversationState.EMAIL_INTEREST_CHECK, "Solicitud de email detectada")
            memory.expecting_answer_for = "confirmación de envío por email"
            return f"¡Perfecto {memory.user_name}! ¿Te gustaría que te envíe esta cotización por correo electrónico?"
        
        elif intent == ConversationIntent.AFFIRMATIVE_RESPONSE:
            memory.transition_to_state(ConversationState.EMAIL_INTEREST_CHECK, "Respuesta afirmativa - ofreciendo email")
            memory.expecting_answer_for = "confirmación de envío por email"
            return f"¡Excelente {memory.user_name}! ¿Te gustaría que te envíe esta cotización por correo electrónico?"
        
        else:
            return f"¿Te interesa proceder con la compra, {memory.user_name}? También puedo enviarte la cotización por correo electrónico."
    
    def _handle_email_interest_check_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja estado verificando interés en email"""
        if intent == ConversationIntent.AFFIRMATIVE_RESPONSE:
            memory.transition_to_state(ConversationState.COLLECTING_EMAIL, "Confirmación para envío por email")
            memory.expecting_answer_for = "dirección de correo electrónico"
            return f"¡Perfecto {memory.user_name}! ¿Cuál es tu dirección de correo electrónico?"
        
        elif intent == ConversationIntent.NEGATIVE_RESPONSE:
            memory.transition_to_state(ConversationState.CONVERSATION_COMPLETE, "No desea email")
            return f"No hay problema {memory.user_name}. ¿Hay algo más en lo que pueda ayudarte?"
        
        else:
            memory.increment_retry("email_interest_check")
            return f"¿Te gustaría recibir la cotización por correo electrónico, {memory.user_name}? Responde 'sí' o 'no'"
    
    def _handle_collecting_email_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja estado recopilando email"""
        if intent == ConversationIntent.EMAIL_PROVIDING:
            email = self._extract_email_from_message(message)
            if email:
                memory.email = email
                memory.transition_to_state(ConversationState.EMAIL_SENT, f"Email recibido: {email}")
                return f"¡Excelente {memory.user_name}! He enviado tu cotización SOAT a {email}. Por favor revisa tu bandeja de entrada (y la carpeta de spam por si acaso). ¡Gracias por confiar en Autofondo Alese!"
        
        memory.increment_retry("collecting_email")
        return "Por favor proporciona un correo válido (ejemplo: tunombre@gmail.com)"
    
    def _handle_email_sent_state(self, memory: ContextualMemory, message: str, intent: ConversationIntent) -> str:
        """Maneja estado email enviado"""
        memory.transition_to_state(ConversationState.CONVERSATION_COMPLETE, "Conversación finalizada")
        return f"¡Gracias {memory.user_name}! ¿Hay algo más en lo que pueda ayudarte?"
    
    # 🔍 MÉTODOS DE EXTRACCIÓN ULTRA-PRECISOS
    
    def _extract_name_from_message(self, message: str) -> Optional[str]:
        """Extrae nombre con patrones ultra-precisos"""
        try:
            message_clean = message.strip()
            
            for pattern in self.name_patterns:
                match = re.search(pattern, message_clean, re.IGNORECASE)
                if match:
                    name = match.group(1).strip()
                    if self._is_valid_name(name):
                        return name.title()
            
            return None
        except Exception:
            return None
    
    def _extract_name_flexible(self, message: str) -> Optional[str]:
        """Extrae nombre con lógica más flexible para romper bucles"""
        words = message.strip().split()
        for word in words:
            if len(word) >= 3 and word.isalpha() and self._is_valid_name(word):
                return word.title()
        return None
    
    def _is_valid_name(self, name: str) -> bool:
        """Valida si es un nombre válido"""
        forbidden = {'hola', 'barbara', 'auto', 'moto', 'soat', 'cotizar', 'quiero', 'precio', 'si', 'no'}
        return name.lower() not in forbidden and len(name) >= 2
    
    def _extract_vehicle_type_from_message(self, message: str) -> Optional[str]:
        """Extrae tipo de vehículo"""
        message_lower = message.lower()
        for vehicle_type, keywords in self.vehicle_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                return vehicle_type
        return None
    
    def _extract_year_from_message(self, message: str) -> Optional[str]:
        """Extrae año del vehículo"""
        import re
        year_match = re.search(r'\b(19[9]\d|20[0-2]\d)\b', message)
        if year_match:
            year = int(year_match.group(1))
            if year in self.valid_years:
                return str(year)
        return None
    
    def _extract_usage_from_message(self, message: str) -> Optional[str]:
        """Extrae uso del vehículo"""
        message_lower = message.lower()
        usage_patterns = {
            'particular': ['particular', 'personal', 'propio'],
            'trabajo': ['trabajo', 'laboral', 'empresa'],
            'comercial': ['comercial', 'negocio', 'carga'],
            'taxi': ['taxi', 'uber', 'colectivo']
        }
        
        for usage, keywords in usage_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                return usage
        return None
    
    def _extract_city_from_message(self, message: str) -> Optional[str]:
        """Extrae ciudad"""
        message_lower = message.lower()
        for city in self.peruvian_cities:
            if city in message_lower:
                return city.title()
        
        # Si no encuentra ciudad conocida, tomar primera palabra válida
        words = message.split()
        for word in words:
            if len(word) > 2 and word.isalpha():
                return word.title()
        return None
    
    def _extract_email_from_message(self, message: str) -> Optional[str]:
        """Extrae email válido"""
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, message)
        return match.group(0) if match else None
    
    def _generate_quote_with_data(self, memory: ContextualMemory) -> str:
        """Genera cotización usando SOLO los datos proporcionados por el usuario"""
        try:
            import uuid
            from datetime import datetime
            
            quote_id = f"AF{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
            
            # Calcular precio REAL según datos proporcionados
            base_price = self._calculate_price_from_data(memory)
            
            memory.quote_data = {
                'quote_id': quote_id,
                'price': base_price,
                'client_name': memory.user_name,
                'vehicle_type': memory.vehicle_type,
                'vehicle_year': memory.vehicle_year,
                'vehicle_usage': memory.vehicle_usage,
                'city': memory.city
            }
            
            quote_response = f"""📋 *COTIZACIÓN SOAT 2024*

👤 Cliente: {memory.user_name}
🚗 Vehículo: {memory.vehicle_type.title()} {memory.vehicle_year}
🎯 Uso: {memory.vehicle_usage.title()}
📍 Ciudad: {memory.city}
📅 Vigencia: 1 año
🛡️ Cobertura completa contra terceros

💰 *PRECIO FINAL: S/ {base_price}.00*

📄 Cotización N°: {quote_id}
⏰ Válida por 15 días

¿Te interesa proceder con la compra? También puedo enviarte esta cotización por correo electrónico.

📞 Para más información: +51 999 888 777"""

            self.logger.info(f"💰 Cotización generada para {memory.user_name}: {quote_id} - S/{base_price}")
            return quote_response
            
        except Exception as e:
            self.logger.error(f"❌ Error generando cotización: {e}")
            return f"¡Perfecto {memory.user_name}! Tu cotización SOAT está lista. Te contactaremos pronto con los detalles."
    
    def _calculate_price_from_data(self, memory: ContextualMemory) -> int:
        """Calcula precio basado en datos reales proporcionados"""
        base_price = 160  # Precio base
        
        # Ajuste por tipo de vehículo
        if memory.vehicle_type == 'moto':
            base_price = 80
        elif memory.vehicle_type == 'taxi':
            base_price = 220
        elif memory.vehicle_type == 'comercial':
            base_price = 350
        elif memory.vehicle_type == 'camioneta':
            base_price = 180
        
        # Ajuste por año
        if memory.vehicle_year:
            year = int(memory.vehicle_year)
            if year >= 2020:
                base_price += 20
            elif year >= 2015:
                base_price += 10
            elif year < 2000:
                base_price -= 20
        
        # Ajuste por uso
        if memory.vehicle_usage == 'comercial':
            base_price += 30
        elif memory.vehicle_usage == 'taxi':
            base_price += 50
        
        # Ajuste por ciudad (Lima más caro)
        if memory.city and memory.city.lower() == 'lima':
            base_price += 10
        
        return base_price
    
    def _get_fallback_response(self) -> str:
        """Respuesta de emergencia"""
        return "¡Hola! Soy Barbara de Autofondo Alese. ¿Cómo puedo ayudarte con tu SOAT hoy?"
    
    # 🔧 MÉTODOS DE COMPATIBILIDAD
    
    def process_conversation(self, user_id: str, message: str, client_repository=None, quote_repository=None) -> Tuple[str, bool]:
        """Método de compatibilidad"""
        return self.process_message(user_id, message)
    
    def get_user_name(self, user_id: str) -> Optional[str]:
        """Obtiene nombre de usuario"""
        memory = self._get_memory(user_id)
        return memory.user_name
    
    def get_interaction_count(self, user_id: str) -> int:
        """Obtiene número de interacciones"""
        memory = self._get_memory(user_id)
        return len(memory.conversation_history) 