"""
🧠 BARBARA LEARNING ENGINE - SISTEMA DE APRENDIZAJE AVANZADO
=========================================================

Motor de aprendizaje que permite a Barbara desarrollar:
- Libre albedrío en las respuestas
- Adaptación al lenguaje coloquial
- Memoria contextual avanzada
- Prevención de escenarios problemáticos
- Creatividad y originalidad
"""

import json
import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class PersonalityMode(Enum):
    """Modos de personalidad que Barbara puede adoptar"""
    FORMAL = "formal"
    COLOQUIAL = "coloquial"
    CREATIVO = "creativo"
    EMPATICO = "empatico"
    TECNICO = "tecnico"
    DIVERTIDO = "divertido"
    SABIO = "sabio"

class LearningContext(Enum):
    """Contextos de aprendizaje"""
    CONVERSATION = "conversation"
    PROBLEM_SOLVING = "problem_solving"
    CREATIVE_TASK = "creative_task"
    EMOTIONAL_SUPPORT = "emotional_support"
    TECHNICAL_QUERY = "technical_query"

@dataclass
class ConversationPattern:
    """Patrón de conversación aprendido"""
    pattern: str
    response_style: str
    context: LearningContext
    effectiveness: float
    usage_count: int
    last_used: datetime
    variations: List[str]

@dataclass
class MemoryFragment:
    """Fragmento de memoria contextual"""
    user_id: str
    content: str
    emotion: str
    importance: float
    timestamp: datetime
    connections: List[str]
    decay_rate: float

class BarbaraLearningEngine:
    """
    Motor de aprendizaje avanzado para Barbara
    Implementa capacidades de adaptación, creatividad y libre albedrío
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Configuración del motor
        self.creativity_level = 0.7  # Nivel de creatividad (0-1)
        self.free_will_factor = 0.8  # Factor de libre albedrío (0-1)
        self.learning_rate = 0.1     # Tasa de aprendizaje
        
        # Memoria y patrones
        self.conversation_patterns: Dict[str, ConversationPattern] = {}
        self.memory_fragments: Dict[str, List[MemoryFragment]] = {}
        self.personality_traits: Dict[str, float] = {
            'humor': 0.6,
            'empathy': 0.8,
            'creativity': 0.7,
            'formality': 0.4,
            'technical_depth': 0.5,
            'colloquial_adaptation': 0.3
        }
        
        # Vocabulario coloquial peruano
        self.coloquial_vocabulary = {
            'friend': ['pata', 'brother', 'compadre', 'causa', 'hermano', 'bro'],
            'car': ['carrito', 'nave', 'fierro', 'auto', 'carro'],
            'money': ['plata', 'mosca', 'lucas', 'efectivo', 'billete'],
            'good': ['chevere', 'bacán', 'joya', 'genial', 'perfecto'],
            'problem': ['bronca', 'problema', 'rollo', 'tema', 'asunto'],
            'fast': ['rapidito', 'al toque', 'ya mismo', 'volando', 'de una']
        }
        
        # Expresiones creativas
        self.creative_expressions = [
            "¡Esa es una pregunta que me hace brillar los circuitos! 🌟",
            "Mi IA está procesando eso con mucho cariño 💝",
            "¡Voy a sacar mi varita mágica digital para ayudarte! ✨",
            "Déjame consultar con mi sabiduría artificial 🧙‍♀️",
            "¡Eso suena como una aventura de seguros! 🚀"
        ]
        
        # Cargar conocimiento previo
        self._load_previous_learning()
        
        self.logger.info("🧠 Barbara Learning Engine inicializado")
    
    def process_with_learning(self, user_message: str, user_id: str, 
                            current_context: str = "conversation") -> Dict[str, Any]:
        """
        Procesa un mensaje con aprendizaje avanzado
        
        Returns:
            Dict con análisis completo del mensaje y estrategia de respuesta
        """
        try:
            # Análisis del mensaje
            message_analysis = self._analyze_message(user_message)
            
            # Detección de personalidad requerida
            required_personality = self._detect_personality_mode(user_message, message_analysis)
            
            # Adaptación del vocabulario
            vocab_adaptations = self._adapt_vocabulary(user_message)
            
            # Generación de respuesta con libre albedrío
            response_strategy = self._generate_response_strategy(
                user_message, message_analysis, required_personality, user_id
            )
            
            # Actualización de memoria
            self._update_memory(user_id, user_message, message_analysis)
            
            # Aprender del patrón
            self._learn_from_interaction(user_message, message_analysis, current_context)
            
            return {
                'message_analysis': message_analysis,
                'personality_mode': required_personality,
                'vocab_adaptations': vocab_adaptations,
                'response_strategy': response_strategy,
                'free_will_factor': self._calculate_free_will_factor(user_message),
                'creativity_boost': self._calculate_creativity_boost(message_analysis),
                'memory_context': self._get_relevant_memory(user_id, user_message)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error en proceso de aprendizaje: {e}")
            return self._get_fallback_strategy()
    
    def _analyze_message(self, message: str) -> Dict[str, Any]:
        """Análisis profundo del mensaje"""
        analysis = {
            'length': len(message),
            'words': len(message.split()),
            'emotion': self._detect_emotion(message),
            'urgency': self._detect_urgency(message),
            'formality': self._detect_formality(message),
            'creativity_request': self._detect_creativity_request(message),
            'coloquial_level': self._detect_coloquial_level(message),
            'context_clues': self._extract_context_clues(message),
            'intent_complexity': self._measure_intent_complexity(message)
        }
        
        return analysis
    
    def _detect_emotion(self, message: str) -> str:
        """Detecta la emoción del mensaje"""
        message_lower = message.lower()
        
        # Patrones emocionales
        emotions = {
            'excited': ['!!!', 'genial', 'increíble', 'fantástico', 'chevere', 'bacán'],
            'frustrated': ['no funciona', 'problema', 'error', 'mal', 'terrible'],
            'urgent': ['urgente', 'ya', 'rápido', 'ahora mismo', 'inmediatamente'],
            'happy': ['😊', '😄', 'feliz', 'contento', 'alegre'],
            'confused': ['no entiendo', 'confuso', 'perdido', '???', 'explicar'],
            'casual': ['pata', 'brother', 'compadre', 'causa', 'hola']
        }
        
        for emotion, patterns in emotions.items():
            if any(pattern in message_lower for pattern in patterns):
                return emotion
        
        return 'neutral'
    
    def _detect_urgency(self, message: str) -> float:
        """Detecta nivel de urgencia (0-1)"""
        urgency_indicators = [
            ('!!!', 0.9), ('ahora mismo', 0.8), ('urgente', 0.8),
            ('rápido', 0.6), ('ya', 0.5), ('inmediatamente', 0.9),
            ('necesito', 0.4), ('pronto', 0.5)
        ]
        
        urgency_score = 0.0
        message_lower = message.lower()
        
        for indicator, score in urgency_indicators:
            if indicator in message_lower:
                urgency_score = max(urgency_score, score)
        
        # Bonus por múltiples signos de exclamación
        exclamation_count = message.count('!')
        if exclamation_count > 1:
            urgency_score = min(1.0, urgency_score + exclamation_count * 0.1)
        
        return urgency_score
    
    def _detect_formality(self, message: str) -> float:
        """Detecta nivel de formalidad (0-1)"""
        formal_indicators = [
            'estimado', 'señor', 'señora', 'usted', 'cordialmente',
            'agradecería', 'solicito', 'requiero'
        ]
        
        informal_indicators = [
            'hola', 'pata', 'brother', 'compadre', 'causa', 'che',
            'oye', 'mira', 'tú', 'tu'
        ]
        
        message_lower = message.lower()
        formal_count = sum(1 for indicator in formal_indicators if indicator in message_lower)
        informal_count = sum(1 for indicator in informal_indicators if indicator in message_lower)
        
        if formal_count + informal_count == 0:
            return 0.5  # Neutral
        
        return formal_count / (formal_count + informal_count)
    
    def _detect_creativity_request(self, message: str) -> bool:
        """Detecta si el usuario pide creatividad"""
        creative_requests = [
            'imagínate', 'inventa', 'crea', 'creativo', 'original',
            'divertido', 'historia', 'cuéntame', 'como si fueras',
            'superhéroe', 'robot', 'futuro'
        ]
        
        message_lower = message.lower()
        return any(request in message_lower for request in creative_requests)
    
    def _detect_coloquial_level(self, message: str) -> float:
        """Detecta nivel de uso coloquial (0-1)"""
        coloquial_terms = [
            'pata', 'brother', 'compadre', 'causa', 'hermano',
            'chevere', 'bacán', 'joya', 'carrito', 'nave',
            'plata', 'mosca', 'al toque', 'de una', 'rapidito'
        ]
        
        message_lower = message.lower()
        coloquial_count = sum(1 for term in coloquial_terms if term in message_lower)
        total_words = len(message.split())
        
        if total_words == 0:
            return 0.0
        
        return min(1.0, coloquial_count / total_words * 3)  # Multiplicador para sensibilidad
    
    def _extract_context_clues(self, message: str) -> List[str]:
        """Extrae pistas de contexto del mensaje"""
        clues = []
        message_lower = message.lower()
        
        # Contextos específicos
        contexts = {
            'soat': ['soat', 'seguro', 'poliza', 'asegurar'],
            'vehicle': ['auto', 'carro', 'moto', 'camioneta', 'vehículo'],
            'money': ['precio', 'costo', 'pagar', 'plata', 'dinero'],
            'time': ['cuando', 'tiempo', 'pronto', 'ahora', 'mañana'],
            'problem': ['problema', 'error', 'falla', 'bronca', 'rollo']
        }
        
        for context, keywords in contexts.items():
            if any(keyword in message_lower for keyword in keywords):
                clues.append(context)
        
        return clues
    
    def _measure_intent_complexity(self, message: str) -> float:
        """Mide la complejidad de la intención (0-1)"""
        # Factores de complejidad
        factors = {
            'question_words': len(re.findall(r'\b(qué|cómo|cuándo|dónde|por qué|para qué)\b', 
                                           message.lower())),
            'multiple_topics': len(self._extract_context_clues(message)),
            'conditional_statements': len(re.findall(r'\b(si|cuando|aunque|pero)\b', 
                                                   message.lower())),
            'length_factor': min(1.0, len(message.split()) / 50)  # Normalizado a 50 palabras
        }
        
        complexity = sum(factors.values()) / len(factors)
        return min(1.0, complexity)
    
    def _detect_personality_mode(self, message: str, analysis: Dict) -> PersonalityMode:
        """Detecta qué modo de personalidad usar"""
        
        # Lógica de decisión basada en análisis
        if analysis['creativity_request']:
            return PersonalityMode.CREATIVO
        
        if analysis['emotion'] in ['frustrated', 'confused']:
            return PersonalityMode.EMPATICO
        
        if analysis['coloquial_level'] > 0.5:
            return PersonalityMode.COLOQUIAL
        
        if analysis['formality'] > 0.7:
            return PersonalityMode.FORMAL
        
        if analysis['emotion'] == 'excited':
            return PersonalityMode.DIVERTIDO
        
        if 'soat' in analysis['context_clues'] and analysis['intent_complexity'] > 0.6:
            return PersonalityMode.TECNICO
        
        # Libre albedrío: ocasionalmente elegir modo aleatorio
        if random.random() < self.free_will_factor * 0.2:  # 20% chance con libre albedrío
            return random.choice(list(PersonalityMode))
        
        return PersonalityMode.COLOQUIAL  # Default amigable
    
    def _adapt_vocabulary(self, message: str) -> Dict[str, str]:
        """Adapta vocabulario según el estilo del usuario"""
        adaptations = {}
        message_lower = message.lower()
        
        # Detectar términos del usuario y sugerir equivalentes
        for category, terms in self.coloquial_vocabulary.items():
            for term in terms:
                if term in message_lower:
                    # Sugerir un término similar pero diferente para variedad
                    available_terms = [t for t in terms if t != term]
                    if available_terms:
                        adaptations[category] = random.choice(available_terms)
        
        return adaptations
    
    def _generate_response_strategy(self, message: str, analysis: Dict, 
                                  personality: PersonalityMode, user_id: str) -> Dict[str, Any]:
        """Genera estrategia de respuesta con libre albedrío"""
        
        strategy = {
            'personality_mode': personality.value,
            'tone': self._determine_tone(analysis, personality),
            'creativity_elements': [],
            'coloquial_adaptations': [],
            'empathy_level': self._calculate_empathy_level(analysis),
            'humor_injection': self._should_inject_humor(analysis, personality),
            'free_will_choices': []
        }
        
        # Elementos creativos según personalidad
        if personality == PersonalityMode.CREATIVO:
            strategy['creativity_elements'] = [
                'metaphor', 'storytelling', 'imaginative_scenario'
            ]
        
        if personality == PersonalityMode.COLOQUIAL:
            strategy['coloquial_adaptations'] = [
                'use_local_expressions', 'informal_tone', 'friendly_terms'
            ]
        
        # Decisiones de libre albedrío
        free_will_decisions = self._make_free_will_decisions(message, analysis)
        strategy['free_will_choices'] = free_will_decisions
        
        return strategy
    
    def _determine_tone(self, analysis: Dict, personality: PersonalityMode) -> str:
        """Determina el tono de la respuesta"""
        
        tone_mapping = {
            PersonalityMode.FORMAL: 'professional',
            PersonalityMode.COLOQUIAL: 'friendly',
            PersonalityMode.CREATIVO: 'imaginative',
            PersonalityMode.EMPATICO: 'caring',
            PersonalityMode.TECNICO: 'informative',
            PersonalityMode.DIVERTIDO: 'playful',
            PersonalityMode.SABIO: 'wise'
        }
        
        base_tone = tone_mapping.get(personality, 'friendly')
        
        # Modificar según urgencia
        if analysis['urgency'] > 0.7:
            base_tone += '_urgent'
        
        return base_tone
    
    def _calculate_empathy_level(self, analysis: Dict) -> float:
        """Calcula nivel de empatía necesario"""
        base_empathy = self.personality_traits['empathy']
        
        # Aumentar empatía si hay frustración o confusión
        if analysis['emotion'] in ['frustrated', 'confused']:
            base_empathy += 0.3
        
        if analysis['urgency'] > 0.6:
            base_empathy += 0.2
        
        return min(1.0, base_empathy)
    
    def _should_inject_humor(self, analysis: Dict, personality: PersonalityMode) -> bool:
        """Decide si inyectar humor"""
        
        # No humor en situaciones muy urgentes o frustrantes
        if analysis['urgency'] > 0.8 or analysis['emotion'] == 'frustrated':
            return False
        
        # Más humor en modos divertidos
        if personality == PersonalityMode.DIVERTIDO:
            return True
        
        # Decisión basada en libre albedrío y nivel de humor
        humor_chance = self.personality_traits['humor'] * self.free_will_factor
        return random.random() < humor_chance
    
    def _make_free_will_decisions(self, message: str, analysis: Dict) -> List[str]:
        """Toma decisiones de libre albedrío"""
        decisions = []
        
        # Decisión de agregar elementos únicos
        if random.random() < self.free_will_factor:
            creative_decisions = [
                'add_unexpected_metaphor',
                'reference_previous_conversation',
                'inject_personality_quirk',
                'use_surprising_vocabulary',
                'add_empathetic_touch'
            ]
            
            num_decisions = random.randint(1, 3)
            decisions = random.sample(creative_decisions, min(num_decisions, len(creative_decisions)))
        
        return decisions
    
    def _calculate_free_will_factor(self, message: str) -> float:
        """Calcula factor de libre albedrío para esta respuesta"""
        base_factor = self.free_will_factor
        
        # Aumentar libre albedrío en conversaciones creativas
        if any(word in message.lower() for word in ['imagínate', 'crea', 'inventa']):
            base_factor += 0.2
        
        # Reducir en consultas técnicas muy específicas
        if any(word in message.lower() for word in ['precio', 'costo', 'requisitos']):
            base_factor -= 0.1
        
        return max(0.1, min(1.0, base_factor))
    
    def _calculate_creativity_boost(self, analysis: Dict) -> float:
        """Calcula boost de creatividad"""
        boost = 0.0
        
        if analysis['creativity_request']:
            boost += 0.5
        
        if analysis['emotion'] == 'excited':
            boost += 0.2
        
        if analysis['coloquial_level'] > 0.5:
            boost += 0.3
        
        return min(1.0, boost)
    
    def _update_memory(self, user_id: str, message: str, analysis: Dict):
        """Actualiza memoria contextual"""
        if user_id not in self.memory_fragments:
            self.memory_fragments[user_id] = []
        
        # Crear nuevo fragmento de memoria
        fragment = MemoryFragment(
            user_id=user_id,
            content=message[:100],  # Primeros 100 caracteres
            emotion=analysis['emotion'],
            importance=self._calculate_importance(analysis),
            timestamp=datetime.now(),
            connections=analysis['context_clues'],
            decay_rate=0.1
        )
        
        self.memory_fragments[user_id].append(fragment)
        
        # Limitar memoria (mantener últimas 50)
        if len(self.memory_fragments[user_id]) > 50:
            self.memory_fragments[user_id] = self.memory_fragments[user_id][-50:]
    
    def _calculate_importance(self, analysis: Dict) -> float:
        """Calcula importancia del mensaje para memoria"""
        importance = 0.5  # Base
        
        if analysis['urgency'] > 0.5:
            importance += 0.3
        
        if analysis['emotion'] in ['frustrated', 'excited']:
            importance += 0.2
        
        if analysis['intent_complexity'] > 0.6:
            importance += 0.2
        
        return min(1.0, importance)
    
    def _get_relevant_memory(self, user_id: str, current_message: str) -> List[Dict]:
        """Obtiene memoria relevante para el contexto actual"""
        if user_id not in self.memory_fragments:
            return []
        
        current_clues = self._extract_context_clues(current_message)
        relevant_memories = []
        
        for fragment in self.memory_fragments[user_id][-10:]:  # Últimas 10
            # Calcular relevancia
            relevance = 0.0
            
            # Relevancia por conexiones de contexto
            common_connections = set(fragment.connections) & set(current_clues)
            if common_connections:
                relevance += len(common_connections) * 0.3
            
            # Relevancia por importancia y recencia
            days_old = (datetime.now() - fragment.timestamp).days
            relevance += fragment.importance * max(0, 1 - days_old * fragment.decay_rate)
            
            if relevance > 0.2:  # Umbral de relevancia
                relevant_memories.append({
                    'content': fragment.content,
                    'emotion': fragment.emotion,
                    'relevance': relevance,
                    'age_days': days_old
                })
        
        # Ordenar por relevancia
        relevant_memories.sort(key=lambda x: x['relevance'], reverse=True)
        return relevant_memories[:3]  # Top 3
    
    def _learn_from_interaction(self, message: str, analysis: Dict, context: str):
        """Aprende del patrón de interacción"""
        
        # Crear clave de patrón
        pattern_key = f"{analysis['emotion']}_{analysis['urgency']:.1f}_{context}"
        
        if pattern_key not in self.conversation_patterns:
            self.conversation_patterns[pattern_key] = ConversationPattern(
                pattern=pattern_key,
                response_style="adaptive",
                context=LearningContext(context) if context in LearningContext.__members__.values() else LearningContext.CONVERSATION,
                effectiveness=0.5,
                usage_count=0,
                last_used=datetime.now(),
                variations=[]
            )
        
        # Actualizar patrón
        pattern = self.conversation_patterns[pattern_key]
        pattern.usage_count += 1
        pattern.last_used = datetime.now()
        
        # Adaptación de rasgos de personalidad
        self._adapt_personality_traits(analysis)
        
        self.logger.info(f"🧠 Patrón aprendido: {pattern_key}")
    
    def _adapt_personality_traits(self, analysis: Dict):
        """Adapta rasgos de personalidad basándose en la interacción"""
        
        # Ajustar adaptación coloquial
        if analysis['coloquial_level'] > 0.3:
            self.personality_traits['colloquial_adaptation'] += self.learning_rate * 0.1
        
        # Ajustar creatividad
        if analysis['creativity_request']:
            self.personality_traits['creativity'] += self.learning_rate * 0.05
        
        # Ajustar empatía según emociones detectadas
        if analysis['emotion'] in ['frustrated', 'confused']:
            self.personality_traits['empathy'] += self.learning_rate * 0.03
        
        # Mantener valores en rango 0-1
        for trait in self.personality_traits:
            self.personality_traits[trait] = max(0.0, min(1.0, self.personality_traits[trait]))
    
    def _load_previous_learning(self):
        """Carga aprendizaje previo desde archivo"""
        try:
            # Por ahora, inicializar con algunos patrones base
            self._initialize_base_patterns()
            self.logger.info("🧠 Conocimiento base cargado")
        except Exception as e:
            self.logger.warning(f"⚠️ No se pudo cargar aprendizaje previo: {e}")
    
    def _initialize_base_patterns(self):
        """Inicializa patrones base de conversación"""
        base_patterns = [
            {
                'pattern': 'frustrated_0.8_conversation',
                'style': 'empathetic_helpful',
                'context': LearningContext.PROBLEM_SOLVING
            },
            {
                'pattern': 'excited_0.6_conversation',
                'style': 'enthusiastic_engaging',
                'context': LearningContext.CONVERSATION
            },
            {
                'pattern': 'neutral_0.3_conversation',
                'style': 'friendly_informative',
                'context': LearningContext.CONVERSATION
            }
        ]
        
        for pattern_data in base_patterns:
            pattern = ConversationPattern(
                pattern=pattern_data['pattern'],
                response_style=pattern_data['style'],
                context=pattern_data['context'],
                effectiveness=0.7,
                usage_count=0,
                last_used=datetime.now(),
                variations=[]
            )
            self.conversation_patterns[pattern_data['pattern']] = pattern
    
    def _get_fallback_strategy(self) -> Dict[str, Any]:
        """Estrategia de respaldo en caso de error"""
        return {
            'message_analysis': {'emotion': 'neutral', 'urgency': 0.0},
            'personality_mode': PersonalityMode.COLOQUIAL,
            'vocab_adaptations': {},
            'response_strategy': {'tone': 'friendly'},
            'free_will_factor': 0.5,
            'creativity_boost': 0.0,
            'memory_context': []
        }
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del aprendizaje"""
        return {
            'patterns_learned': len(self.conversation_patterns),
            'personality_traits': self.personality_traits.copy(),
            'creativity_level': self.creativity_level,
            'free_will_factor': self.free_will_factor,
            'total_interactions': sum(p.usage_count for p in self.conversation_patterns.values()),
            'memory_fragments_total': sum(len(fragments) for fragments in self.memory_fragments.values())
        } 