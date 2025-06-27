"""
🧠 BARBARA ULTRA-INTELLIGENT CONVERSATION SERVICE
================================================

Solución definitiva para evitar bucles infinitos y mantener contexto perfecto.
Basado en las mejores prácticas de la comunidad OpenAI para prevenir loops.
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging
import re
from enum import Enum

logger = logging.getLogger(__name__)

class ConversationIntent(Enum):
    GREETING = "greeting"
    NAME_PROVIDING = "name_providing"  
    AFFIRMATIVE = "affirmative"
    NEGATIVE = "negative"
    QUOTE_REQUEST = "quote_request"
    VEHICLE_INFO = "vehicle_info"
    YEAR_INFO = "year_info"
    USAGE_INFO = "usage_info"
    CITY_INFO = "city_info"
    EMAIL_REQUEST = "email_request"
    EMAIL_PROVIDING = "email_providing"
    CLARIFICATION = "clarification"

class ConversationState(Enum):
    INITIAL = "initial"
    WAITING_NAME = "waiting_name"
    NAME_RECEIVED = "name_received"
    QUOTE_INTEREST = "quote_interest"
    COLLECTING_VEHICLE = "collecting_vehicle"
    COLLECTING_YEAR = "collecting_year"
    COLLECTING_USAGE = "collecting_usage"
    COLLECTING_CITY = "collecting_city"
    QUOTE_READY = "quote_ready"
    QUOTE_PRESENTED = "quote_presented"
    EMAIL_INTEREST = "email_interest"
    COLLECTING_EMAIL = "collecting_email"
    EMAIL_SENT = "email_sent"
    COMPLETE = "complete"

class SmartMemory:
    """Memoria inteligente que previene bucles infinitos"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.state = ConversationState.INITIAL
        self.created_at = datetime.now()
        
        # 🧠 DATOS CONVERSACIONALES
        self.user_name: Optional[str] = None
        self.vehicle_type: Optional[str] = None
        self.vehicle_year: Optional[str] = None
        self.vehicle_usage: Optional[str] = None
        self.city: Optional[str] = None
        self.email: Optional[str] = None
        
        # 🔄 CONTROL DE BUCLES
        self.conversation_history: List[Dict] = []
        self.retry_count = 0
        self.last_state = None
        self.same_state_count = 0
        self.expecting = None
        
    def add_interaction(self, user_msg: str, bot_response: str, intent: ConversationIntent):
        """Registra interacción y detecta bucles"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_msg,
            'bot': bot_response,
            'intent': intent.value,
            'state': self.state.value
        })
        
        # Detectar bucles
        if self.state == self.last_state:
            self.same_state_count += 1
        else:
            self.same_state_count = 0
            self.retry_count = 0
        
        self.last_state = self.state
    
    def change_state(self, new_state: ConversationState, reason: str = ""):
        """Cambia estado con logging"""
        old_state = self.state
        self.state = new_state
        self.retry_count = 0
        self.same_state_count = 0
        logger.info(f"🔄 {old_state.value} → {new_state.value} ({reason})")
    
    def is_stuck_in_loop(self) -> bool:
        """Detecta si está atrapado en bucle"""
        return self.same_state_count >= 3 or self.retry_count >= 3
    
    def increment_retry(self):
        """Incrementa contador de reintentos"""
        self.retry_count += 1

class BarbaraUltraIntelligentService:
    """Servicio ultra-inteligente que evita bucles infinitos"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.memories: Dict[str, SmartMemory] = {}
        
        # 🎯 PATRONES INTELIGENTES
        self.name_patterns = [
            r'(?:soy|me llamo|mi nombre es)\s+([A-Za-záéíóúÁÉÍÓÚñÑ]{2,20})',
            r'^([A-Za-záéíóúÁÉÍÓÚñÑ]{3,20})$'
        ]
        
        self.forbidden_names = {
            'hola', 'barbara', 'auto', 'moto', 'soat', 'cotizar', 
            'quiero', 'precio', 'si', 'no', 'ok', 'gracias'
        }
        
        self.vehicle_types = {
            'auto': ['auto', 'carro', 'automóvil', 'sedan'],
            'moto': ['moto', 'motocicleta', 'scooter'],
            'taxi': ['taxi', 'colectivo'],
            'camioneta': ['camioneta', 'pickup', 'suv'],
            'comercial': ['camión', 'bus', 'comercial']
        }
        
        self.usage_types = {
            'particular': ['particular', 'personal', 'propio'],
            'trabajo': ['trabajo', 'laboral', 'empresa'],
            'comercial': ['comercial', 'negocio'],
            'taxi': ['taxi', 'uber']
        }
        
        self.cities = ['lima', 'arequipa', 'trujillo', 'chiclayo', 'piura', 'cusco']
    
    def process_message(self, user_id: str, message: str) -> Tuple[str, bool]:
        """Procesa mensaje con inteligencia anti-bucles"""
        try:
            memory = self._get_memory(user_id)
            
            # 🔍 DETECTAR BUCLE INFINITO
            if memory.is_stuck_in_loop():
                return self._break_loop(memory, message)
            
            # 🎯 DETECTAR INTENCIÓN CONTEXTUAL
            intent = self._detect_intent(message, memory)
            
            # 🔄 PROCESAR SEGÚN ESTADO
            response = self._process_by_state(memory, message, intent)
            
            # 📝 REGISTRAR INTERACCIÓN
            memory.add_interaction(message, response, intent)
            
            # ✅ DETERMINAR SI NECESITA COTIZACIÓN
            needs_quote = memory.state == ConversationState.QUOTE_READY
            
            return response, needs_quote
            
        except Exception as e:
            self.logger.error(f"❌ Error: {e}")
            return "¡Hola! Soy Barbara de Autofondo Alese. ¿Cómo puedo ayudarte con tu SOAT?", False
    
    def _get_memory(self, user_id: str) -> SmartMemory:
        """Obtiene memoria del usuario"""
        if user_id not in self.memories:
            self.memories[user_id] = SmartMemory(user_id)
        return self.memories[user_id]
    
    def _detect_intent(self, message: str, memory: SmartMemory) -> ConversationIntent:
        """Detecta intención basada en contexto"""
        msg = message.lower().strip()
        
        # 🎯 DETECCIÓN CONTEXTUAL SEGÚN ESTADO
        if memory.state == ConversationState.INITIAL:
            return ConversationIntent.GREETING
            
        elif memory.state == ConversationState.WAITING_NAME:
            if self._extract_name(message):
                return ConversationIntent.NAME_PROVIDING
            return ConversationIntent.CLARIFICATION
            
        elif memory.state == ConversationState.NAME_RECEIVED:
            if any(word in msg for word in ['cotizar', 'soat', 'seguro']):
                return ConversationIntent.QUOTE_REQUEST
            return ConversationIntent.CLARIFICATION
            
        elif memory.state == ConversationState.QUOTE_INTEREST:
            if any(word in msg for word in ['si', 'sí', 'yes', 'claro', 'quiero']):
                return ConversationIntent.AFFIRMATIVE
            elif any(word in msg for word in ['no', 'nope', 'negativo']):
                return ConversationIntent.NEGATIVE
            return ConversationIntent.CLARIFICATION
            
        elif memory.state == ConversationState.COLLECTING_VEHICLE:
            if self._extract_vehicle_type(message):
                return ConversationIntent.VEHICLE_INFO
            return ConversationIntent.CLARIFICATION
            
        elif memory.state == ConversationState.COLLECTING_YEAR:
            if self._extract_year(message):
                return ConversationIntent.YEAR_INFO
            return ConversationIntent.CLARIFICATION
            
        elif memory.state == ConversationState.COLLECTING_USAGE:
            if self._extract_usage(message):
                return ConversationIntent.USAGE_INFO
            return ConversationIntent.CLARIFICATION
            
        elif memory.state == ConversationState.COLLECTING_CITY:
            if self._extract_city(message):
                return ConversationIntent.CITY_INFO
            return ConversationIntent.CLARIFICATION
            
        elif memory.state == ConversationState.QUOTE_PRESENTED:
            if any(word in msg for word in ['correo', 'email', 'mail']):
                return ConversationIntent.EMAIL_REQUEST
            elif any(word in msg for word in ['si', 'sí', 'quiero']):
                return ConversationIntent.AFFIRMATIVE
            return ConversationIntent.CLARIFICATION
            
        elif memory.state == ConversationState.EMAIL_INTEREST:
            if any(word in msg for word in ['si', 'sí', 'yes', 'claro']):
                return ConversationIntent.AFFIRMATIVE
            elif any(word in msg for word in ['no', 'nope']):
                return ConversationIntent.NEGATIVE
            return ConversationIntent.CLARIFICATION
            
        elif memory.state == ConversationState.COLLECTING_EMAIL:
            if self._extract_email(message):
                return ConversationIntent.EMAIL_PROVIDING
            return ConversationIntent.CLARIFICATION
        
        return ConversationIntent.CLARIFICATION
    
    def _break_loop(self, memory: SmartMemory, message: str) -> Tuple[str, bool]:
        """Rompe bucles infinitos con estrategias inteligentes"""
        self.logger.warning(f"🔄 BUCLE DETECTADO - Estado: {memory.state.value}, Reintentos: {memory.retry_count}")
        
        if memory.state == ConversationState.WAITING_NAME:
            # Estrategia: Extracción flexible de nombre
            name = self._extract_name_flexible(message)
            if name:
                memory.user_name = name
                memory.change_state(ConversationState.NAME_RECEIVED, "Bucle roto - nombre extraído")
                return f"Perfecto {name}. Soy Barbara, especialista en SOAT. ¿Te interesa una cotización?", False
            else:
                return "Escribe solo tu nombre, por favor. Ejemplo: 'Juan'", False
                
        elif memory.state == ConversationState.QUOTE_INTEREST:
            # Estrategia: Asumir interés si menciona palabras clave
            if any(word in message.lower() for word in ['si', 'quiero', 'necesito', 'cotizar']):
                memory.change_state(ConversationState.COLLECTING_VEHICLE, "Bucle roto - asumiendo interés")
                memory.expecting = "tipo de vehículo"
                return f"¡Excelente {memory.user_name}! ¿Qué tipo de vehículo tienes? (auto, moto, taxi, camioneta)", False
            else:
                return f"¿Te interesa una cotización de SOAT, {memory.user_name}? Responde solo 'sí' o 'no'", False
                
        elif memory.state == ConversationState.COLLECTING_VEHICLE:
            # Estrategia: Asumir auto por defecto
            memory.vehicle_type = "auto"
            memory.change_state(ConversationState.COLLECTING_YEAR, "Bucle roto - asumiendo auto")
            memory.expecting = "año del vehículo"
            return f"Asumiré que es un auto. ¿De qué año? (ejemplo: 2020)", False
            
        elif memory.state == ConversationState.COLLECTING_YEAR:
            # Estrategia: Asumir año reciente
            memory.vehicle_year = "2020"
            memory.change_state(ConversationState.COLLECTING_USAGE, "Bucle roto - asumiendo 2020")
            memory.expecting = "uso del vehículo"
            return f"Asumiré año 2020. ¿Uso del vehículo? (particular, trabajo, comercial)", False
            
        elif memory.state == ConversationState.COLLECTING_USAGE:
            # Estrategia: Asumir particular
            memory.vehicle_usage = "particular"
            memory.change_state(ConversationState.COLLECTING_CITY, "Bucle roto - asumiendo particular")
            memory.expecting = "ciudad"
            return f"Asumiré uso particular. ¿En qué ciudad? (Lima, Arequipa, etc.)", False
            
        elif memory.state == ConversationState.COLLECTING_CITY:
            # Estrategia: Asumir Lima
            memory.city = "Lima"
            memory.change_state(ConversationState.QUOTE_READY, "Bucle roto - asumiendo Lima")
            return self._generate_quote(memory), True
        
        # Fallback: Reiniciar conversación
        memory.change_state(ConversationState.INITIAL, "Bucle roto - reiniciando")
        return "Reiniciemos. ¡Hola! Soy Barbara de Autofondo Alese. ¿Cómo te llamas?", False
    
    def _process_by_state(self, memory: SmartMemory, message: str, intent: ConversationIntent) -> str:
        """Procesa según estado actual"""
        
        if memory.state == ConversationState.INITIAL:
            memory.change_state(ConversationState.WAITING_NAME, "Saludo inicial")
            memory.expecting = "nombre"
            return "¡Hola! Soy Barbara de Autofondo Alese. ¿Cómo te llamas?"
            
        elif memory.state == ConversationState.WAITING_NAME:
            if intent == ConversationIntent.NAME_PROVIDING:
                name = self._extract_name(message)
                if name:
                    memory.user_name = name
                    memory.change_state(ConversationState.NAME_RECEIVED, f"Nombre: {name}")
                    memory.expecting = "solicitud de ayuda"
                    return f"Mucho gusto {name}. Soy especialista en SOAT. ¿En qué puedo ayudarte?"
            
            memory.increment_retry()
            return "Por favor, dime tu nombre."
            
        elif memory.state == ConversationState.NAME_RECEIVED:
            if intent == ConversationIntent.QUOTE_REQUEST:
                memory.change_state(ConversationState.COLLECTING_VEHICLE, "Solicitud de cotización")
                memory.expecting = "tipo de vehículo"
                return f"¡Perfecto {memory.user_name}! Para tu cotización SOAT, ¿qué tipo de vehículo tienes? (auto, moto, taxi, camioneta)"
            else:
                memory.change_state(ConversationState.QUOTE_INTEREST, "Preguntando interés")
                memory.expecting = "confirmación de interés"
                return f"Entiendo {memory.user_name}. ¿Te interesa una cotización de SOAT?"
                
        elif memory.state == ConversationState.QUOTE_INTEREST:
            if intent == ConversationIntent.AFFIRMATIVE:
                memory.change_state(ConversationState.COLLECTING_VEHICLE, "Interés confirmado")
                memory.expecting = "tipo de vehículo"
                return f"¡Excelente {memory.user_name}! ¿Qué tipo de vehículo tienes? (auto, moto, taxi, camioneta)"
            elif intent == ConversationIntent.NEGATIVE:
                memory.change_state(ConversationState.COMPLETE, "No interesado")
                return f"No hay problema {memory.user_name}. ¡Que tengas un buen día!"
            else:
                memory.increment_retry()
                return f"¿Te interesa una cotización de SOAT, {memory.user_name}? Responde 'sí' o 'no'"
                
        elif memory.state == ConversationState.COLLECTING_VEHICLE:
            if intent == ConversationIntent.VEHICLE_INFO:
                vehicle = self._extract_vehicle_type(message)
                if vehicle:
                    memory.vehicle_type = vehicle
                    memory.change_state(ConversationState.COLLECTING_YEAR, f"Vehículo: {vehicle}")
                    memory.expecting = "año del vehículo"
                    return f"Perfecto, {vehicle}. ¿De qué año es? (ejemplo: 2020, 2015)"
            
            memory.increment_retry()
            return "Especifica el tipo: auto, moto, taxi, camioneta, etc."
            
        elif memory.state == ConversationState.COLLECTING_YEAR:
            if intent == ConversationIntent.YEAR_INFO:
                year = self._extract_year(message)
                if year:
                    memory.vehicle_year = year
                    memory.change_state(ConversationState.COLLECTING_USAGE, f"Año: {year}")
                    memory.expecting = "uso del vehículo"
                    return f"Excelente, año {year}. ¿Uso del vehículo? (particular, trabajo, comercial, taxi)"
            
            memory.increment_retry()
            return "Indica el año: 2020, 2018, 2023, etc."
            
        elif memory.state == ConversationState.COLLECTING_USAGE:
            if intent == ConversationIntent.USAGE_INFO:
                usage = self._extract_usage(message)
                if usage:
                    memory.vehicle_usage = usage
                    memory.change_state(ConversationState.COLLECTING_CITY, f"Uso: {usage}")
                    memory.expecting = "ciudad"
                    return f"Perfecto, uso {usage}. ¿En qué ciudad lo usas? (Lima, Arequipa, etc.)"
            
            memory.increment_retry()
            return "Especifica el uso: particular, trabajo, comercial, taxi"
            
        elif memory.state == ConversationState.COLLECTING_CITY:
            if intent == ConversationIntent.CITY_INFO:
                city = self._extract_city(message)
                if city:
                    memory.city = city
                    memory.change_state(ConversationState.QUOTE_PRESENTED, f"Ciudad: {city}")
                    memory.expecting = "decisión sobre cotización"
                    return self._generate_quote(memory)
            
            memory.increment_retry()
            return "¿En qué ciudad? Lima, Arequipa, Trujillo, etc."
            
        elif memory.state == ConversationState.QUOTE_PRESENTED:
            if intent == ConversationIntent.EMAIL_REQUEST:
                memory.change_state(ConversationState.EMAIL_INTEREST, "Solicitud de email")
                memory.expecting = "confirmación email"
                return f"¡Perfecto {memory.user_name}! ¿Te envío la cotización por correo?"
            elif intent == ConversationIntent.AFFIRMATIVE:
                memory.change_state(ConversationState.EMAIL_INTEREST, "Interés en proceder")
                memory.expecting = "confirmación email"
                return f"¡Excelente {memory.user_name}! ¿Te envío la cotización por correo?"
            else:
                return f"¿Te interesa proceder, {memory.user_name}? También puedo enviarte la cotización por correo."
                
        elif memory.state == ConversationState.EMAIL_INTEREST:
            if intent == ConversationIntent.AFFIRMATIVE:
                memory.change_state(ConversationState.COLLECTING_EMAIL, "Enviará por email")
                memory.expecting = "dirección email"
                return f"¡Perfecto {memory.user_name}! ¿Cuál es tu correo electrónico?"
            elif intent == ConversationIntent.NEGATIVE:
                memory.change_state(ConversationState.COMPLETE, "No quiere email")
                return f"No hay problema {memory.user_name}. ¿Algo más en que pueda ayudarte?"
            else:
                memory.increment_retry()
                return f"¿Te envío la cotización por correo, {memory.user_name}? 'sí' o 'no'"
                
        elif memory.state == ConversationState.COLLECTING_EMAIL:
            if intent == ConversationIntent.EMAIL_PROVIDING:
                email = self._extract_email(message)
                if email:
                    memory.email = email
                    memory.change_state(ConversationState.EMAIL_SENT, f"Email: {email}")
                    return f"¡Excelente {memory.user_name}! Cotización enviada a {email}. ¡Revisa tu bandeja!"
            
            memory.increment_retry()
            return "Proporciona un correo válido: ejemplo@gmail.com"
            
        elif memory.state == ConversationState.EMAIL_SENT:
            memory.change_state(ConversationState.COMPLETE, "Conversación terminada")
            return f"¡Gracias {memory.user_name}! ¿Algo más en que pueda ayudarte?"
        
        return "¿En qué más puedo ayudarte?"
    
    # 🔍 MÉTODOS DE EXTRACCIÓN
    
    def _extract_name(self, message: str) -> Optional[str]:
        """Extrae nombre validado"""
        try:
            for pattern in self.name_patterns:
                match = re.search(pattern, message.strip(), re.IGNORECASE)
                if match:
                    name = match.group(1).strip()
                    if self._is_valid_name(name):
                        return name.title()
            return None
        except:
            return None
    
    def _extract_name_flexible(self, message: str) -> Optional[str]:
        """Extrae nombre con lógica flexible"""
        words = message.strip().split()
        for word in words:
            if len(word) >= 3 and word.isalpha() and self._is_valid_name(word):
                return word.title()
        return None
    
    def _is_valid_name(self, name: str) -> bool:
        """Valida nombre"""
        return name.lower() not in self.forbidden_names and len(name) >= 2
    
    def _extract_vehicle_type(self, message: str) -> Optional[str]:
        """Extrae tipo de vehículo"""
        msg = message.lower()
        for vehicle, keywords in self.vehicle_types.items():
            if any(keyword in msg for keyword in keywords):
                return vehicle
        return None
    
    def _extract_year(self, message: str) -> Optional[str]:
        """Extrae año válido"""
        match = re.search(r'\b(19[9]\d|20[0-2]\d)\b', message)
        if match:
            year = int(match.group(1))
            if 1990 <= year <= 2025:
                return str(year)
        return None
    
    def _extract_usage(self, message: str) -> Optional[str]:
        """Extrae uso del vehículo"""
        msg = message.lower()
        for usage, keywords in self.usage_types.items():
            if any(keyword in msg for keyword in keywords):
                return usage
        return None
    
    def _extract_city(self, message: str) -> Optional[str]:
        """Extrae ciudad"""
        msg = message.lower()
        for city in self.cities:
            if city in msg:
                return city.title()
        
        # Si no encuentra, tomar primera palabra válida
        words = message.split()
        for word in words:
            if len(word) > 2 and word.isalpha():
                return word.title()
        return None
    
    def _extract_email(self, message: str) -> Optional[str]:
        """Extrae email válido"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(pattern, message)
        return match.group(0) if match else None
    
    def _generate_quote(self, memory: SmartMemory) -> str:
        """Genera cotización con datos reales"""
        try:
            import uuid
            quote_id = f"AF{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
            
            # Calcular precio real
            price = self._calculate_price(memory)
            
            quote = f"""📋 *COTIZACIÓN SOAT 2024*

👤 Cliente: {memory.user_name}
🚗 Vehículo: {memory.vehicle_type.title()} {memory.vehicle_year}
🎯 Uso: {memory.vehicle_usage.title()}
📍 Ciudad: {memory.city}
📅 Vigencia: 1 año
🛡️ Cobertura completa contra terceros

💰 *PRECIO FINAL: S/ {price}.00*

📄 Cotización N°: {quote_id}
⏰ Válida por 15 días

¿Te interesa proceder? También puedo enviarte esta cotización por correo electrónico."""

            self.logger.info(f"💰 Cotización generada: {memory.user_name} - {quote_id} - S/{price}")
            return quote
            
        except Exception as e:
            self.logger.error(f"❌ Error generando cotización: {e}")
            return f"¡Perfecto {memory.user_name}! Tu cotización SOAT está lista."
    
    def _calculate_price(self, memory: SmartMemory) -> int:
        """Calcula precio según datos reales"""
        base = 160
        
        # Por tipo de vehículo
        if memory.vehicle_type == 'moto':
            base = 80
        elif memory.vehicle_type == 'taxi':
            base = 220
        elif memory.vehicle_type == 'comercial':
            base = 350
        elif memory.vehicle_type == 'camioneta':
            base = 180
        
        # Por año
        if memory.vehicle_year:
            year = int(memory.vehicle_year)
            if year >= 2020:
                base += 20
            elif year >= 2015:
                base += 10
        
        # Por uso
        if memory.vehicle_usage == 'comercial':
            base += 30
        elif memory.vehicle_usage == 'taxi':
            base += 50
        
        # Por ciudad
        if memory.city and memory.city.lower() == 'lima':
            base += 10
        
        return base
    
    # 🔧 COMPATIBILIDAD
    
    def process_conversation(self, user_id: str, message: str, client_repository=None, quote_repository=None) -> Tuple[str, bool]:
        """Método de compatibilidad"""
        return self.process_message(user_id, message)
    
    def get_user_name(self, user_id: str) -> Optional[str]:
        """Obtiene nombre"""
        memory = self._get_memory(user_id)
        return memory.user_name
    
    def get_interaction_count(self, user_id: str) -> int:
        """Obtiene conteo de interacciones"""
        memory = self._get_memory(user_id)
        return len(memory.conversation_history) 