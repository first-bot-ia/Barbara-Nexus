"""
🛡️ BARBARA CONVERSATION SERVICE - VERSIÓN SÚPER ROBUSTA
Versión simplificada y a prueba de errores

Basado en mejores prácticas de:
- Debugging robusto de Python
- Manejo de errores inteligente
- Arquitectura failsafe
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import logging
import re
from enum import Enum

logger = logging.getLogger(__name__)

class ConversationState(Enum):
    """Estados del flujo conversacional paso a paso"""
    INITIAL = "initial"                    # Estado inicial
    WAITING_NAME = "waiting_name"          # Esperando nombre
    NAME_RECEIVED = "name_received"        # Nombre recibido, preguntar cómo ayudar
    WAITING_HELP_REQUEST = "waiting_help"  # Esperando que diga qué necesita
    COLLECTING_VEHICLE_TYPE = "vehicle_type"     # Pidiendo tipo de vehículo  
    COLLECTING_VEHICLE_YEAR = "vehicle_year"     # Pidiendo año del vehículo
    COLLECTING_VEHICLE_USAGE = "vehicle_usage"   # Pidiendo uso del vehículo
    COLLECTING_CITY = "collecting_city"          # Pidiendo ciudad
    READY_TO_QUOTE = "ready_to_quote"           # Listo para generar cotización
    QUOTE_GENERATED = "quote_generated"         # Cotización generada
    ASKING_EMAIL = "asking_email"               # Preguntando si quiere por email
    WAITING_EMAIL = "waiting_email"             # Esperando dirección de email
    EMAIL_CONFIRMED = "email_confirmed"         # Email confirmado y enviado
    CONVERSATION_COMPLETE = "complete"          # Conversación completada

class RobustConversationMemory:
    """Memoria conversacional súper simple y robusta con estados"""
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.user_name: Optional[str] = None
        self.interactions: List[Dict] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # 🎯 ESTADOS CONVERSACIONALES PARA FLUJO PASO A PASO
        self.conversation_state = ConversationState.INITIAL
        self.vehicle_type: Optional[str] = None
        self.vehicle_year: Optional[str] = None
        self.vehicle_usage: Optional[str] = None
        self.city: Optional[str] = None
        self.email: Optional[str] = None
        self.quote_data: Optional[Dict] = None
        
        # 🚨 DETECCIÓN Y PREVENCIÓN DE BUCLES INFINITOS
        self.loop_detection_count: int = 0
        self.last_response: str = ""
        self.retry_count_per_state: Dict[str, int] = {}
    
    def set_name(self, name: str) -> bool:
        """Establece nombre del usuario de forma segura"""
        try:
            if name and len(name.strip()) >= 2:
                self.user_name = name.strip().title()
                self.updated_at = datetime.now()
                return True
        except Exception:
            pass
        return False
    
    def add_interaction(self, user_message: str, bot_response: str) -> bool:
        """Agrega interacción de forma segura"""
        try:
            interaction = {
                "timestamp": datetime.now().isoformat(),
                "user": user_message[:200],  # Limitar tamaño
                "bot": bot_response[:200]
            }
            self.interactions.append(interaction)
            
            # Mantener solo últimas 10 interacciones
            if len(self.interactions) > 10:
                self.interactions.pop(0)
            
            self.updated_at = datetime.now()
            return True
        except Exception:
            return False

class BarbaraConversationServiceRobust:
    """
    Versión SÚPER ROBUSTA de Barbara
    - Sin dependencias complejas
    - Manejo de errores exhaustivo
    - Funcionalidad garantizada
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.memories: Dict[str, RobustConversationMemory] = {}
        
        # Patrones simples para extracción de nombres
        self.name_patterns = [
            r'soy\s+([A-Za-záéíóúÁÉÍÓÚñÑ]{2,20})',
            r'me\s+llamo\s+([A-Za-záéíóúÁÉÍÓÚñÑ]{2,20})',
            r'mi\s+nombre\s+es\s+([A-Za-záéíóúÁÉÍÓÚñÑ]{2,20})',
            r'^([A-Za-záéíóúÁÉÍÓÚñÑ]{3,20})$'  # Solo nombre
        ]
        
        # Palabras prohibidas como nombres
        self.forbidden_names = {
            'hola', 'barbara', 'auto', 'moto', 'soat', 'cotizar', 
            'quiero', 'precio', 'gracias', 'si', 'no', 'ok'
        }
    
    def process_message(self, user_id: str, message: str) -> Tuple[str, bool]:
        """
        Procesa mensaje de forma SÚPER ROBUSTA
        
        Returns:
            (response, needs_quote)
        """
        try:
            # 1. Obtener o crear memoria de forma segura
            memory = self._get_memory(user_id)
            
            # 2. Intentar extraer nombre si no lo tenemos
            if not memory.user_name:
                extracted_name = self._extract_name_safe(message)
                if extracted_name:
                    if memory.set_name(extracted_name):
                        self.logger.info(f"👤 Nombre capturado: {extracted_name}")
            
            # 3. Detectar si necesita cotización
            needs_quote = self._needs_quotation(message)
            
            # 4. Generar respuesta robusta
            response = self._generate_response_safe(memory, message, needs_quote)
            
            # 5. Guardar interacción de forma segura
            memory.add_interaction(message, response)
            
            return response, needs_quote
            
        except Exception as e:
            # Manejo de error súper robusto
            self.logger.error(f"❌ Error en process_message: {e}")
            return self._get_fallback_response(), False
    
    def _get_memory(self, user_id: str) -> RobustConversationMemory:
        """Obtiene memoria de forma súper segura"""
        try:
            if user_id not in self.memories:
                self.memories[user_id] = RobustConversationMemory(user_id)
            return self.memories[user_id]
        except Exception:
            # Crear memoria temporal si falla
            return RobustConversationMemory(user_id or "temp_user")
    
    def _extract_name_safe(self, message: str) -> Optional[str]:
        """Extrae nombre de forma súper segura"""
        try:
            message_clean = message.strip().lower()
            
            # Probar cada patrón
            for pattern in self.name_patterns:
                match = re.search(pattern, message_clean, re.IGNORECASE)
                if match:
                    potential_name = match.group(1).strip()
                    
                    # Validar que no sea palabra prohibida
                    if potential_name.lower() not in self.forbidden_names:
                        self.logger.info(f"✅ Nombre extraído: {potential_name}")
                        return potential_name.title()
            
            return None
            
        except Exception as e:
            self.logger.warning(f"⚠️ Error extrayendo nombre: {e}")
            return None
    
    def _needs_quotation(self, message: str) -> bool:
        """Detecta si necesita cotización de forma robusta y contextual - MEJORADO PARA PERUANO"""
        try:
            message_lower = message.lower().strip()
            
            # 🎯 PALABRAS EXPLÍCITAS DE COTIZACIÓN
            quote_keywords = ['cotizar', 'cotización', 'precio', 'costo', 'soat', 'seguro', 'cuanto', 'vale', 'tarifas', 'cuánto cuesta']
            if any(keyword in message_lower for keyword in quote_keywords):
                return True
            
            # 🔄 RESPUESTAS AFIRMATIVAS PERUANAS
            affirmative_keywords = [
                'si', 'sí', 'yes', 'claro', 'perfecto', 'dale', 'por favor', 'quiero', 'necesito',
                'ya', 'oe si', 'asu', 'bacán', 'jato', 'palta', 'chevere', 'buenazo', 'genial',
                'obvio', 'por supuesto', 'asu mare', 'bueno', 'ok', 'vale', 'simon', 'listo'
            ]
            if any(keyword == message_lower or keyword in message_lower for keyword in affirmative_keywords):
                return True
            
            # 🚗 MENCIONES DE VEHÍCULOS PERUANAS
            vehicle_keywords = ['auto', 'carro', 'vehículo', 'moto', 'taxi', 'camioneta', 'carrito', 'nave', 'fierro']
            if any(keyword in message_lower for keyword in vehicle_keywords):
                return True
                
            return False
        except Exception:
            return False
    
    def _generate_response_safe(self, memory: RobustConversationMemory, message: str, needs_quote: bool) -> str:
        """Genera respuesta ULTRA-INTELIGENTE que evita bucles infinitos"""
        try:
            message_lower = message.lower().strip()
            current_state = memory.conversation_state
            
            # 🚨 DETECTOR DE BUCLES INFINITOS
            if hasattr(memory, 'loop_detection_count'):
                memory.loop_detection_count += 1
            else:
                memory.loop_detection_count = 1
                memory.last_response = ""
                memory.retry_count_per_state = {}
            
            # 🔄 SI ESTÁ EN BUCLE, FORZAR PROGRESIÓN
            state_key = current_state.value
            if state_key not in memory.retry_count_per_state:
                memory.retry_count_per_state[state_key] = 0
            
            memory.retry_count_per_state[state_key] += 1
            
            # SI YA INTENTÓ 3 VECES EN EL MISMO ESTADO, FORZAR AVANCE
            if memory.retry_count_per_state[state_key] >= 3:
                return self._force_conversation_progress(memory, message, current_state)
            
            # 🎯 FLUJO CONVERSACIONAL PASO A PASO MEJORADO
            
            # Estado INICIAL - Solo saludos
            if current_state == ConversationState.INITIAL:
                memory.conversation_state = ConversationState.WAITING_NAME
                memory.retry_count_per_state = {}  # Reset counters
                return "¡Hola! Soy Barbara de Autofondo Alese. ¿Cómo te llamas?"
            
            # Estado ESPERANDO NOMBRE
            elif current_state == ConversationState.WAITING_NAME:
                name = self._extract_name_safe(message)
                if name:
                    memory.user_name = name
                    memory.conversation_state = ConversationState.NAME_RECEIVED
                    memory.retry_count_per_state = {}  # Reset counters
                    return f"Mucho gusto {name}. Soy especialista en SOAT. ¿En qué puedo ayudarte?"
                else:
                    # ESTRATEGIA ANTI-BUCLE: Extracción flexible
                    flexible_name = self._extract_name_flexible(message)
                    if flexible_name:
                        memory.user_name = flexible_name
                        memory.conversation_state = ConversationState.NAME_RECEIVED
                        memory.retry_count_per_state = {}
                        return f"Perfecto {flexible_name}. Soy especialista en SOAT. ¿Te interesa una cotización?"
                    return "Solo escribe tu nombre, por favor. Ejemplo: 'Juan'"
            
            # Estado NOMBRE RECIBIDO - Preguntar cómo ayudar
            elif current_state == ConversationState.NAME_RECEIVED:
                if needs_quote or any(word in message_lower for word in ['cotizar', 'cotización', 'soat', 'seguro', 'si', 'sí', 'quiero', 'necesito']):
                    memory.conversation_state = ConversationState.COLLECTING_VEHICLE_TYPE
                    memory.retry_count_per_state = {}
                    return f"¡Excelente {memory.user_name}! Para tu cotización SOAT, ¿qué tipo de vehículo tienes? (auto, moto, taxi, camioneta)"
                else:
                    return f"Entiendo {memory.user_name}. ¿Te interesa una cotización de SOAT? (responde 'sí' o 'no')"
            
            # Estado RECOPILANDO TIPO DE VEHÍCULO
            elif current_state == ConversationState.COLLECTING_VEHICLE_TYPE:
                vehicle_type = self._extract_vehicle_type(message)
                if vehicle_type:
                    memory.vehicle_type = vehicle_type
                    memory.conversation_state = ConversationState.COLLECTING_VEHICLE_YEAR
                    return f"Perfecto, {vehicle_type}. ¿De qué año es tu vehículo?"
                else:
                    return "Por favor especifica el tipo de vehículo: auto, moto, taxi, camioneta, etc."
            
            # Estado RECOPILANDO AÑO
            elif current_state == ConversationState.COLLECTING_VEHICLE_YEAR:
                year = self._extract_year(message)
                if year:
                    memory.vehicle_year = year
                    memory.conversation_state = ConversationState.COLLECTING_VEHICLE_USAGE
                    return f"Excelente, año {year}. ¿Cuál es el uso principal? (particular, trabajo, comercial)"
                else:
                    return "Por favor indica el año de tu vehículo (ej: 2020, 2023, etc.)"
            
            # Estado RECOPILANDO USO
            elif current_state == ConversationState.COLLECTING_VEHICLE_USAGE:
                usage = self._extract_usage(message)
                if usage:
                    memory.vehicle_usage = usage
                    memory.conversation_state = ConversationState.COLLECTING_CITY
                    return f"Perfecto, uso {usage}. ¿En qué ciudad lo usas principalmente?"
                else:
                    return "Especifica el uso: particular, trabajo, comercial, taxi, etc."
            
            # Estado RECOPILANDO CIUDAD
            elif current_state == ConversationState.COLLECTING_CITY:
                city = self._extract_city(message)
                if city:
                    memory.city = city
                    # ✅ GENERAR COTIZACIÓN CON DATOS REALES Y PREGUNTAR POR CORREO
                    quote_response = self._generate_complete_quote(memory)
                    # Agregar pregunta por correo inmediatamente después de la cotización
                    quote_response += f"\n\n¿Te gustaría que te envíe esta cotización por correo electrónico, {memory.user_name}?"
                    memory.conversation_state = ConversationState.ASKING_EMAIL
                    return quote_response
                else:
                    return "¿En qué ciudad usas tu vehículo? (Lima, Arequipa, Trujillo, etc.)"
            
            # Estado PREGUNTANDO POR EMAIL  
            elif current_state == ConversationState.ASKING_EMAIL:
                # 🇵🇪 RESPUESTAS AFIRMATIVAS PERUANAS MEJORADAS
                if any(word in message_lower for word in [
                    'si', 'sí', 'yes', 'claro', 'perfecto', 'dale', 'por favor', 'quiero', 'ok',
                    'ya', 'oe si', 'asu', 'bacán', 'jato', 'palta', 'chevere', 'buenazo', 'genial',
                    'obvio', 'por supuesto', 'asu mare', 'bueno', 'vale', 'simon', 'listo', 'mandalo',
                    'envialo', 'manda', 'envia', 'correo', 'email', 'gmail'
                ]):
                    memory.conversation_state = ConversationState.WAITING_EMAIL
                    return f"¡Perfecto {memory.user_name}! ¿Cuál es tu correo electrónico?"
                # 🇵🇪 RESPUESTAS NEGATIVAS PERUANAS
                elif any(word in message_lower for word in [
                    'no', 'nah', 'mejor no', 'paso', 'nop', 'nel', 'ni loco', 'que va', 'nones'
                ]):
                    memory.conversation_state = ConversationState.CONVERSATION_COMPLETE
                    return f"¡Perfecto {memory.user_name}! Tu cotización está lista. Para más información puedes llamar al +51 999 888 777. ¡Gracias por contactarnos!"
                else:
                    return f"¿Te gustaría que te envíe la cotización por correo electrónico, {memory.user_name}? (responde 'sí' o 'no')"
            
            # Estado COTIZACIÓN GENERADA (ya no se usa, reemplazado por ASKING_EMAIL)
            elif current_state == ConversationState.QUOTE_GENERATED:
                if self._mentions_email(message):
                    memory.conversation_state = ConversationState.WAITING_EMAIL
                    return f"¡Perfecto {memory.user_name}! ¿Cuál es tu correo electrónico?"
                elif any(word in message_lower for word in ['comprar', 'compra', 'proceder', 'ok', 'si']):
                    memory.conversation_state = ConversationState.ASKING_EMAIL
                    return f"¡Excelente {memory.user_name}! ¿Te gustaría que te envíe la cotización por correo?"
                else:
                    return "¿Te gustaría proceder con la compra o necesitas que te envíe la cotización por correo?"
            
            # Estado ESPERANDO EMAIL
            elif current_state == ConversationState.WAITING_EMAIL:
                email = self._extract_email(message)
                if email:
                    memory.email = email
                    memory.conversation_state = ConversationState.EMAIL_CONFIRMED
                    return f"¡Perfecto {memory.user_name}! He enviado tu cotización a {email}. ¡Revisa tu bandeja de entrada!"
                else:
                    return "Por favor proporciona un correo válido (ej: tu@email.com)"
            
            # Estado FINAL
            elif current_state == ConversationState.EMAIL_CONFIRMED:
                return f"¡Gracias {memory.user_name}! ¿Hay algo más en lo que pueda ayudarte?"
            
            # Estado por defecto
            else:
                memory.conversation_state = ConversationState.INITIAL
                return "¡Hola! Soy Barbara de Autofondo Alese. ¿Cómo puedo ayudarte?"
                
        except Exception as e:
            self.logger.error(f"❌ Error en flujo conversacional: {e}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> str:
        """Respuesta de emergencia súper robusta"""
        return "¡Hola! Soy Barbara de Autofondo Alese. ¿Cómo puedo ayudarte con tu SOAT?"
    
    def get_user_name(self, user_id: str) -> Optional[str]:
        """Obtiene nombre de usuario de forma segura"""
        try:
            memory = self._get_memory(user_id)
            return memory.user_name
        except Exception:
            return None
    
    def get_interaction_count(self, user_id: str) -> int:
        """Obtiene número de interacciones de forma segura"""
        try:
            memory = self._get_memory(user_id)
            return len(memory.interactions)
        except Exception:
            return 0
    
    # 🔧 MÉTODOS DE COMPATIBILIDAD CON INTERFAZ ORIGINAL
    
    def process_conversation(self, user_id: str, message: str, client_repository=None, quote_repository=None) -> Tuple[str, bool]:
        """Método de compatibilidad - usa process_message internamente"""
        return self.process_message(user_id, message)
    
    def get_memory_summary(self, user_id: str) -> Dict[str, Any]:
        """Obtiene resumen de memoria compatible con interfaz original"""
        try:
            memory = self._get_memory(user_id)
            return {
                'interactions': len(memory.interactions),
                'status': 'active_client' if memory.user_name else 'new_client',
                'client_name': memory.user_name,
                'conversation_stage': 'greeting' if not memory.user_name else 'named',
                'presentation_done': memory.user_name is not None,
                'quote_requested': False,
                'quote_generated': False
            }
        except Exception:
            return {
                'interactions': 0,
                'status': 'new_client',
                'client_name': None,
                'conversation_stage': 'greeting',
                'presentation_done': False,
                'quote_requested': False,
                'quote_generated': False
            }
    
    def get_or_create_memory(self, user_id: str):
        """Método de compatibilidad - retorna objeto memoria compatible"""
        try:
            memory = self._get_memory(user_id)
            
            # Crear objeto compatible con interfaz original
            class CompatibleMemory:
                def __init__(self, robust_memory):
                    self.user_id = robust_memory.user_id
                    self.user_profile = {'nombre': robust_memory.user_name} if robust_memory.user_name else {}
                    self.short_term_context = []
                    self.conversation_stage = 'greeting'
                    self.emotional_state = 'neutral'
            
            return CompatibleMemory(memory)
        except Exception:
            # Memoria de emergencia
            class EmergencyMemory:
                def __init__(self):
                    self.user_profile = {}
                    self.short_term_context = []
                    self.conversion_stage = 'greeting'
                    self.emotional_state = 'neutral'
            
            return EmergencyMemory()
    
    def _extract_name_with_advanced_ner(self, message: str) -> Optional[str]:
        """Método de compatibilidad - usa _extract_name_safe internamente"""
        return self._extract_name_safe(message)
    
    def _extract_name_flexible(self, message: str) -> Optional[str]:
        """Extracción flexible de nombres para romper bucles infinitos"""
        try:
            # Dividir mensaje en palabras
            words = message.strip().split()
            
            # Buscar cualquier palabra que pueda ser un nombre
            for word in words:
                if len(word) >= 3 and word.isalpha():
                    # Verificar que no sea palabra prohibida
                    if word.lower() not in self.forbidden_names:
                        self.logger.info(f"✅ Nombre extraído flexiblemente: {word}")
                        return word.title()
            
            # Si no encuentra nada, tomar la primera palabra con más de 2 caracteres
            for word in words:
                if len(word) > 2:
                    clean_word = ''.join(char for char in word if char.isalpha())
                    if clean_word and clean_word.lower() not in self.forbidden_names:
                        self.logger.info(f"✅ Nombre extraído por último recurso: {clean_word}")
                        return clean_word.title()
            
            return None
            
        except Exception as e:
            self.logger.warning(f"⚠️ Error en extracción flexible de nombre: {e}")
            return None
    
    def _force_conversation_progress(self, memory: RobustConversationMemory, message: str, current_state: ConversationState) -> str:
        """Fuerza el progreso conversacional para romper bucles infinitos"""
        try:
            self.logger.warning(f"🔄 FORZANDO PROGRESO - Estado: {current_state.value}, Reintentos: {memory.retry_count_per_state.get(current_state.value, 0)}")
            
            # ESTRATEGIAS ESPECÍFICAS SEGÚN EL ESTADO
            
            if current_state == ConversationState.WAITING_NAME:
                # Forzar extracción de nombre más agresiva
                flexible_name = self._extract_name_flexible(message)
                if flexible_name:
                    memory.user_name = flexible_name
                    memory.conversation_state = ConversationState.NAME_RECEIVED
                    memory.retry_count_per_state = {}
                    return f"Perfecto {flexible_name}. Soy Barbara, especialista en SOAT. ¿Te interesa una cotización?"
                else:
                    # Último recurso: pedir que escriba solo el nombre
                    return "Escribe solo tu nombre en una palabra, por favor. Ejemplo: 'Juan'"
            
            elif current_state == ConversationState.NAME_RECEIVED:
                # Asumir que quiere cotización si llegó hasta aquí
                memory.conversation_state = ConversationState.COLLECTING_VEHICLE_TYPE
                memory.retry_count_per_state = {}
                return f"Entiendo {memory.user_name}. Vamos a hacer tu cotización SOAT. ¿Qué tipo de vehículo tienes? (auto, moto, taxi, camioneta)"
            
            elif current_state == ConversationState.COLLECTING_VEHICLE_TYPE:
                # Asumir auto por defecto
                memory.vehicle_type = "auto"
                memory.conversation_state = ConversationState.COLLECTING_VEHICLE_YEAR
                memory.retry_count_per_state = {}
                return f"Asumiré que es un auto. ¿De qué año es tu vehículo? (ejemplo: 2020, 2015)"
            
            elif current_state == ConversationState.COLLECTING_VEHICLE_YEAR:
                # Asumir año 2020 por defecto
                memory.vehicle_year = "2020"
                memory.conversation_state = ConversationState.COLLECTING_VEHICLE_USAGE
                memory.retry_count_per_state = {}
                return f"Asumiré año 2020. ¿Cuál es el uso principal? (particular, trabajo, comercial)"
            
            elif current_state == ConversationState.COLLECTING_VEHICLE_USAGE:
                # Asumir uso particular
                memory.vehicle_usage = "particular"
                memory.conversation_state = ConversationState.COLLECTING_CITY
                memory.retry_count_per_state = {}
                return f"Asumiré uso particular. ¿En qué ciudad usas tu vehículo? (Lima, Arequipa, etc.)"
            
            elif current_state == ConversationState.COLLECTING_CITY:
                # Asumir Lima y generar cotización
                memory.city = "Lima"
                memory.conversation_state = ConversationState.QUOTE_GENERATED
                memory.retry_count_per_state = {}
                return self._generate_complete_quote(memory)
            
            elif current_state == ConversationState.QUOTE_GENERATED:
                # Preguntar por email
                memory.conversation_state = ConversationState.ASKING_EMAIL
                memory.retry_count_per_state = {}
                return f"¿Te gustaría que te envíe esta cotización por correo electrónico, {memory.user_name}?"
            
            elif current_state == ConversationState.ASKING_EMAIL:
                # Asumir que sí quiere email
                memory.conversation_state = ConversationState.WAITING_EMAIL
                memory.retry_count_per_state = {}
                return f"¡Perfecto {memory.user_name}! ¿Cuál es tu dirección de correo electrónico?"
            
            elif current_state == ConversationState.WAITING_EMAIL:
                # Intentar extraer email o asumir uno genérico
                email = self._extract_email(message)
                if email:
                    memory.email = email
                    memory.conversation_state = ConversationState.EMAIL_CONFIRMED
                    memory.retry_count_per_state = {}
                    return f"¡Excelente {memory.user_name}! He enviado tu cotización a {email}. ¡Revisa tu bandeja de entrada!"
                else:
                    return "Por favor proporciona un correo válido. Ejemplo: tu@email.com"
            
            # ÚLTIMO RECURSO: Reiniciar conversación
            else:
                memory.conversation_state = ConversationState.INITIAL
                memory.retry_count_per_state = {}
                return f"Reiniciemos, {memory.user_name or 'amigo'}. ¿En qué puedo ayudarte con tu SOAT?"
                
        except Exception as e:
            self.logger.error(f"❌ Error forzando progreso: {e}")
            return "¡Hola! Soy Barbara de Autofondo Alese. Empecemos de nuevo. ¿Cómo te llamas?"
    
    def _generate_instant_quote(self, name: str) -> str:
        """Genera cotización instantánea cuando el usuario confirma que quiere cotizar"""
        try:
            import uuid
            from datetime import datetime, timedelta
            
            # Generar cotización única
            quote_id = f"AF{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
            precio = 160  # Precio estándar SOAT 2024
            
            quote_response = f"""📋 *COTIZACIÓN SOAT 2024*

👤 Cliente: {name}
🚗 Vehículo: Auto particular
📅 Vigencia: 1 año
🛡️ Cobertura completa contra terceros

💰 *PRECIO FINAL: S/ {precio}.00*

📄 Cotización N°: {quote_id}
⏰ Válida por 15 días

¿Te gustaría proceder con la compra o necesitas más información?

📧 También puedo enviarte esta cotización por correo electrónico
📞 Para finalizar tu SOAT: +51 999 888 777"""

            self.logger.info(f"💰 Cotización instantánea generada para {name}: {quote_id}")
            return quote_response
            
        except Exception as e:
            self.logger.error(f"❌ Error generando cotización instantánea: {e}")
            return f"¡Perfecto {name}! Te ayudo con tu cotización SOAT. ¿Qué tipo de vehículo tienes?" 
    
    # 🛠️ MÉTODOS AUXILIARES PARA FLUJO CONVERSACIONAL PASO A PASO
    
    def _extract_vehicle_type(self, message: str) -> Optional[str]:
        """Extrae tipo de vehículo del mensaje"""
        try:
            message_lower = message.lower().strip()
            
            vehicle_mapping = {
                'auto': 'auto',
                'carro': 'auto', 
                'automóvil': 'auto',
                'particular': 'auto',
                'moto': 'moto',
                'motocicleta': 'moto',
                'taxi': 'taxi',
                'camioneta': 'camioneta',
                'pickup': 'camioneta',
                'suv': 'camioneta',
                'comercial': 'comercial',
                'camión': 'comercial'
            }
            
            for keyword, vehicle_type in vehicle_mapping.items():
                if keyword in message_lower:
                    return vehicle_type
            
            return None
        except Exception:
            return None
    
    def _extract_year(self, message: str) -> Optional[str]:
        """Extrae año del mensaje"""
        try:
            import re
            # Buscar años entre 1990 y 2025
            year_match = re.search(r'\b(19[9]\d|20[0-2]\d)\b', message)
            if year_match:
                return year_match.group(1)
            return None
        except Exception:
            return None
    
    def _extract_usage(self, message: str) -> Optional[str]:
        """Extrae uso del vehículo"""
        try:
            message_lower = message.lower().strip()
            
            usage_mapping = {
                'particular': 'particular',
                'personal': 'particular',
                'trabajo': 'trabajo',
                'laboral': 'trabajo',
                'comercial': 'comercial',
                'negocio': 'comercial',
                'taxi': 'taxi',
                'uber': 'taxi'
            }
            
            for keyword, usage in usage_mapping.items():
                if keyword in message_lower:
                    return usage
            
            return None
        except Exception:
            return None
    
    def _extract_city(self, message: str) -> Optional[str]:
        """Extrae ciudad del mensaje"""
        try:
            message_lower = message.lower().strip()
            
            cities = ['lima', 'arequipa', 'trujillo', 'chiclayo', 'piura', 'iquitos', 'cusco', 'huancayo', 'tacna', 'ica']
            
            for city in cities:
                if city in message_lower:
                    return city.title()
            
            # Si no encuentra ciudad conocida, tomar primera palabra como ciudad
            words = message.split()
            if words and len(words[0]) > 2:
                return words[0].title()
            
            return None
        except Exception:
            return None
    
    def _generate_complete_quote(self, memory: RobustConversationMemory) -> str:
        """Genera cotización completa con todos los datos recopilados"""
        try:
            import uuid
            from datetime import datetime
            
            quote_id = f"AF{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
            
            # Calcular precio según datos reales recopilados
            base_price = 140
            if memory.vehicle_type == 'moto':
                base_price = 80
            elif memory.vehicle_type == 'taxi':
                base_price = 200
            elif memory.vehicle_type == 'comercial':
                base_price = 300
            
            # Ajustar por año
            if memory.vehicle_year:
                year = int(memory.vehicle_year)
                if year >= 2020:
                    base_price += 20
                elif year >= 2010:
                    base_price += 10
            
            # Guardar datos de cotización en memoria
            memory.quote_data = {
                'quote_id': quote_id,
                'price': base_price,
                'vehicle_type': memory.vehicle_type,
                'year': memory.vehicle_year,
                'usage': memory.vehicle_usage,
                'city': memory.city
            }
            
            # ✅ NO cambiar estado aquí - se maneja externamente
            # memory.conversation_state = ConversationState.QUOTE_GENERATED
            
            quote_response = f"""📋 *COTIZACIÓN SOAT 2024*

👤 Cliente: {memory.user_name}
🚗 Vehículo: {memory.vehicle_type.title() if memory.vehicle_type else 'Auto'} {memory.vehicle_year or '2024'}
🎯 Uso: {memory.vehicle_usage.title() if memory.vehicle_usage else 'Particular'}
📍 Ciudad: {memory.city or 'Lima'}
📅 Vigencia: 1 año
🛡️ Cobertura completa contra terceros

💰 *PRECIO FINAL: S/ {base_price}.00*

📄 Cotización N°: {quote_id}
⏰ Válida por 15 días

📞 Para más información: +51 999 888 777"""

            self.logger.info(f"💰 Cotización completa generada para {memory.user_name}: {quote_id}")
            return quote_response
            
        except Exception as e:
            self.logger.error(f"❌ Error generando cotización completa: {e}")
            return f"¡Excelente {memory.user_name}! Tu cotización está lista."
    
    def _mentions_email(self, message: str) -> bool:
        """Detecta si menciona correo/email"""
        try:
            message_lower = message.lower()
            email_keywords = ['correo', 'email', 'mail', '@', 'gmail', 'hotmail', 'yahoo']
            return any(word in message_lower for word in email_keywords)
        except Exception:
            return False
    
    def _extract_email(self, message: str) -> Optional[str]:
        """Extrae email del mensaje"""
        try:
            import re
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            match = re.search(email_pattern, message)
            if match:
                return match.group(0)
            return None
        except Exception:
            return None