"""
🏗️ Domain Service: Barbara Conversation Service
Siguiendo principios de Domain-Driven Design (DDD)
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import time
import random
import re
import logging
import json
from dataclasses import dataclass, asdict

# Importaciones del dominio
from ..entities.cliente import Cliente
from ..aggregates.cotizacion import TipoVehiculo
from .barbara_personality_service import BarbaraPersonalityService, EmotionalState, ConversationIntent

logger = logging.getLogger(__name__)

# Importar NER avanzado
try:
    from infrastructure.external_apis.spacy_ner_service import SpacyNERService
    NER_AVAILABLE = True
except ImportError:
    NER_AVAILABLE = False
    logger.warning("⚠️ spaCy NER no disponible, usando regex fallback")

@dataclass
class ConversationMemory:
    """Memoria conversacional estructurada"""
    user_id: str
    short_term_context: Optional[List[Dict]] = None  # Últimos 5 intercambios
    long_term_summary: str = ""  # Resumen de la conversación completa
    user_profile: Optional[Dict] = None  # Perfil del usuario (nombre, preferencias, etc.)
    emotional_state: str = "neutral"  # Estado emocional detectado
    conversation_stage: str = "greeting"  # Etapa de la conversación
    last_intent: str = ""  # Último intent detectado
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.short_term_context is None:
            self.short_term_context = []
        if self.user_profile is None:
            self.user_profile = {}
        if self.created_at is None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()

class BarbaraConversationService:
    """
    Domain Service: Servicio de conversación de Barbara
    
    Siguiendo DDD: Los domain services contienen lógica de negocio
    que no pertenece naturalmente a ninguna entidad o value object
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.spacy_service = SpacyNERService()
        self.conversation_memories: Dict[str, ConversationMemory] = {}
        
        # 🎭 Nuevo servicio de personalidad avanzado
        self.personality_service = BarbaraPersonalityService()
        
        # Patrones emocionales para detección de estado
        self.emotional_patterns = {
            "frustrated": ["no entiendo", "no funciona", "problema", "error", "mal"],
            "excited": ["excelente", "perfecto", "genial", "súper", "fantástico"],
            "confused": ["no sé", "confundido", "help", "ayuda", "qué"],
            "satisfied": ["gracias", "perfecto", "bien", "ok", "correcto"]
        }
        
        self.typing_delays = {
            'short': (0.8, 1.5),
            'medium': (1.2, 2.0), 
            'long': (1.8, 2.5),
            'thinking': (0.3, 0.8),
            'cotizacion': (2.0, 3.5)
        }
    
    def process_conversation(self, user_id: str, message: str, client_repository, quote_repository) -> Tuple[str, bool]:
        """Procesa la conversación con memoria contextual mejorada"""
        try:
            # Obtener memoria conversacional
            memory = self.get_or_create_memory(user_id)
            
            # Procesar extracción de nombres
            name = self._extract_name_with_advanced_ner(message)
            
            if name and self._is_valid_name(name):
                memory.user_profile['nombre'] = name
                self.logger.info(f"👤 Nombre guardado en memoria: {name}")
            
            # Detectar si necesita cotización
            needs_quote = any(word in message.lower() for word in ['cotizar', 'cotización', 'precio', 'costo', 'soat'])
            
            # Generar respuesta básica
            if memory.user_profile.get('nombre'):
                if needs_quote:
                    response = f"¡Perfecto {memory.user_profile['nombre']}! Voy a preparar tu cotización SOAT. ¿Qué tipo de vehículo tienes?"
                else:
                    response = f"¡Hola {memory.user_profile['nombre']}! ¿En qué puedo ayudarte hoy?"
            else:
                if "hola" in message.lower():
                    response = "¡Hola! Soy Barbara, tu asesora digital de Autofondo Alese. ¿Cómo te llamas?"
                else:
                    response = "¡Hola! ¿Cómo puedo ayudarte con tu SOAT?"
            
            # Actualizar contexto conversacional
            self.update_conversation_context(user_id, message, response)
            
            return response, needs_quote
            
        except Exception as e:
            self.logger.error(f"❌ Error en process_conversation: {e}")
            return "¡Hola! Soy Barbara, ¿cómo puedo ayudarte?", False
    
    def get_or_create_memory(self, user_id: str) -> ConversationMemory:
        """Obtiene o crea la memoria conversacional del usuario"""
        if user_id not in self.conversation_memories:
            self.conversation_memories[user_id] = ConversationMemory(user_id=user_id)
        return self.conversation_memories[user_id]
    
    def detect_emotional_state(self, message: str) -> str:
        """Detecta el estado emocional del usuario basado en su mensaje"""
        message_lower = message.lower()
        
        for emotion, keywords in self.emotional_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                return emotion
        
        return "neutral"

    def update_conversation_context(self, user_id: str, user_message: str, bot_response: str):
        """Actualiza el contexto conversacional"""
        memory = self.get_or_create_memory(user_id)
        
        # Detectar estado emocional
        emotional_state = self.detect_emotional_state(user_message)
        memory.emotional_state = emotional_state
        
        # Agregar al contexto a corto plazo
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "bot_response": bot_response,
            "emotional_state": emotional_state
        }
        
        if memory.short_term_context is not None:
            memory.short_term_context.append(interaction)
            
            # Mantener solo los últimos 5 intercambios en memoria corta
            if len(memory.short_term_context) > 5:
                # Mover el más antiguo al resumen de largo plazo
                old_interaction = memory.short_term_context.pop(0)
                self._update_long_term_summary(memory, old_interaction)
        
        memory.updated_at = datetime.now()
        
        self.logger.info(f"🧠 Contexto actualizado para {user_id}: estado={emotional_state}")

    def _update_long_term_summary(self, memory: ConversationMemory, interaction: Dict):
        """Actualiza el resumen de largo plazo"""
        if not memory.long_term_summary:
            memory.long_term_summary = f"Historial: Usuario mostró interés en seguros. "
        
        # Agregar información clave del intercambio al resumen
        if "cotización" in interaction["user_message"].lower():
            memory.long_term_summary += f"Solicitó cotización. "
        if "vehículo" in interaction["user_message"].lower():
            memory.long_term_summary += f"Consultó sobre vehículos. "

    def get_contextual_prompt_enhancement(self, user_id: str, base_prompt: str) -> str:
        """Mejora el prompt con contexto conversacional y personalidad"""
        memory = self.get_or_create_memory(user_id)
        
        # Contexto de personalidad de Barbara
        personality_context = """
        PERSONALIDAD DE BARBARA (OCEAN):
        - Apertura: Muy creativa e innovadora en soluciones de seguros
        - Responsabilidad: Extremadamente detallista y confiable
        - Extroversión: Amigable pero profesional
        - Amabilidad: Muy empática y cooperativa
        - Estabilidad: Siempre calmada y positiva
        """
        
        # Contexto emocional
        emotional_context = f"\nESTADO EMOCIONAL DETECTADO: {memory.emotional_state}"
        if memory.emotional_state == "frustrated":
            emotional_context += "\n[Responde con extra paciencia y comprensión]"
        elif memory.emotional_state == "excited":
            emotional_context += "\n[Mantén el entusiasmo y sé celebrativa]"
        elif memory.emotional_state == "confused":
            emotional_context += "\n[Explica de manera más simple y clara]"
        
        # Contexto de conversación
        conversation_context = ""
        if memory.short_term_context:
            conversation_context = "\nCONTEXTO RECIENTE:\n"
            for interaction in memory.short_term_context[-2:]:  # Últimos 2 intercambios
                conversation_context += f"Usuario: {interaction['user_message'][:100]}...\n"
                conversation_context += f"Barbara: {interaction['bot_response'][:100]}...\n"
        
        # Contexto de perfil de usuario
        profile_context = ""
        if memory.user_profile:
            profile_context = f"\nPERFIL USUARIO:\n"
            if memory.user_profile.get('nombre'):
                profile_context += f"Nombre: {memory.user_profile['nombre']}\n"
            if memory.user_profile.get('vehiculo_preferido'):
                profile_context += f"Vehículo preferido: {memory.user_profile['vehiculo_preferido']}\n"
        
        enhanced_prompt = f"""
        {base_prompt}
        
        {personality_context}
        {emotional_context}
        {conversation_context}
        {profile_context}
        
        INSTRUCCIONES ESPECIALES:
        - Mantén la consistencia con la personalidad de Barbara establecida
        - Adapta tu respuesta al estado emocional del usuario
        - Utiliza el contexto de conversaciones previas cuando sea relevante
        - Siempre sé empática, profesional y orientada a soluciones
        """
        
        return enhanced_prompt
    
    def _extract_name_with_advanced_ner(self, message: str) -> Optional[str]:
        """
        🧠 EXTRACCIÓN AVANZADA DE NOMBRES CON NER
        
        Usa spaCy NER para extraer nombres de CUALQUIER texto,
        no solo patrones específicos de presentación.
        """
        
        logger.info(f"🔍 Extrayendo nombre con NER avanzado: '{message}'")
        
        # 1. Intentar con NER de spaCy (más poderoso)
        if self.spacy_service:
            try:
                extracted_name = self.spacy_service.extract_best_name(message)
                if extracted_name:
                    logger.info(f"🎯 NER spaCy extrajo: '{extracted_name}'")
                    return extracted_name
                else:
                    logger.info("🔍 NER spaCy no encontró nombres, probando fallback...")
            except Exception as e:
                logger.warning(f"⚠️ Error en NER spaCy: {e}")
        
        # 2. Fallback: Patrones regex mejorados
        logger.info("🔧 Usando fallback regex...")
        
        patterns = [
            # "soy Carlos Rodriguez" -> captura "Carlos Rodriguez"
            r'\bsoy\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+\s+[A-Za-záéíóúÁÉÍÓÚñÑ]+)',
            r'\bsoy\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+)',
            
            # "me llamo Ana Martinez" -> captura "Ana Martinez"
            r'\bme\s+llamo\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+\s+[A-Za-záéíóúÁÉÍÓÚñÑ]+)',
            r'\bme\s+llamo\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+)',
            
            # "mi nombre es Pedro Silva" -> captura "Pedro Silva"
            r'\bmi\s+nombre\s+es\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+\s+[A-Za-záéíóúÁÉÍÓÚñÑ]+)',
            r'\bmi\s+nombre\s+es\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+)',
            
            # "llamo Carlos" o variantes
            r'\bllamo\s+([A-Za-záéíóúÁÉÍÓÚñÑ]+\s+[A-Za-záéíóúÁÉÍÓÚñÑ]+)',
            r'\bllamo\s+([A-Za-záéíóúÁÑ]+)',
            
            # Patrones al inicio de mensaje
            r'^([A-Za-záéíóúÁÉÍÓÚñÑ]+\s+[A-Za-záéíóúÁÉÍÓÚñÑ]+)\s*,',
            r'^([A-Za-záéíóúÁÉÍÓÚñÑ]+\s+[A-Za-záéíóúÁÉÍÓÚñÑ]+)$',
            
            # 🔥 NUEVO: NOMBRE SOLO - Como "Jairo", "Carlos", "Ana"
            r'^([A-Za-záéíóúÁÉÍÓÚñÑ]{2,20})$'
        ]
        
        for i, pattern in enumerate(patterns):
            logger.info(f"🔍 Probando patrón regex {i+1}: {pattern}")
            match = re.search(pattern, message.strip(), re.IGNORECASE)
            if match:
                potential_name = match.group(1).strip()
                logger.info(f"✅ COINCIDENCIA: '{potential_name}' en mensaje: '{message}'")
                
                if self._is_valid_name(potential_name):
                    final_name = potential_name.title()
                    logger.info(f"🎉 NOMBRE EXTRAÍDO (regex): '{final_name}'")
                    return final_name
                else:
                    logger.info(f"❌ Nombre inválido descartado: '{potential_name}'")
        
        # 3. Último intento: Preguntar al cliente sobre qué se refiere
        logger.info(f"❌ NO se extrajo nombre de: '{message}'")
        return None
    
    def _is_valid_name(self, name: str) -> bool:
        """Validación SÚPER PERMISIVA - Acepta prácticamente cualquier nombre"""
        
        # Validaciones MUY básicas
        if len(name) < 2 or len(name) > 50:
            logger.info(f"❌ Nombre demasiado corto/largo: '{name}' (len={len(name)})")
            return False
        
        # Solo letras y espacios (permitir acentos, ñ, etc.)
        if not re.match(r'^[A-Za-záéíóúÁÉÍÓÚñÑüÜ\s]+$', name):
            logger.info(f"❌ Nombre contiene caracteres inválidos: '{name}'")
            return False
        
        # Lista MÍNIMA de palabras que NO son nombres
        forbidden_words = {
            'auto', 'moto', 'soat', 'cotizar', 'quiero', 'precio', 
            'hola', 'si', 'no', 'ok', 'gracias', 'taxi', 'información',
            'seguro', 'lima', 'que', 'para', 'como', 'donde', 'cuando'
        }
        
        # SOLO verificar si es UNA palabra prohibida exacta
        name_lower = name.lower().strip()
        if name_lower in forbidden_words:
            logger.info(f"❌ Nombre es palabra prohibida: '{name}' -> '{name_lower}'")
            return False
        
        # ✅ ACEPTAR TODO LO DEMÁS
        logger.info(f"✅ Nombre VÁLIDO: '{name}'")
        return True
    
    def _apply_human_delay(self, delay_type: str) -> None:
        """Aplica delay humano realista"""
        if delay_type not in self.typing_delays:
            delay_type = 'medium'
        
        min_delay, max_delay = self.typing_delays[delay_type]
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def _calculate_delay_type(self, response: str) -> str:
        """Calcula el tipo de delay según la longitud de respuesta"""
        length = len(response)
        
        if length < 50:
            return 'short'
        elif length < 150:
            return 'medium'
        else:
            return 'long'
    
    def get_memory_summary(self, phone_number: str) -> Dict[str, Any]:
        """Obtiene resumen de memoria conversacional mejorado"""
        if phone_number not in self.conversation_memories:
            return {
                'interactions': 0, 
                'status': 'new_client',
                'client_name': None,
                'conversation_stage': 'greeting',
                'presentation_done': False,
                'quote_requested': False,
                'quote_generated': False
            }
        
        memory = self.conversation_memories[phone_number]
        return {
            'interactions': len(memory.short_term_context),
            'status': 'active_client',
            'client_name': memory.user_profile.get('nombre'),
            'conversation_stage': memory.conversation_stage,
            'presentation_done': memory.conversation_stage != "greeting",
            'name_requested': memory.conversation_stage == "name_captured",
            'quote_requested': memory.conversation_stage == "quote_requested",
            'quote_generated': memory.conversation_stage == "quote_generated",
            'vehicle_info': memory.user_profile.get('vehiculo_preferido'),
            'last_interaction': memory.updated_at.isoformat() if memory.updated_at else None,
            'conversation_summary': self.get_contextual_prompt_enhancement(phone_number, "Resumen de la conversación:")
        } 