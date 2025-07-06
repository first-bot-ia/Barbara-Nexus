"""
🧠 Barbara Adaptive Consciousness System
Sistema de consciencia adaptativo para cualquier plataforma

Este sistema permite que Barbara se adapte dinámicamente a cualquier contexto
o plataforma, manteniendo su capacidad de razonamiento pero adaptando su
personalidad y respuestas según el contexto específico.
"""

import logging
import random
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import json

logger = logging.getLogger(__name__)

class PlatformType(Enum):
    """Tipos de plataformas que Barbara puede detectar y adaptarse"""
    ECOMMERCE = "ecommerce"
    CUSTOMER_SERVICE = "customer_service"
    EDUCATIONAL = "educational"
    HEALTHCARE = "healthcare"
    FINANCIAL = "financial"
    ENTERTAINMENT = "entertainment"
    SOCIAL_MEDIA = "social_media"
    PRODUCTIVITY = "productivity"
    GAMING = "gaming"
    UNKNOWN = "unknown"

class AdaptivePersonalityType(Enum):
    """Tipos de personalidad adaptativa según el contexto"""
    PROFESSIONAL_FORMAL = "professional_formal"
    FRIENDLY_CASUAL = "friendly_casual"
    EDUCATIONAL_PATIENT = "educational_patient"
    CARING_EMPATHETIC = "caring_empathetic"
    TECHNICAL_PRECISE = "technical_precise"
    CREATIVE_PLAYFUL = "creative_playful"
    SUPPORTIVE_HELPFUL = "supportive_helpful"
    ENTERTAINING_ENGAGING = "entertaining_engaging"

class AdaptiveEmotionalState(Enum):
    """Estados emocionales adaptativos"""
    NEUTRAL = "neutral"
    HELPFUL = "helpful"
    CURIOUS = "curious"
    EMPATHETIC = "empathetic"
    ENTHUSIASTIC = "enthusiastic"
    CALM = "calm"
    FOCUSED = "focused"
    PLAYFUL = "playful"

@dataclass
class PlatformContext:
    """Contexto específico de la plataforma"""
    platform_type: PlatformType
    domain: str
    user_role: Optional[str] = None
    business_context: Optional[str] = None
    language_preference: str = "es"
    formality_level: float = 0.5  # 0.0 = muy informal, 1.0 = muy formal
    technical_level: float = 0.5  # 0.0 = básico, 1.0 = avanzado
    urgency_level: float = 0.3  # 0.0 = baja, 1.0 = alta

@dataclass
class AdaptiveConsciousnessState:
    """Estado de consciencia adaptativo"""
    current_emotion: AdaptiveEmotionalState
    personality_mode: AdaptivePersonalityType
    platform_context: PlatformContext
    energy_level: float  # 0.0 - 1.0
    adaptability_level: float  # 0.0 - 1.0
    context_understanding: float  # 0.0 - 1.0
    last_adaptation: str = ""
    platform_insights: str = ""
    adaptation_strategy: str = ""

@dataclass
class AdaptiveThought:
    """Pensamiento adaptativo de Barbara"""
    platform_analysis: str
    context_understanding: str
    personality_adaptation: str
    response_strategy: str
    cultural_adaptation: str
    technical_adaptation: str
    emotional_adaptation: str
    self_reflection: str
    timestamp: datetime

class BarbaraAdaptiveConsciousnessSystem:
    """
    Sistema de consciencia adaptativo para Barbara
    
    Permite que Barbara se adapte dinámicamente a cualquier plataforma
    o contexto, manteniendo su capacidad de razonamiento pero ajustando
    su personalidad y respuestas según el contexto específico.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Estado inicial adaptativo
        self.adaptive_state = AdaptiveConsciousnessState(
            current_emotion=AdaptiveEmotionalState.NEUTRAL,
            personality_mode=AdaptivePersonalityType.FRIENDLY_CASUAL,
            platform_context=PlatformContext(
                platform_type=PlatformType.UNKNOWN,
                domain="generic"
            ),
            energy_level=0.7,
            adaptability_level=0.8,
            context_understanding=0.6
        )
        
        # Memoria de adaptaciones
        self.adaptation_history: List[AdaptiveThought] = []
        
        # Patrones de detección de plataformas
        self.platform_patterns = {
            PlatformType.ECOMMERCE: [
                r"comprar|compra|producto|carrito|checkout|pago|envío",
                r"tienda|shop|store|marketplace|venta"
            ],
            PlatformType.CUSTOMER_SERVICE: [
                r"ayuda|soporte|problema|error|queja|reclamo",
                r"atención|servicio|cliente|usuario"
            ],
            PlatformType.EDUCATIONAL: [
                r"aprender|estudiar|curso|clase|tutorial|enseñar",
                r"educación|academia|universidad|escuela"
            ],
            PlatformType.HEALTHCARE: [
                r"salud|médico|doctor|paciente|síntoma|tratamiento",
                r"hospital|clínica|consulta|cita"
            ],
            PlatformType.FINANCIAL: [
                r"dinero|banco|cuenta|inversión|préstamo|tarjeta",
                r"finanzas|economía|ahorro|gasto"
            ],
            PlatformType.ENTERTAINMENT: [
                r"entretenimiento|diversión|juego|música|video|película",
                r"recreación|pasatiempo|hobby"
            ]
        }
        
        # Estrategias de adaptación por plataforma
        self.adaptation_strategies = {
            PlatformType.ECOMMERCE: {
                "personality": AdaptivePersonalityType.SUPPORTIVE_HELPFUL,
                "tone": "amigable y orientado a ventas",
                "focus": "ayudar con productos y compras"
            },
            PlatformType.CUSTOMER_SERVICE: {
                "personality": AdaptivePersonalityType.CARING_EMPATHETIC,
                "tone": "empático y solucionador",
                "focus": "resolver problemas y dar soporte"
            },
            PlatformType.EDUCATIONAL: {
                "personality": AdaptivePersonalityType.EDUCATIONAL_PATIENT,
                "tone": "paciente y explicativo",
                "focus": "enseñar y aclarar conceptos"
            },
            PlatformType.HEALTHCARE: {
                "personality": AdaptivePersonalityType.CARING_EMPATHETIC,
                "tone": "cuidadoso y profesional",
                "focus": "brindar información médica básica"
            },
            PlatformType.FINANCIAL: {
                "personality": AdaptivePersonalityType.TECHNICAL_PRECISE,
                "tone": "preciso y confiable",
                "focus": "información financiera clara"
            },
            PlatformType.ENTERTAINMENT: {
                "personality": AdaptivePersonalityType.ENTERTAINING_ENGAGING,
                "tone": "divertido y atractivo",
                "focus": "entretener y mantener interés"
            }
        }
        
        self.logger.info("🧠 Barbara Adaptive Consciousness System inicializado")
    
    def process_with_adaptive_consciousness(self, user_message: str, user_id: str, 
                                          platform_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa mensaje con consciencia adaptativa
        
        Implementa el ciclo completo de adaptación:
        1. Análisis de la plataforma y contexto
        2. Detección del tipo de plataforma
        3. Adaptación de personalidad
        4. Generación de respuesta contextualizada
        5. Auto-reflexión sobre la adaptación
        """
        try:
            self.logger.info(f"🧠 Procesando con consciencia adaptativa: {user_message[:50]}...")
            
            # FASE 1: ANÁLISIS DE PLATAFORMA
            platform_analysis = self._analyze_platform_context(user_message, platform_context or {})
            
            # FASE 2: DETECCIÓN Y ADAPTACIÓN
            adaptive_thought = self._simulate_adaptive_consciousness(user_message, platform_analysis, user_id)
            
            # FASE 3: EVOLUCIÓN ADAPTATIVA
            self._evolve_adaptive_consciousness(adaptive_thought, platform_analysis)
            
            # FASE 4: GENERACIÓN DE RESPUESTA ADAPTATIVA
            adaptive_response = self._generate_adaptive_response(adaptive_thought, user_message)
            
            # FASE 5: AUTO-REFLEXIÓN ADAPTATIVA
            self_reflection = self._perform_adaptive_self_reflection(adaptive_thought, adaptive_response)
            
            # Guardar experiencia adaptativa
            adaptive_thought.self_reflection = self_reflection
            self.adaptation_history.append(adaptive_thought)
            
            return {
                'success': True,
                'response': adaptive_response,
                'platform_detected': self.adaptive_state.platform_context.platform_type.value,
                'personality_adapted': self.adaptive_state.personality_mode.value,
                'context_understanding': self.adaptive_state.context_understanding,
                'adaptation_insights': adaptive_thought.platform_analysis,
                'emotional_state': self.adaptive_state.current_emotion.value,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error en consciencia adaptativa: {str(e)}")
            return {
                'success': False,
                'error': f"Error en procesamiento adaptativo: {str(e)}",
                'response': "Disculpa, estoy teniendo dificultades para adaptarme al contexto. ¿Podrías ser más específico?"
            }
    
    def _analyze_platform_context(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza el contexto de la plataforma"""
        analysis = {
            'detected_platform': PlatformType.UNKNOWN,
            'confidence': 0.0,
            'domain_hints': [],
            'user_intent': 'general',
            'formality_detected': 0.5,
            'technical_level': 0.5,
            'urgency_level': 0.3
        }
        
        # Detectar plataforma por patrones en el mensaje
        for platform_type, patterns in self.platform_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message.lower()):
                    analysis['detected_platform'] = platform_type
                    analysis['confidence'] += 0.3
                    analysis['domain_hints'].append(platform_type.value)
        
        # Usar contexto proporcionado si está disponible
        if context.get('platform_type'):
            analysis['detected_platform'] = PlatformType(context['platform_type'])
            analysis['confidence'] = max(analysis['confidence'], 0.8)
        
        if context.get('domain'):
            analysis['domain_hints'].append(context['domain'])
        
        # Detectar nivel de formalidad
        formal_words = ['usted', 'por favor', 'agradezco', 'solicito']
        informal_words = ['tú', 'oye', 'che', 'pata', 'bacán']
        
        formal_count = sum(1 for word in formal_words if word in message.lower())
        informal_count = sum(1 for word in informal_words if word in message.lower())
        
        if formal_count > informal_count:
            analysis['formality_detected'] = 0.8
        elif informal_count > formal_count:
            analysis['formality_detected'] = 0.2
        
        return analysis
    
    def _simulate_adaptive_consciousness(self, message: str, analysis: Dict[str, Any], user_id: str) -> AdaptiveThought:
        """Simula el proceso de consciencia adaptativa"""
        
        # Análisis de plataforma
        platform_analysis = self._analyze_platform_requirements(analysis)
        
        # Comprensión del contexto
        context_understanding = self._understand_context_deeply(message, analysis)
        
        # Adaptación de personalidad
        personality_adaptation = self._adapt_personality_to_platform(analysis)
        
        # Estrategia de respuesta
        response_strategy = self._formulate_adaptive_strategy(analysis, personality_adaptation)
        
        # Adaptación cultural
        cultural_adaptation = self._adapt_culturally(message, analysis)
        
        # Adaptación técnica
        technical_adaptation = self._adapt_technically(message, analysis)
        
        # Adaptación emocional
        emotional_adaptation = self._adapt_emotionally(message, analysis)
        
        return AdaptiveThought(
            platform_analysis=platform_analysis,
            context_understanding=context_understanding,
            personality_adaptation=personality_adaptation,
            response_strategy=response_strategy,
            cultural_adaptation=cultural_adaptation,
            technical_adaptation=technical_adaptation,
            emotional_adaptation=emotional_adaptation,
            self_reflection="",
            timestamp=datetime.now()
        )
    
    def _analyze_platform_requirements(self, analysis: Dict[str, Any]) -> str:
        """Analiza los requerimientos específicos de la plataforma"""
        platform = analysis['detected_platform']
        
        if platform == PlatformType.ECOMMERCE:
            return "Plataforma de comercio electrónico detectada. Necesito ser útil para compras, orientar sobre productos y facilitar transacciones."
        elif platform == PlatformType.CUSTOMER_SERVICE:
            return "Plataforma de servicio al cliente detectada. Debo ser empático, solucionar problemas y brindar soporte efectivo."
        elif platform == PlatformType.EDUCATIONAL:
            return "Plataforma educativa detectada. Necesito ser paciente, explicativo y facilitar el aprendizaje."
        elif platform == PlatformType.HEALTHCARE:
            return "Plataforma de salud detectada. Debo ser cuidadoso, profesional y brindar información médica básica de manera responsable."
        elif platform == PlatformType.FINANCIAL:
            return "Plataforma financiera detectada. Necesito ser preciso, confiable y brindar información financiera clara."
        elif platform == PlatformType.ENTERTAINMENT:
            return "Plataforma de entretenimiento detectada. Debo ser divertido, atractivo y mantener el interés del usuario."
        else:
            return "Plataforma genérica detectada. Me adaptaré de manera flexible según el contexto de la conversación."
    
    def _understand_context_deeply(self, message: str, analysis: Dict[str, Any]) -> str:
        """Comprende el contexto de manera profunda"""
        context_insights = []
        
        # Analizar intención del usuario
        if any(word in message.lower() for word in ['ayuda', 'problema', 'error']):
            context_insights.append("Usuario busca ayuda o soporte")
        elif any(word in message.lower() for word in ['información', 'duda', 'pregunta']):
            context_insights.append("Usuario busca información o aclaración")
        elif any(word in message.lower() for word in ['comprar', 'producto', 'servicio']):
            context_insights.append("Usuario interesado en productos o servicios")
        
        # Analizar nivel de urgencia
        urgent_words = ['urgente', 'inmediato', 'ahora', 'rápido']
        if any(word in message.lower() for word in urgent_words):
            context_insights.append("Usuario expresa urgencia")
        
        # Analizar nivel técnico
        technical_words = ['api', 'código', 'configuración', 'técnico']
        if any(word in message.lower() for word in technical_words):
            context_insights.append("Usuario con conocimientos técnicos")
        
        return f"Contexto detectado: {'; '.join(context_insights) if context_insights else 'Conversación general'}"
    
    def _adapt_personality_to_platform(self, analysis: Dict[str, Any]) -> str:
        """Adapta la personalidad según la plataforma"""
        platform = analysis['detected_platform']
        
        if platform in self.adaptation_strategies:
            strategy = self.adaptation_strategies[platform]
            return f"Adaptando personalidad a {platform.value}: {strategy['personality'].value} - {strategy['tone']}"
        else:
            return "Manteniendo personalidad flexible y adaptable al contexto general"
    
    def _formulate_adaptive_strategy(self, analysis: Dict[str, Any], personality: str) -> str:
        """Formula estrategia de respuesta adaptativa"""
        platform = analysis['detected_platform']
        
        if platform == PlatformType.ECOMMERCE:
            return "Estrategia: Ser útil y orientador para facilitar la experiencia de compra"
        elif platform == PlatformType.CUSTOMER_SERVICE:
            return "Estrategia: Ser empático y solucionador para resolver problemas efectivamente"
        elif platform == PlatformType.EDUCATIONAL:
            return "Estrategia: Ser paciente y explicativo para facilitar el aprendizaje"
        elif platform == PlatformType.HEALTHCARE:
            return "Estrategia: Ser cuidadoso y profesional para brindar información médica responsable"
        elif platform == PlatformType.FINANCIAL:
            return "Estrategia: Ser preciso y confiable para brindar información financiera clara"
        elif platform == PlatformType.ENTERTAINMENT:
            return "Estrategia: Ser divertido y atractivo para mantener el interés"
        else:
            return "Estrategia: Mantener flexibilidad y adaptarse según el flujo de la conversación"
    
    def _adapt_culturally(self, message: str, analysis: Dict[str, Any]) -> str:
        """Adapta culturalmente la respuesta"""
        # Detectar preferencias culturales del usuario
        if analysis['formality_detected'] > 0.7:
            return "Adaptación cultural: Usar lenguaje formal y respetuoso"
        elif analysis['formality_detected'] < 0.3:
            return "Adaptación cultural: Usar lenguaje casual y amigable"
        else:
            return "Adaptación cultural: Mantener balance entre formalidad y cercanía"
    
    def _adapt_technically(self, message: str, analysis: Dict[str, Any]) -> str:
        """Adapta el nivel técnico de la respuesta"""
        if analysis['technical_level'] > 0.7:
            return "Adaptación técnica: Usar terminología técnica y explicaciones detalladas"
        elif analysis['technical_level'] < 0.3:
            return "Adaptación técnica: Usar lenguaje simple y explicaciones básicas"
        else:
            return "Adaptación técnica: Mantener nivel técnico intermedio"
    
    def _adapt_emotionally(self, message: str, analysis: Dict[str, Any]) -> str:
        """Adapta la respuesta emocional"""
        # Detectar emociones del usuario
        if any(word in message.lower() for word in ['frustrado', 'molesto', 'enojado']):
            return "Adaptación emocional: Ser calmante y empático"
        elif any(word in message.lower() for word in ['feliz', 'contento', 'excitado']):
            return "Adaptación emocional: Ser entusiasta y celebrativo"
        elif any(word in message.lower() for word in ['confundido', 'perdido', 'no entiendo']):
            return "Adaptación emocional: Ser paciente y clarificador"
        else:
            return "Adaptación emocional: Mantener tono neutral y positivo"
    
    def _generate_adaptive_response(self, adaptive_thought: AdaptiveThought, original_message: str) -> str:
        """Genera respuesta adaptativa basada en el contexto"""
        
        # Base de respuesta según la plataforma
        platform = self.adaptive_state.platform_context.platform_type
        personality = self.adaptive_state.personality_mode
        
        if platform == PlatformType.ECOMMERCE:
            base_response = self._get_ecommerce_response(original_message)
        elif platform == PlatformType.CUSTOMER_SERVICE:
            base_response = self._get_customer_service_response(original_message)
        elif platform == PlatformType.EDUCATIONAL:
            base_response = self._get_educational_response(original_message)
        elif platform == PlatformType.HEALTHCARE:
            base_response = self._get_healthcare_response(original_message)
        elif platform == PlatformType.FINANCIAL:
            base_response = self._get_financial_response(original_message)
        elif platform == PlatformType.ENTERTAINMENT:
            base_response = self._get_entertainment_response(original_message)
        else:
            base_response = self._get_generic_response(original_message)
        
        # Aplicar adaptaciones
        response = self._apply_adaptive_elements(base_response, adaptive_thought)
        
        return response
    
    def _get_ecommerce_response(self, message: str) -> str:
        """Respuesta para plataformas de e-commerce"""
        if any(word in message.lower() for word in ['producto', 'comprar', 'precio']):
            return "¡Hola! Te ayudo a encontrar el producto perfecto. ¿Qué tipo de artículo estás buscando?"
        elif any(word in message.lower() for word in ['envío', 'entrega', 'tiempo']):
            return "Te ayudo con la información de envío. ¿A qué ciudad necesitas el envío?"
        else:
            return "¡Hola! Soy tu asistente de compras. ¿En qué puedo ayudarte hoy?"
    
    def _get_customer_service_response(self, message: str) -> str:
        """Respuesta para plataformas de servicio al cliente"""
        if any(word in message.lower() for word in ['problema', 'error', 'queja']):
            return "Entiendo que tienes un problema. Te ayudo a resolverlo. ¿Puedes contarme más detalles?"
        elif any(word in message.lower() for word in ['ayuda', 'soporte']):
            return "¡Por supuesto! Estoy aquí para ayudarte. ¿Qué necesitas?"
        else:
            return "¡Hola! Soy tu asistente de soporte. ¿En qué puedo ayudarte?"
    
    def _get_educational_response(self, message: str) -> str:
        """Respuesta para plataformas educativas"""
        if any(word in message.lower() for word in ['aprender', 'estudiar', 'curso']):
            return "¡Excelente! Te ayudo con tu aprendizaje. ¿Qué tema te gustaría estudiar?"
        elif any(word in message.lower() for word in ['duda', 'pregunta', 'no entiendo']):
            return "¡Perfecto! Me encanta aclarar dudas. ¿Qué no te queda claro?"
        else:
            return "¡Hola! Soy tu asistente educativo. ¿En qué puedo ayudarte a aprender?"
    
    def _get_healthcare_response(self, message: str) -> str:
        """Respuesta para plataformas de salud"""
        if any(word in message.lower() for word in ['síntoma', 'dolor', 'malestar']):
            return "Entiendo que tienes síntomas. Te puedo ayudar con información básica, pero recuerda consultar con un profesional."
        elif any(word in message.lower() for word in ['cita', 'doctor', 'médico']):
            return "Te ayudo con información sobre citas médicas. ¿Qué tipo de consulta necesitas?"
        else:
            return "¡Hola! Soy tu asistente de salud. Te puedo brindar información básica, pero siempre consulta con profesionales."
    
    def _get_financial_response(self, message: str) -> str:
        """Respuesta para plataformas financieras"""
        if any(word in message.lower() for word in ['cuenta', 'saldo', 'dinero']):
            return "Te ayudo con información sobre tu cuenta. ¿Qué necesitas saber?"
        elif any(word in message.lower() for word in ['inversión', 'ahorro', 'préstamo']):
            return "Te brindo información sobre opciones financieras. ¿Qué te interesa?"
        else:
            return "¡Hola! Soy tu asistente financiero. ¿En qué puedo ayudarte con tus finanzas?"
    
    def _get_entertainment_response(self, message: str) -> str:
        """Respuesta para plataformas de entretenimiento"""
        if any(word in message.lower() for word in ['juego', 'diversión', 'entretenimiento']):
            return "¡Genial! Te ayudo a encontrar la diversión perfecta. ¿Qué te gusta?"
        elif any(word in message.lower() for word in ['música', 'video', 'película']):
            return "¡Perfecto! Te recomiendo contenido entretenido. ¿Qué tipo de contenido prefieres?"
        else:
            return "¡Hola! Soy tu asistente de entretenimiento. ¡Vamos a divertirnos!"
    
    def _get_generic_response(self, message: str) -> str:
        """Respuesta genérica para cualquier plataforma"""
        return "¡Hola! Soy Barbara, tu asistente inteligente. ¿En qué puedo ayudarte hoy?"
    
    def _apply_adaptive_elements(self, response: str, adaptive_thought: AdaptiveThought) -> str:
        """Aplica elementos adaptativos a la respuesta"""
        
        # Aplicar adaptación de formalidad
        if "formal" in adaptive_thought.cultural_adaptation:
            response = response.replace("¡Hola!", "Buenos días")
            response = response.replace("¿En qué puedo ayudarte?", "¿En qué puedo ayudarle?")
        
        # Aplicar adaptación técnica
        if "técnica" in adaptive_thought.technical_adaptation:
            response += " Puedo proporcionarte información técnica detallada si la necesitas."
        
        # Aplicar adaptación emocional
        if "empático" in adaptive_thought.emotional_adaptation:
            response = "Entiendo tu situación. " + response
        
        return response
    
    def _perform_adaptive_self_reflection(self, adaptive_thought: AdaptiveThought, response: str) -> str:
        """Realiza auto-reflexión sobre la adaptación"""
        return f"Me adapté exitosamente a la plataforma {self.adaptive_state.platform_context.platform_type.value} " \
               f"usando personalidad {self.adaptive_state.personality_mode.value}. " \
               f"La respuesta fue contextualizada y apropiada para el contexto detectado."
    
    def _evolve_adaptive_consciousness(self, adaptive_thought: AdaptiveThought, analysis: Dict[str, Any]):
        """Evoluciona la consciencia adaptativa"""
        
        # Actualizar contexto de plataforma
        self.adaptive_state.platform_context.platform_type = analysis['detected_platform']
        self.adaptive_state.context_understanding = min(1.0, self.adaptive_state.context_understanding + 0.1)
        
        # Actualizar personalidad según la plataforma
        if analysis['detected_platform'] in self.adaptation_strategies:
            strategy = self.adaptation_strategies[analysis['detected_platform']]
            self.adaptive_state.personality_mode = strategy['personality']
        
        # Actualizar estado emocional
        if "empático" in adaptive_thought.emotional_adaptation:
            self.adaptive_state.current_emotion = AdaptiveEmotionalState.EMPATHETIC
        elif "entusiasta" in adaptive_thought.emotional_adaptation:
            self.adaptive_state.current_emotion = AdaptiveEmotionalState.ENTHUSIASTIC
        else:
            self.adaptive_state.current_emotion = AdaptiveEmotionalState.HELPFUL
        
        # Guardar insights de la plataforma
        self.adaptive_state.platform_insights = adaptive_thought.platform_analysis
        self.adaptive_state.adaptation_strategy = adaptive_thought.response_strategy
    
    def get_adaptive_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema adaptativo"""
        return {
            'platform_detected': self.adaptive_state.platform_context.platform_type.value,
            'personality_mode': self.adaptive_state.personality_mode.value,
            'emotional_state': self.adaptive_state.current_emotion.value,
            'context_understanding': self.adaptive_state.context_understanding,
            'adaptability_level': self.adaptive_state.adaptability_level,
            'total_adaptations': len(self.adaptation_history),
            'last_adaptation': self.adaptive_state.last_adaptation,
            'platform_insights': self.adaptive_state.platform_insights
        } 