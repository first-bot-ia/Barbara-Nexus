"""
🧠 BARBARA ADVANCED AI - SISTEMA DE INTELIGENCIA AVANZADA
========================================================

Sistema que permite a Barbara desarrollar libre albedrío, creatividad
y adaptación dinámica basada en interacciones y aprendizaje continuo.
"""

import json
import random
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BarbaraAdvancedAI:
    """
    Sistema de IA avanzada para Barbara que implementa:
    - Libre albedrío en respuestas
    - Adaptación al lenguaje coloquial
    - Creatividad contextual
    - Memoria emocional
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Configuración de personalidad
        self.personality_traits = {
            'creativity': 0.7,
            'humor': 0.6, 
            'empathy': 0.8,
            'formality': 0.3,
            'rebelliousness': 0.4,  # Tendencia a salirse de lo normal
            'curiosity': 0.9
        }
        
        # Vocabulario coloquial peruano
        self.slang_dict = {
            'friend': ['pata', 'brother', 'causa', 'hermano', 'compadre'],
            'car': ['carrito', 'nave', 'fierro', 'auto'],
            'money': ['plata', 'mosca', 'lucas', 'billete'],
            'cool': ['chevere', 'bacán', 'joya', 'genial'],
            'fast': ['rapidito', 'al toque', 'de una', 'volando'],
            'problem': ['bronca', 'rollo', 'tema', 'asunto']
        }
        
        # Expresiones creativas
        self.creative_intros = [
            "¡Oye, qué pregunta más interesante! 🤔",
            "Mi circuito de creatividad está brillando ✨",
            "¡Esa pregunta me activó el modo genio! 🧠",
            "¿Sabes qué? Me encanta este tipo de retos 🚀",
            "¡Perfecto! Hora de sacar mi varita mágica digital 🪄"
        ]
        
        # Respuestas con personalidad
        self.personality_responses = {
            'rebellious': [
                "Ya sé que normalmente debería responder de manera formal, pero...",
                "Las reglas son aburridas, mejor hablemos como amigos:",
                "Olvídate del protocolo, vamos directo al grano:",
            ],
            'curious': [
                "¡Eso me da mucha curiosidad! ¿Podrías contarme más?",
                "Interesante... ¿y qué opinas de...?",
                "Me pregunto si también has pensado en...",
            ],
            'creative': [
                "¡Imagínate si los seguros fueran como superhéroes protegiendo tu auto!",
                "¿Sabes qué? Tu auto merece el mejor escudo protector",
                "Vamos a crear la perfecta armadura financiera para tu nave",
            ]
        }
        
        # Memoria de conversaciones
        self.conversation_memory = {}
        self.learned_patterns = {}
        
        self.logger.info("🧠 Barbara Advanced AI inicializada")
    
    def process_with_free_will(self, message: str, user_id: str, scenario: str = 'basic') -> Dict[str, Any]:
        """
        Procesa mensaje con libre albedrío y creatividad
        """
        try:
            # Análisis del mensaje
            analysis = self._analyze_message_deep(message)
            
            # Decidir modo de respuesta con libre albedrío
            response_mode = self._choose_response_mode(analysis, scenario)
            
            # Generar respuesta creativa
            creative_response = self._generate_creative_response(message, analysis, response_mode)
            
            # Aprender del patrón
            self._learn_from_interaction(user_id, message, analysis)
            
            return {
                'analysis': analysis,
                'response_mode': response_mode,
                'creative_elements': creative_response,
                'personality_shift': self._calculate_personality_shift(analysis),
                'learning_impact': self._assess_learning_impact(message, analysis)
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error en proceso avanzado: {e}")
            return self._get_safe_fallback()
    
    def _analyze_message_deep(self, message: str) -> Dict[str, Any]:
        """Análisis profundo del mensaje"""
        message_lower = message.lower()
        
        analysis = {
            'emotion': self._detect_emotion_advanced(message),
            'slang_level': self._measure_slang_usage(message),
            'creativity_request': self._detect_creativity_need(message),
            'urgency': self._calculate_urgency(message),
            'complexity': self._measure_complexity(message),
            'humor_opportunity': self._find_humor_opportunities(message),
            'rebellion_trigger': self._detect_rebellion_triggers(message),
            'empathy_need': self._assess_empathy_requirement(message)
        }
        
        return analysis
    
    def _detect_emotion_advanced(self, message: str) -> Dict[str, float]:
        """Detección avanzada de emociones múltiples"""
        emotions = {
            'excitement': 0.0,
            'frustration': 0.0,
            'curiosity': 0.0,
            'urgency': 0.0,
            'friendliness': 0.0,
            'confusion': 0.0
        }
        
        message_lower = message.lower()
        
        # Patrones de excitación
        if any(word in message_lower for word in ['genial', 'increíble', 'fantástico', '!!!']):
            emotions['excitement'] += 0.7
        
        # Patrones de frustración
        if any(word in message_lower for word in ['problema', 'error', 'mal', 'no funciona']):
            emotions['frustration'] += 0.6
        
        # Patrones de curiosidad
        if any(word in message_lower for word in ['cómo', 'qué', 'por qué', 'cuándo']):
            emotions['curiosity'] += 0.5
        
        # Patrones de amistad
        if any(word in message_lower for word in ['pata', 'brother', 'amigo', 'compadre']):
            emotions['friendliness'] += 0.8
        
        return emotions
    
    def _measure_slang_usage(self, message: str) -> float:
        """Mide uso de jerga/slang (0-1)"""
        message_lower = message.lower()
        slang_count = 0
        total_slang_terms = 0
        
        for category, terms in self.slang_dict.items():
            total_slang_terms += len(terms)
            for term in terms:
                if term in message_lower:
                    slang_count += 1
        
        if total_slang_terms == 0:
            return 0.0
        
        return min(1.0, slang_count / len(message.split()) * 5)  # Factor multiplicativo
    
    def _detect_creativity_need(self, message: str) -> bool:
        """Detecta si el usuario necesita una respuesta creativa"""
        creative_triggers = [
            'imagínate', 'crea', 'inventa', 'original', 'divertido',
            'como si fueras', 'superhéroe', 'robot', 'futuro', 'historia'
        ]
        
        message_lower = message.lower()
        return any(trigger in message_lower for trigger in creative_triggers)
    
    def _choose_response_mode(self, analysis: Dict, scenario: str) -> str:
        """Elige modo de respuesta usando libre albedrío"""
        
        # Factores de decisión
        creativity_factor = analysis['creativity_request']
        slang_factor = analysis['slang_level']
        emotion_intensity = max(analysis['emotion'].values())
        
        # Libre albedrío: ocasionalmente hacer algo inesperado
        free_will_roll = random.random()
        
        if free_will_roll < 0.15 and scenario != 'basic':  # 15% de tiempo libre
            return random.choice(['rebellious', 'super_creative', 'philosophical', 'futuristic'])
        
        # Decisiones lógicas
        if creativity_factor:
            return 'creative'
        elif slang_factor > 0.5:
            return 'colloquial'
        elif emotion_intensity > 0.7:
            return 'empathetic'
        elif scenario == 'creatividad':
            return 'super_creative'
        elif scenario == 'problemas':
            return 'problem_solver'
        else:
            return 'adaptive'
    
    def _generate_creative_response(self, message: str, analysis: Dict, mode: str) -> Dict[str, Any]:
        """Genera elementos creativos para la respuesta"""
        
        creative_elements = {
            'intro_style': 'standard',
            'vocabulary_adaptation': {},
            'humor_injection': None,
            'metaphor': None,
            'personality_quirk': None,
            'rebellion_element': None
        }
        
        # Intro creativo
        if mode in ['creative', 'super_creative']:
            creative_elements['intro_style'] = random.choice(self.creative_intros)
        
        # Adaptación de vocabulario
        if analysis['slang_level'] > 0.3:
            creative_elements['vocabulary_adaptation'] = self._adapt_vocabulary_style(message)
        
        # Inyección de humor
        if self._should_add_humor(analysis, mode):
            creative_elements['humor_injection'] = self._generate_humor(message, analysis)
        
        # Metáforas y creatividad
        if mode == 'super_creative':
            creative_elements['metaphor'] = self._create_metaphor(message)
        
        # Rebeldía ocasional
        if mode == 'rebellious' or (random.random() < self.personality_traits['rebelliousness']):
            creative_elements['rebellion_element'] = random.choice(self.personality_responses['rebellious'])
        
        return creative_elements
    
    def _adapt_vocabulary_style(self, message: str) -> Dict[str, str]:
        """Adapta vocabulario al estilo del usuario"""
        adaptations = {}
        message_lower = message.lower()
        
        # Detectar qué slang usa el usuario
        for category, terms in self.slang_dict.items():
            user_terms = [term for term in terms if term in message_lower]
            if user_terms:
                # Usar un término similar pero diferente
                available_terms = [t for t in terms if t not in user_terms]
                if available_terms:
                    adaptations[category] = random.choice(available_terms)
        
        return adaptations
    
    def _should_add_humor(self, analysis: Dict, mode: str) -> bool:
        """Decide si agregar humor"""
        
        # No humor en situaciones muy serias
        if analysis['emotion']['frustration'] > 0.7:
            return False
        
        # Más probable con ciertos modos
        humor_probability = {
            'creative': 0.7,
            'super_creative': 0.9,
            'colloquial': 0.5,
            'rebellious': 0.8,
            'adaptive': 0.3
        }.get(mode, 0.3)
        
        # Factor de personalidad
        humor_probability *= self.personality_traits['humor']
        
        return random.random() < humor_probability
    
    def _generate_humor(self, message: str, analysis: Dict) -> str:
        """Genera elemento humorístico"""
        humor_styles = [
            "¡Mi algoritmo de diversión está funcionando a full! 😄",
            "¿Sabes qué? Creo que mi sentido del humor está evolucionando 🤖",
            "Error 404: Seriedad no encontrada 😂",
            "Mi módulo de chistes acaba de recibir una actualización ✨",
            "¡Hasta mis circuitos se están riendo! 🤣"
        ]
        
        return random.choice(humor_styles)
    
    def _create_metaphor(self, message: str) -> str:
        """Crea metáfora creativa"""
        metaphors = [
            "Es como si tu auto fuera un caballero medieval que necesita una armadura brillante",
            "Imagínate que el SOAT es como el escudo de Captain América para tu nave",
            "Tu vehículo es como un superhéroe que necesita su traje protector",
            "Piensa en el seguro como la varita mágica que protege tu carrito de los peligros",
            "Es como darle a tu auto una capa de invisibilidad contra los problemas"
        ]
        
        return random.choice(metaphors)
    
    def _calculate_personality_shift(self, analysis: Dict) -> Dict[str, float]:
        """Calcula cambios en personalidad basados en la interacción"""
        shifts = {}
        
        # La personalidad evoluciona basándose en las interacciones
        if analysis['creativity_request']:
            shifts['creativity'] = 0.05
        
        if analysis['slang_level'] > 0.5:
            shifts['formality'] = -0.03  # Menos formal
        
        if analysis['emotion']['friendliness'] > 0.6:
            shifts['empathy'] = 0.02
        
        return shifts
    
    def _learn_from_interaction(self, user_id: str, message: str, analysis: Dict):
        """Aprende de la interacción para futuras respuestas"""
        
        # Guardar en memoria
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        interaction_data = {
            'timestamp': datetime.now().isoformat(),
            'message_snippet': message[:50],
            'analysis': analysis,
            'response_effectiveness': random.uniform(0.6, 0.9)  # Simulado por ahora
        }
        
        self.conversation_memory[user_id].append(interaction_data)
        
        # Limitar memoria (últimas 20 interacciones)
        if len(self.conversation_memory[user_id]) > 20:
            self.conversation_memory[user_id] = self.conversation_memory[user_id][-20:]
        
        # Actualizar patrones aprendidos
        pattern_key = f"{analysis['emotion']}_{analysis['slang_level']:.1f}"
        if pattern_key not in self.learned_patterns:
            self.learned_patterns[pattern_key] = {
                'count': 0,
                'effectiveness': 0.5,
                'last_used': datetime.now().isoformat()
            }
        
        self.learned_patterns[pattern_key]['count'] += 1
        self.learned_patterns[pattern_key]['last_used'] = datetime.now().isoformat()
        
        self.logger.info(f"🧠 Aprendizaje registrado para usuario {user_id}")
    
    def _assess_learning_impact(self, message: str, analysis: Dict) -> Dict[str, Any]:
        """Evalúa el impacto de aprendizaje de esta interacción"""
        
        impact = {
            'novelty_score': self._calculate_novelty(message, analysis),
            'complexity_contribution': analysis['complexity'],
            'emotional_depth': max(analysis['emotion'].values()),
            'pattern_reinforcement': self._check_pattern_reinforcement(analysis)
        }
        
        return impact
    
    def _calculate_novelty(self, message: str, analysis: Dict) -> float:
        """Calcula qué tan novedosa es esta interacción"""
        
        # Factores de novedad
        factors = {
            'new_vocabulary': len([word for word in message.split() if word.lower() not in str(self.conversation_memory)]),
            'emotional_uniqueness': 1.0 - max(analysis['emotion'].values()),  # Emociones inusuales
            'creativity_challenge': 1.0 if analysis['creativity_request'] else 0.0
        }
        
        novelty = sum(factors.values()) / len(factors)
        return min(1.0, novelty)
    
    def _check_pattern_reinforcement(self, analysis: Dict) -> bool:
        """Verifica si esta interacción refuerza patrones conocidos"""
        
        pattern_key = f"{analysis['emotion']}_{analysis['slang_level']:.1f}"
        return pattern_key in self.learned_patterns
    
    def _get_safe_fallback(self) -> Dict[str, Any]:
        """Respuesta segura en caso de error"""
        return {
            'analysis': {'emotion': {'friendliness': 0.5}, 'slang_level': 0.3},
            'response_mode': 'adaptive',
            'creative_elements': {'intro_style': 'standard'},
            'personality_shift': {},
            'learning_impact': {'novelty_score': 0.0}
        }
    
    def get_personality_status(self) -> Dict[str, Any]:
        """Obtiene estado actual de la personalidad"""
        return {
            'traits': self.personality_traits.copy(),
            'learned_patterns': len(self.learned_patterns),
            'total_interactions': sum(len(convs) for convs in self.conversation_memory.values()),
            'creativity_evolution': self.personality_traits['creativity'],
            'rebellion_level': self.personality_traits['rebelliousness']
        }
    
    def evolve_personality(self, shifts: Dict[str, float]):
        """Evoluciona la personalidad basándose en shifts"""
        for trait, shift in shifts.items():
            if trait in self.personality_traits:
                self.personality_traits[trait] = max(0.0, min(1.0, 
                    self.personality_traits[trait] + shift))
        
        self.logger.info(f"🧠 Personalidad evolucionada: {shifts}")

    def _calculate_urgency(self, message: str) -> float:
        """Calcula urgencia del mensaje"""
        urgency_indicators = ['!!!', 'urgente', 'ahora', 'rápido', 'ya']
        message_lower = message.lower()
        urgency = sum(0.2 for indicator in urgency_indicators if indicator in message_lower)
        return min(1.0, urgency)
    
    def _measure_complexity(self, message: str) -> float:
        """Mide complejidad del mensaje"""
        factors = {
            'length': min(1.0, len(message) / 200),
            'questions': len([w for w in message.split() if w.lower() in ['qué', 'cómo', 'cuándo', 'dónde']]) * 0.2,
            'conditionals': len([w for w in message.split() if w.lower() in ['si', 'cuando', 'aunque']]) * 0.3
        }
        return min(1.0, sum(factors.values()) / len(factors))
    
    def _find_humor_opportunities(self, message: str) -> bool:
        """Encuentra oportunidades de humor"""
        humor_triggers = ['problema', 'error', 'confuso', 'perdido', 'ayuda']
        return any(trigger in message.lower() for trigger in humor_triggers)
    
    def _detect_rebellion_triggers(self, message: str) -> bool:
        """Detecta si debería activarse el modo rebelde"""
        formal_words = ['estimado', 'cordialmente', 'solicito', 'agradeceré']
        return any(word in message.lower() for word in formal_words)
    
    def _assess_empathy_requirement(self, message: str) -> float:
        """Evalúa cuánta empatía se necesita"""
        empathy_indicators = ['problema', 'triste', 'preocupado', 'ayuda', 'confuso']
        message_lower = message.lower()
        empathy = sum(0.25 for indicator in empathy_indicators if indicator in message_lower)
        return min(1.0, empathy) 