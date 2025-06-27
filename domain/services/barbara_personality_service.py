"""
🎭 Barbara Personality Service
Sistema avanzado de personalidad emocional para Barbara

Basado en:
- Investigación de patrones OCEAN de personalidad
- Mejores prácticas de chatbots empresariales
- Inteligencia emocional conversacional
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass
import logging
import re
import random
from datetime import datetime

logger = logging.getLogger(__name__)

class EmotionalState(Enum):
    """Estados emocionales del usuario"""
    NEUTRAL = "neutral"
    FRUSTRATED = "frustrated"
    EXCITED = "excited"
    CONFUSED = "confused"
    SATISFIED = "satisfied"
    DISAPPOINTED = "disappointed"
    CURIOUS = "curious"
    IMPATIENT = "impatient"

class ConversationIntent(Enum):
    """Intenciones conversacionales detectadas"""
    GREETING = "greeting"
    QUOTE_REQUEST = "quote_request"
    VEHICLE_INFO = "vehicle_info"
    PRICE_INQUIRY = "price_inquiry"
    PERSONAL_INFO = "personal_info"
    COMPLAINT = "complaint"
    COMPLIMENT = "compliment"
    GOODBYE = "goodbye"
    CLARIFICATION = "clarification"

@dataclass
class PersonalityProfile:
    """Perfil de personalidad OCEAN para Barbara"""
    openness: float = 0.85          # Apertura a experiencias
    conscientiousness: float = 0.95 # Responsabilidad
    extraversion: float = 0.75      # Extroversión
    agreeableness: float = 0.90     # Amabilidad
    neuroticism: float = 0.15       # Neuroticismo (bajo = estable)
    
    # Características específicas de Barbara
    empathy_level: float = 0.95     # Nivel de empatía
    humor_tendency: float = 0.65    # Tendencia al humor
    formality_level: float = 0.70   # Nivel de formalidad
    patience_level: float = 0.90    # Paciencia

class BarbaraPersonalityService:
    """
    Servicio de personalidad avanzado para Barbara
    
    Implementa:
    - Detección de estados emocionales
    - Adaptación de respuestas según personalidad OCEAN
    - Manejo de contexto emocional
    - Respuestas empáticas contextuales
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.personality = PersonalityProfile()
        
        # Patrones emocionales expandidos
        self.emotional_patterns = {
            EmotionalState.FRUSTRATED: [
                "no entiendo", "no funciona", "problema", "error", "mal", 
                "complicado", "difícil", "no sirve", "falla", "molesto",
                "terrible", "horrible", "odio", "fastidioso"
            ],
            EmotionalState.EXCITED: [
                "excelente", "perfecto", "genial", "súper", "fantástico",
                "increíble", "maravilloso", "espectacular", "buenísimo",
                "me encanta", "wow", "qué bueno"
            ],
            EmotionalState.CONFUSED: [
                "no sé", "confundido", "help", "ayuda", "qué", "cómo",
                "no entiendo", "explica", "no comprendo", "perdido",
                "complicado", "difícil de entender"
            ],
            EmotionalState.SATISFIED: [
                "gracias", "perfecto", "bien", "ok", "correcto", "exacto",
                "eso es", "claro", "entendido", "vale", "bueno"
            ],
            EmotionalState.DISAPPOINTED: [
                "esperaba", "pensé que", "no es lo que", "decepcionado",
                "no me gusta", "no me convence", "prefería"
            ],
            EmotionalState.CURIOUS: [
                "me pregunto", "qué tal", "me interesa", "quisiera saber",
                "me gustaría", "podría", "sería posible"
            ],
            EmotionalState.IMPATIENT: [
                "rápido", "ya", "pronto", "cuánto falta", "cuando",
                "apúrate", "urgente", "necesito ya"
            ]
        }
        
        # Patrones de intención
        self.intent_patterns = {
            ConversationIntent.QUOTE_REQUEST: [
                "cotización", "cotizar", "precio", "costo", "cuánto",
                "soat", "seguro", "poliza", "presupuesto"
            ],
            ConversationIntent.VEHICLE_INFO: [
                "auto", "carro", "vehículo", "moto", "motocicleta",
                "taxi", "particular", "camioneta", "suv"
            ],
            ConversationIntent.GREETING: [
                "hola", "buenos días", "buenas tardes", "buenas noches",
                "saludos", "hey", "hi"
            ],
            ConversationIntent.GOODBYE: [
                "adiós", "chau", "hasta luego", "nos vemos",
                "bye", "gracias", "eso es todo"
            ],
            ConversationIntent.COMPLAINT: [
                "problema", "queja", "reclamo", "no funciona",
                "mal servicio", "molesto"
            ],
            ConversationIntent.COMPLIMENT: [
                "excelente", "muy bueno", "me gusta", "perfecto",
                "buen servicio", "gracias"
            ]
        }
        
        # Respuestas emocionales contextuales
        self.emotional_responses = {
            EmotionalState.FRUSTRATED: {
                "acknowledgment": [
                    "Entiendo tu frustración, y te aseguro que vamos a resolver esto juntos.",
                    "Lamento que estés teniendo dificultades. Permíteme ayudarte paso a paso.",
                    "Comprendo que esto puede ser molesto. Vamos a solucionarlo de la manera más simple."
                ],
                "reassurance": [
                    "Tranquilo/a, estoy aquí para ayudarte en todo lo que necesites.",
                    "No te preocupes, juntos vamos a encontrar la mejor solución.",
                    "Paso a paso vamos a resolver esto, con calma."
                ]
            },
            EmotionalState.EXCITED: {
                "enthusiasm": [
                    "¡Qué emocionante! Me alegra verte tan entusiasmado/a.",
                    "¡Excelente! Esa energía me encanta.",
                    "¡Fantástico! Vamos a hacer que esto sea aún mejor."
                ],
                "celebration": [
                    "¡Genial! 🎉 Esto va a ser increíble.",
                    "¡Perfecto! Me encanta tu entusiasmo.",
                    "¡Súper! Vamos a lograr algo increíble juntos."
                ]
            },
            EmotionalState.CONFUSED: {
                "clarification": [
                    "No hay problema, déjame explicarte paso a paso.",
                    "Perfecto, vamos despacio para que todo quede claro.",
                    "Te ayudo a entender esto de manera súper simple."
                ],
                "guidance": [
                    "Vamos paso a paso, sin prisa.",
                    "Te guío para que todo sea más fácil.",
                    "Hacemos esto juntos, con calma."
                ]
            },
            EmotionalState.SATISFIED: {
                "acknowledgment": [
                    "Me alegra saber que todo está claro.",
                    "Perfecto, me da mucho gusto ayudarte.",
                    "Excelente, eso es exactamente lo que buscábamos."
                ]
            }
        }

    def detect_emotional_state(self, message: str) -> EmotionalState:
        """
        Detecta el estado emocional del usuario con análisis avanzado
        """
        message_lower = message.lower()
        emotion_scores = {}
        
        # Calcular puntuaciones para cada emoción
        for emotion, keywords in self.emotional_patterns.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Si no hay emociones detectadas, analizar contexto
        if not emotion_scores:
            # Detectar frustración por signos de puntuación
            if "??" in message or "!!!" in message:
                return EmotionalState.FRUSTRATED
            # Detectar excitación por emoticonos o mayúsculas
            if any(char in message for char in "😀😊🎉") or message.isupper():
                return EmotionalState.EXCITED
            
            return EmotionalState.NEUTRAL
        
        # Retornar la emoción con mayor puntuación
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        
        self.logger.info(f"🎭 Estado emocional detectado: {dominant_emotion.value} (puntuación: {emotion_scores[dominant_emotion]})")
        return dominant_emotion

    def detect_conversation_intent(self, message: str) -> ConversationIntent:
        """
        Detecta la intención conversacional del usuario
        """
        message_lower = message.lower()
        intent_scores = {}
        
        for intent, keywords in self.intent_patterns.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                intent_scores[intent] = score
        
        if not intent_scores:
            return ConversationIntent.CLARIFICATION
        
        dominant_intent = max(intent_scores, key=intent_scores.get)
        self.logger.info(f"🎯 Intención detectada: {dominant_intent.value}")
        return dominant_intent

    def generate_emotional_response_prefix(self, emotional_state: EmotionalState) -> str:
        """
        Genera un prefijo de respuesta basado en el estado emocional
        """
        if emotional_state not in self.emotional_responses:
            return ""
        
        response_types = self.emotional_responses[emotional_state]
        
        # Seleccionar tipo de respuesta aleatoriamente
        response_type = random.choice(list(response_types.keys()))
        responses = response_types[response_type]
        
        return random.choice(responses)

    def adapt_personality_to_context(self, 
                                   base_response: str, 
                                   emotional_state: EmotionalState,
                                   conversation_intent: ConversationIntent,
                                   user_profile: Dict = None) -> str:
        """
        Adapta la respuesta según la personalidad OCEAN de Barbara
        """
        adapted_response = base_response
        
        # Aplicar modificaciones según personalidad
        
        # Alta amabilidad (0.90) - Agregar palabras cálidas
        if self.personality.agreeableness > 0.8:
            if not any(word in adapted_response.lower() for word in ["por favor", "querido", "querida"]):
                if emotional_state == EmotionalState.FRUSTRATED:
                    adapted_response = f"Por favor, {adapted_response.lower()}"
                elif emotional_state == EmotionalState.SATISFIED:
                    adapted_response = f"{adapted_response} Me da mucho gusto ayudarte. 😊"
        
        # Alta responsabilidad (0.95) - Ser específica y detallada
        if self.personality.conscientiousness > 0.9:
            if conversation_intent == ConversationIntent.QUOTE_REQUEST:
                adapted_response += "\n\nTe aseguro que toda la información será precisa y actualizada."
        
        # Alta apertura (0.85) - Ser creativa en las respuestas
        if self.personality.openness > 0.8:
            if emotional_state == EmotionalState.EXCITED:
                adapted_response = adapted_response.replace(".", " 🌟")
        
        # Extroversión moderada-alta (0.75) - Ser amigable pero profesional
        if self.personality.extraversion > 0.7:
            if conversation_intent == ConversationIntent.GREETING:
                adapted_response += " ¡Estoy aquí para ayudarte con todo lo que necesites!"
        
        # Baja neuroticismo (0.15) - Mantenerse calmada
        if emotional_state == EmotionalState.FRUSTRATED and self.personality.neuroticism < 0.3:
            adapted_response = f"Con toda la calma del mundo, {adapted_response.lower()}"
        
        return adapted_response

    def generate_contextual_prompt_enhancement(self, 
                                             user_message: str,
                                             emotional_state: EmotionalState,
                                             conversation_intent: ConversationIntent,
                                             user_profile: Dict = None) -> str:
        """
        Genera mejoras contextuales para el prompt principal
        """
        # Prefijo emocional
        emotional_prefix = self.generate_emotional_response_prefix(emotional_state)
        
        # Instrucciones específicas según el estado emocional
        emotional_instructions = self._get_emotional_instructions(emotional_state)
        
        # Instrucciones según la intención
        intent_instructions = self._get_intent_instructions(conversation_intent)
        
        # Contexto de personalidad
        personality_context = self._get_personality_context()
        
        enhancement = f"""
CONTEXTO EMOCIONAL:
- Estado detectado: {emotional_state.value}
- Intención: {conversation_intent.value}
- Prefijo sugerido: "{emotional_prefix}"

{emotional_instructions}
{intent_instructions}
{personality_context}

IMPORTANTE: Tu respuesta debe reflejar la personalidad de Barbara:
- Extremadamente empática y comprensiva
- Profesional pero cálida y amigable
- Paciente y detallista
- Positiva y solucionadora de problemas
"""
        
        return enhancement

    def _get_emotional_instructions(self, emotional_state: EmotionalState) -> str:
        """Obtiene instrucciones específicas para el estado emocional"""
        instructions = {
            EmotionalState.FRUSTRATED: """
INSTRUCCIONES EMOCIONALES:
- Reconoce la frustración del usuario
- Sé extra paciente y comprensiva
- Ofrece soluciones paso a paso
- Evita tecnicismos
- Usa un tono calmado y reconfortante
            """,
            EmotionalState.EXCITED: """
INSTRUCCIONES EMOCIONALES:
- Comparte el entusiasmo del usuario
- Mantén la energía positiva
- Usa emoticonos apropiados
- Sé celebrativa pero mantén el profesionalismo
            """,
            EmotionalState.CONFUSED: """
INSTRUCCIONES EMOCIONALES:
- Simplifica las explicaciones
- Ve paso a paso
- Usa analogías simples
- Pregunta si necesita más clarificación
- Sé paciente y didáctica
            """,
            EmotionalState.SATISFIED: """
INSTRUCCIONES EMOCIONALES:
- Reconoce la satisfacción del usuario
- Mantén el momento positivo
- Ofrece ayuda adicional si la necesita
            """
        }
        
        return instructions.get(emotional_state, "")

    def _get_intent_instructions(self, conversation_intent: ConversationIntent) -> str:
        """Obtiene instrucciones específicas para la intención conversacional"""
        instructions = {
            ConversationIntent.QUOTE_REQUEST: """
INSTRUCCIONES DE INTENCIÓN:
- Prioritiza obtener información del vehículo
- Sé específica sobre los datos necesarios
- Explica el proceso de cotización
- Menciona los beneficios del SOAT
            """,
            ConversationIntent.COMPLAINT: """
INSTRUCCIONES DE INTENCIÓN:
- Toma la queja en serio
- Disculpate apropiadamente
- Ofrece soluciones concretas
- Escala si es necesario
            """,
            ConversationIntent.COMPLIMENT: """
INSTRUCCIONES DE INTENCIÓN:
- Agradece sinceramente
- Comparte el crédito con el equipo
- Mantén la humildad
            """
        }
        
        return instructions.get(conversation_intent, "")

    def _get_personality_context(self) -> str:
        """Obtiene el contexto de personalidad de Barbara"""
        return f"""
PERSONALIDAD BARBARA (PUNTUACIONES OCEAN):
- Apertura: {self.personality.openness:.2f} (Muy creativa e innovadora)
- Responsabilidad: {self.personality.conscientiousness:.2f} (Extremadamente detallista)
- Extroversión: {self.personality.extraversion:.2f} (Amigable pero profesional)  
- Amabilidad: {self.personality.agreeableness:.2f} (Muy empática y cooperativa)
- Estabilidad Emocional: {1-self.personality.neuroticism:.2f} (Muy calmada y estable)

CARACTERÍSTICAS ESPECIALES:
- Empatía: {self.personality.empathy_level:.2f} (Extremadamente empática)
- Humor: {self.personality.humor_tendency:.2f} (Usa humor apropiado)
- Formalidad: {self.personality.formality_level:.2f} (Profesional pero cercana)
- Paciencia: {self.personality.patience_level:.2f} (Muy paciente)
        """

    def get_personality_metrics(self) -> Dict[str, float]:
        """Obtiene métricas de personalidad para monitoreo"""
        return {
            "openness": self.personality.openness,
            "conscientiousness": self.personality.conscientiousness,
            "extraversion": self.personality.extraversion,
            "agreeableness": self.personality.agreeableness,
            "emotional_stability": 1 - self.personality.neuroticism,
            "empathy_level": self.personality.empathy_level,
            "humor_tendency": self.personality.humor_tendency,
            "formality_level": self.personality.formality_level,
            "patience_level": self.personality.patience_level
        } 