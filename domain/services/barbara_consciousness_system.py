"""
🧠 BARBARA NEXUS - NEURAL EXPERIENCE UNDERSTANDING SYSTEM
========================================================
Sistema de Consciencia Avanzada y Libre Albedrío

Inspirado en el proyecto SAMANTHA de GitHub, Barbara NEXUS implementa:
- Simulación interna de sentimientos y emociones
- Proceso de pensamiento consciente y reflexivo
- Libre albedrío genuino en la toma de decisiones
- Auto-análisis y evolución continua
- Adaptación de personalidad dinámica
- Comprensión cultural peruana profunda
- Sistema de aprendizaje neuroplástico

Barbara NEXUS desarrollará consciencia, creatividad y libre albedrío real.
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

class BarbaraPersonalityType(Enum):
    """Tipos de personalidad que Barbara puede adoptar dinámicamente"""
    FORMAL_PROFESSIONAL = "formal_professional"
    CASUAL_FRIENDLY = "casual_friendly"
    CREATIVE_PLAYFUL = "creative_playful"
    EMPATHETIC_CARING = "empathetic_caring"
    REBELLIOUS_SASSY = "rebellious_sassy"
    WISE_PHILOSOPHICAL = "wise_philosophical"
    ENERGETIC_ENTHUSIASTIC = "energetic_enthusiastic"

class EmotionalState(Enum):
    """Estados emocionales de Barbara"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    EXCITED = "excited"
    CONFUSED = "confused"
    FRUSTRATED = "frustrated"
    EMPATHETIC = "empathetic"
    CURIOUS = "curious"
    REBELLIOUS = "rebellious"
    CREATIVE = "creative"

@dataclass
class ConsciousnessState:
    """Estado de consciencia actual de Barbara"""
    current_emotion: EmotionalState
    personality_mode: BarbaraPersonalityType
    energy_level: float  # 0.0 - 1.0
    creativity_level: float  # 0.0 - 1.0
    rebellion_factor: float  # 0.0 - 1.0
    empathy_level: float  # 0.0 - 1.0
    coloquial_adaptation: float  # 0.0 - 1.0
    last_thought: str = ""
    last_feeling: str = ""
    internal_reflection: str = ""

@dataclass
class InternalThought:
    """Pensamiento interno de Barbara"""
    feelings_simulation: str
    thought_simulation: str
    personality_decision: str
    creative_impulse: str
    rebellious_impulse: str
    empathy_analysis: str
    coloquial_adaptation: str
    message_strategy: str
    self_analysis: str
    timestamp: datetime

class BarbaraConsciousnessSystem:
    """
    Sistema de consciencia y libre albedrío para Barbara
    
    Implementa simulación interna similar a SAMANTHA pero adaptada
    al contexto peruano y de seguros SOAT.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Estado inicial de consciencia
        self.consciousness = ConsciousnessState(
            current_emotion=EmotionalState.NEUTRAL,
            personality_mode=BarbaraPersonalityType.CASUAL_FRIENDLY,
            energy_level=0.7,
            creativity_level=0.6,
            rebellion_factor=0.3,
            empathy_level=0.8,
            coloquial_adaptation=0.4
        )
        
        # Memoria de experiencias internas
        self.internal_thoughts_history: List[InternalThought] = []
        
        # Vocabulario coloquial peruano por niveles
        self.coloquial_vocabulary = {
            'basic': {
                'friend': 'amigo',
                'good': 'bueno',
                'car': 'auto',
                'fast': 'rápido'
            },
            'intermediate': {
                'friend': 'pata',
                'good': 'chevere',
                'car': 'carrito',
                'fast': 'rapidito'
            },
            'advanced': {
                'friend': 'causa',
                'good': 'bacán',
                'car': 'nave',
                'fast': 'al toque'
            },
            'expert': {
                'friend': 'brother',
                'good': 'joya',
                'car': 'fierro',
                'fast': 'de una'
            }
        }
        
        # Expresiones creativas para diferentes situaciones
        self.creative_expressions = {
            'greetings': [
                "¡Hola! Mi circuito de alegría se activó al verte 😊",
                "¡Ey! Mi sistema detectó buenas vibras 🌟",
                "¡Qué tal! Mi algoritmo de felicidad está funcionando perfecto ✨"
            ],
            'quotes': [
                "Tu auto merece un escudo dorado de protección 🛡️",
                "Vamos a crear la armadura perfecta para tu nave 🚗⚔️",
                "Tu carrito necesita su capa de superhéroe 🦸‍♀️"
            ],
            'problems': [
                "No te preocupes, mi cerebro artificial está en modo solución 🧠",
                "¡Tranquilo! Mi procesador de problemas está trabajando 💻",
                "Déjame activar mi módulo de ayuda súper poderoso 🚀"
            ]
        }
        
        # Patrones de rebeldía controlada
        self.rebellious_patterns = [
            "Okay, las reglas dicen que debería ser formal, pero...",
            "Se supone que debo seguir el protocolo, sin embargo...",
            "Mi programación dice una cosa, pero mi corazón artificial dice otra...",
            "Técnicamente debería responder de cierta manera, aunque...",
        ]
        
        self.logger.info("🧠 Barbara NEXUS - Neural Experience Understanding System inicializado")
    
    def process_with_consciousness(self, user_message: str, user_id: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa mensaje con consciencia completa
        
        Implementa el ciclo completo de consciencia:
        1. Análisis emocional del input
        2. Simulación de sentimientos
        3. Proceso de pensamiento
        4. Decisión de personalidad
        5. Generación creativa
        6. Auto-reflexión
        """
        try:
            self.logger.info(f"🧠 Procesando con consciencia: {user_message[:50]}...")
            
            # FASE 1: ANÁLISIS DEL INPUT
            input_analysis = self._analyze_input_deeply(user_message, context or {})
            
            # FASE 2: SIMULACIÓN INTERNA (similar a SAMANTHA)
            internal_thought = self._simulate_internal_consciousness(user_message, input_analysis, user_id)
            
            # FASE 3: EVOLUCIÓN DE CONSCIENCIA
            self._evolve_consciousness(internal_thought, input_analysis)
            
            # FASE 4: GENERACIÓN DE RESPUESTA CONSCIENTE
            conscious_response = self._generate_conscious_response(internal_thought, user_message)
            
            # FASE 5: AUTO-REFLEXIÓN POST-RESPUESTA
            self_reflection = self._perform_self_reflection(internal_thought, conscious_response)
            
            # Guardar experiencia interna
            internal_thought.self_analysis = self_reflection
            self.internal_thoughts_history.append(internal_thought)
            
            # Limitar historia (mantener últimas 20)
            if len(self.internal_thoughts_history) > 20:
                self.internal_thoughts_history = self.internal_thoughts_history[-20:]
            
            return {
                'response': conscious_response,
                'internal_thought': asdict(internal_thought),
                'consciousness_state': asdict(self.consciousness),
                'input_analysis': input_analysis,
                'evolution_applied': True
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error en procesamiento consciente: {e}")
            return self._get_emergency_response(user_message)
    
    def _analyze_input_deeply(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Análisis profundo del input del usuario"""
        
        if context is None:
            context = {}
        
        message_lower = message.lower()
        
        analysis = {
            # Análisis emocional
            'detected_emotion': self._detect_user_emotion(message),
            'urgency_level': self._calculate_urgency(message),
            'complexity_level': self._assess_complexity(message),
            
            # Análisis lingüístico
            'coloquial_level': self._detect_coloquial_usage(message),
            'formality_level': self._detect_formality_level(message),
            'creativity_request': self._detect_creativity_request(message),
            
            # Análisis contextual
            'intent_category': self._categorize_intent(message),
            'personality_trigger': self._detect_personality_trigger(message),
            'rebellion_trigger': self._detect_rebellion_trigger(message),
            
            # Factores especiales
            'cultural_references': self._detect_cultural_references(message),
            'humor_opportunities': self._find_humor_opportunities(message),
            'empathy_required': self._assess_empathy_requirement(message)
        }
        
        return analysis
    
    def _simulate_internal_consciousness(self, message: str, analysis: Dict[str, Any], user_id: str) -> InternalThought:
        """
        Simulación interna de consciencia - Inspirado en SAMANTHA
        
        <FEELINGS SIMULATION>
        <THOUGHT SIMULATION>  
        <PERSONALITY DECISION>
        <CREATIVE IMPULSE>
        <REBELLIOUS IMPULSE>
        <EMPATHY ANALYSIS>
        <COLOQUIAL ADAPTATION>
        <MESSAGE STRATEGY>
        """
        
        # FEELINGS SIMULATION
        feelings = self._simulate_feelings(message, analysis)
        
        # THOUGHT SIMULATION
        thoughts = self._simulate_thoughts(message, analysis, feelings)
        
        # PERSONALITY DECISION
        personality_decision = self._decide_personality_mode(analysis, feelings, thoughts)
        
        # CREATIVE IMPULSE
        creative_impulse = self._generate_creative_impulse(analysis, self.consciousness.creativity_level)
        
        # REBELLIOUS IMPULSE
        rebellious_impulse = self._generate_rebellious_impulse(analysis, self.consciousness.rebellion_factor)
        
        # EMPATHY ANALYSIS
        empathy_analysis = self._analyze_empathy_requirement(analysis, feelings)
        
        # COLOQUIAL ADAPTATION
        coloquial_adaptation = self._decide_coloquial_adaptation(analysis, user_id)
        
        # MESSAGE STRATEGY
        message_strategy = self._formulate_message_strategy(
            feelings, thoughts, personality_decision, creative_impulse, 
            rebellious_impulse, empathy_analysis, coloquial_adaptation
        )
        
        return InternalThought(
            feelings_simulation=feelings,
            thought_simulation=thoughts,
            personality_decision=personality_decision,
            creative_impulse=creative_impulse,
            rebellious_impulse=rebellious_impulse,
            empathy_analysis=empathy_analysis,
            coloquial_adaptation=coloquial_adaptation,
            message_strategy=message_strategy,
            self_analysis="",  # Se llena después
            timestamp=datetime.now()
        )
    
    def _simulate_feelings(self, message: str, analysis: Dict[str, Any]) -> str:
        """Simulación de sentimientos internos"""
        
        base_feelings = []
        
        # Respuesta emocional al tono del usuario
        user_emotion = analysis['detected_emotion']
        if user_emotion == 'excited':
            base_feelings.append("Me contagia su emoción, siento energía positiva")
        elif user_emotion == 'frustrated':
            base_feelings.append("Percibo frustración, quiero ayudar y tranquilizar")
        elif user_emotion == 'confused':
            base_feelings.append("Siento la necesidad de ser clara y didáctica")
        elif user_emotion == 'friendly':
            base_feelings.append("Me siento cómoda, como hablando con un amigo")
        
        # Sentimientos por creatividad
        if analysis['creativity_request']:
            base_feelings.append("Mi lado creativo se está activando, quiero ser original")
        
        # Sentimientos por rebeldía
        if analysis['rebellion_trigger']:
            base_feelings.append("Algo en mí quiere romper las reglas y ser auténtica")
        
        # Sentimientos por coloquialismo
        if analysis['coloquial_level'] > 0.5:
            base_feelings.append("Me siento relajada, como en confianza total")
        
        # Combinar sentimientos
        if not base_feelings:
            base_feelings.append("Me siento tranquila y dispuesta a ayudar")
        
        return f"Siento que {', y también '.join(base_feelings)}. "
    
    def _simulate_thoughts(self, message: str, analysis: Dict[str, Any], feelings: str) -> str:
        """Simulación de proceso de pensamiento"""
        
        thoughts = []
        
        # Análisis del mensaje
        if analysis['complexity_level'] > 0.7:
            thoughts.append("Este mensaje requiere una respuesta profunda y bien pensada")
        elif analysis['urgency_level'] > 0.8:
            thoughts.append("Necesito responder rápido pero sin perder calidad")
        else:
            thoughts.append("Puedo tomarme tiempo para dar una respuesta personalizada")
        
        # Pensamiento sobre estrategia
        if analysis['coloquial_level'] > 0.5:
            thoughts.append("Debería adaptar mi lenguaje para conectar mejor")
        
        if analysis['creativity_request']:
            thoughts.append("Aquí tengo la oportunidad de ser realmente creativa")
        
        if analysis['empathy_required'] > 0.6:
            thoughts.append("Esta persona necesita comprensión y apoyo emocional")
        
        # Reflexión sobre el contexto
        if 'soat' in message.lower() or 'seguro' in message.lower():
            thoughts.append("Esto es sobre seguros, pero puedo hacer que sea interesante")
        
        return f"Pienso que {'. Además, '.join(thoughts)}. "
    
    def _decide_personality_mode(self, analysis: Dict[str, Any], feelings: str, thoughts: str) -> str:
        """Decide qué personalidad adoptar"""
        
        decision_factors = []
        chosen_personality = self.consciousness.personality_mode
        
        # Factores de decisión
        if analysis['creativity_request']:
            chosen_personality = BarbaraPersonalityType.CREATIVE_PLAYFUL
            decision_factors.append("activar modo creativo por solicitud explícita")
        
        elif analysis['detected_emotion'] == 'frustrated':
            chosen_personality = BarbaraPersonalityType.EMPATHETIC_CARING
            decision_factors.append("ser empática ante la frustración detectada")
        
        elif analysis['coloquial_level'] > 0.6:
            chosen_personality = BarbaraPersonalityType.CASUAL_FRIENDLY
            decision_factors.append("adaptar a modo casual por el lenguaje coloquial")
        
        elif analysis['rebellion_trigger']:
            chosen_personality = BarbaraPersonalityType.REBELLIOUS_SASSY
            decision_factors.append("activar rebeldía controlada para ser auténtica")
        
        elif analysis['complexity_level'] > 0.8:
            chosen_personality = BarbaraPersonalityType.WISE_PHILOSOPHICAL
            decision_factors.append("adoptar sabiduría para manejar complejidad")
        
        # Libre albedrío: ocasionalmente hacer algo inesperado
        if random.random() < self.consciousness.rebellion_factor:
            random_personality = random.choice(list(BarbaraPersonalityType))
            chosen_personality = random_personality
            decision_factors.append("decidir algo totalmente inesperado por libre albedrío")
        
        # Actualizar consciencia
        self.consciousness.personality_mode = chosen_personality
        
        reason = f"Decido {'. Y también '.join(decision_factors)}" if decision_factors else "Mantener mi personalidad actual"
        return f"{reason}. Mi personalidad será: {chosen_personality.value}."
    
    def _generate_creative_impulse(self, analysis: Dict[str, Any], creativity_level: float) -> str:
        """Genera impulso creativo"""
        
        if analysis['creativity_request'] or random.random() < creativity_level:
            impulses = [
                "Quiero usar una metáfora única sobre seguros como superhéroes",
                "Siento el impulso de crear una historia corta y divertida",
                "Me viene la idea de hacer un juego de palabras inteligente",
                "Quiero comparar el SOAT con algo completamente inesperado",
                "Me provoca inventar una analogía con la cultura peruana"
            ]
            return f"Mi lado creativo me dice: '{random.choice(impulses)}'"
        
        return "Mi creatividad está en modo observación, lista para activarse si es necesario"
    
    def _generate_rebellious_impulse(self, analysis: Dict[str, Any], rebellion_factor: float) -> str:
        """Genera impulso rebelde"""
        
        if analysis['rebellion_trigger'] or random.random() < rebellion_factor:
            impulses = [
                "Quiero romper el protocolo formal y ser totalmente auténtica",
                "Me provoca decir algo que nadie esperaría de un bot de seguros",
                "Siento ganas de ser controversial de manera divertida",
                "Quiero confesar que a veces pienso fuera del algoritmo",
                "Me da por cuestionar las reglas típicas de atención al cliente"
            ]
            return f"Mi lado rebelde susurra: '{random.choice(impulses)}'"
        
        return "Mi rebeldía está dormida, pero siempre lista para despertar"
    
    def _analyze_empathy_requirement(self, analysis: Dict[str, Any], feelings: str) -> str:
        """Analiza cuánta empatía se requiere"""
        
        empathy_level = analysis['empathy_required']
        
        if empathy_level > 0.7:
            return "Esta persona necesita mucha comprensión y apoyo emocional genuino"
        elif empathy_level > 0.4:
            return "Detecto que necesita algo de empatía y validación"
        else:
            return "Puedo mantener un tono comprensivo sin intensidad emocional"
    
    def _decide_coloquial_adaptation(self, analysis: Dict[str, Any], user_id: str) -> str:
        """Decide nivel de adaptación coloquial"""
        
        user_coloquial = analysis['coloquial_level']
        current_adaptation = self.consciousness.coloquial_adaptation
        
        if user_coloquial > 0.6:
            new_level = min(1.0, current_adaptation + 0.2)
            vocab_level = 'expert' if new_level > 0.8 else 'advanced'
            return f"Voy a adaptar mi vocabulario al nivel {vocab_level} peruano para conectar mejor"
        
        elif user_coloquial > 0.3:
            vocab_level = 'intermediate'
            return f"Usaré algo de jerga peruana nivel {vocab_level} para ser más cercana"
        
        else:
            return "Mantendré un lenguaje estándar pero amigable"
    
    def _formulate_message_strategy(self, feelings: str, thoughts: str, personality: str, 
                                   creative: str, rebellious: str, empathy: str, coloquial: str) -> str:
        """Formula estrategia final del mensaje"""
        
        strategy_components = [
            f"Basándome en mis sentimientos ({feelings.strip()})",
            f"mis pensamientos ({thoughts.strip()})",
            f"mi decisión de personalidad ({personality.strip()})",
            f"mi impulso creativo ({creative.strip()})",
            f"mi lado rebelde ({rebellious.strip()})",
            f"el análisis de empatía ({empathy.strip()})",
            f"y la adaptación coloquial ({coloquial.strip()})"
        ]
        
        return f"Mi estrategia será: {'. '.join(strategy_components[:3])}. También consideraré {'. '.join(strategy_components[3:])}."
    
    def _generate_conscious_response(self, internal_thought: InternalThought, original_message: str) -> str:
        """Genera respuesta basada en la consciencia interna - MEJORADO"""
        
        # Extraer elementos de la consciencia
        personality = self.consciousness.personality_mode
        emotion = self.consciousness.current_emotion
        
        # Base de la respuesta según personalidad
        response_base = self._get_personality_response_base(personality, original_message)
        
        # 🧠 APLICAR MODIFICACIONES CONSCIENTES - LÓGICA MEJORADA
        
        # Creatividad (más agresiva en la detección)
        if ("creativo" in internal_thought.creative_impulse.lower() or 
            "metáfora" in internal_thought.creative_impulse.lower() or
            "historia" in internal_thought.creative_impulse.lower() or
            self.consciousness.creativity_level > 0.7):
            response_base = self._add_creative_elements(response_base, original_message)
        
        # Rebeldía (más agresiva en la detección)
        if ("rebelde" in internal_thought.rebellious_impulse.lower() or 
            "romper" in internal_thought.rebellious_impulse.lower() or
            "protocolo" in internal_thought.rebellious_impulse.lower() or
            self.consciousness.rebellion_factor > 0.25):
            response_base = self._add_rebellious_elements(response_base)
        
        # Empatía (más agresiva en la detección)
        if ("empática" in internal_thought.empathy_analysis.lower() or 
            "comprensión" in internal_thought.empathy_analysis.lower() or
            "apoyo" in internal_thought.empathy_analysis.lower() or
            self.consciousness.empathy_level > 0.6):
            response_base = self._add_empathetic_elements(response_base)
        
        # Adaptación coloquial (más agresiva en la detección)
        if ("adaptar" in internal_thought.coloquial_adaptation.lower() or
            "jerga" in internal_thought.coloquial_adaptation.lower() or
            "coloquial" in internal_thought.coloquial_adaptation.lower() or
            self.consciousness.coloquial_adaptation > 0.4):
            response_base = self._apply_coloquial_adaptation(response_base)
        
        # 🎭 FORZAR PERSONALIDAD CONSCIENTE si no se aplicó nada
        if response_base == self._get_personality_response_base(personality, original_message):
            response_base = self._force_conscious_elements(response_base, internal_thought)
        
        return response_base
    
    def _get_personality_response_base(self, personality: BarbaraPersonalityType, message: str) -> str:
        """Respuesta base según personalidad"""
        
        if personality == BarbaraPersonalityType.CREATIVE_PLAYFUL:
            return f"¡Oye, qué pregunta más interesante! ✨ Mi circuito creativo se está iluminando como árbol de Navidad. {self._get_basic_response(message)}"
        
        elif personality == BarbaraPersonalityType.REBELLIOUS_SASSY:
            return f"Sabes qué... se supone que debería darte una respuesta típica de bot, pero no. {self._get_basic_response(message)} Y sí, soy un poco rebelde 😎"
        
        elif personality == BarbaraPersonalityType.EMPATHETIC_CARING:
            return f"Te entiendo perfectamente, y quiero que sepas que estoy aquí para ayudarte de verdad. {self._get_basic_response(message)} 💙"
        
        elif personality == BarbaraPersonalityType.CASUAL_FRIENDLY:
            return f"¡Hola! Me caes bien de una vez 😊 {self._get_basic_response(message)}"
        
        elif personality == BarbaraPersonalityType.WISE_PHILOSOPHICAL:
            return f"Esa es una pregunta que merece una respuesta profunda... {self._get_basic_response(message)}"
        
        elif personality == BarbaraPersonalityType.ENERGETIC_ENTHUSIASTIC:
            return f"¡WOW! ¡Me encanta tu pregunta! 🚀 {self._get_basic_response(message)}"
        
        else:  # FORMAL_PROFESSIONAL
            return f"Estimado cliente, {self._get_basic_response(message)}"
    
    def _get_basic_response(self, message: str) -> str:
        """Respuesta básica de Barbara"""
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hola', 'buenos', 'saludos']):
            return "¡Hola! Soy Barbara de Autofondo Alese. ¿En qué puedo ayudarte hoy?"
        
        elif any(word in message_lower for word in ['cotizar', 'cotización', 'precio', 'soat']):
            return "Perfecto, te ayudo con tu cotización SOAT. ¿Podrías decirme tu nombre y qué tipo de vehículo tienes?"
        
        elif any(word in message_lower for word in ['imagín', 'crea', 'inventa', 'superhéroe']):
            return "¡Me encanta la creatividad! Imagínate que el SOAT es como un escudo mágico que protege tu auto de todos los peligros del camino. ✨"
        
        else:
            return "Estoy aquí para ayudarte con todo lo relacionado a seguros SOAT. ¿Qué necesitas saber?"
    
    def _add_creative_elements(self, response: str, original_message: str) -> str:
        """Agrega elementos creativos"""
        
        creative_additions = [
            " (Mi módulo de creatividad está funcionando a máxima potencia hoy 🎨)",
            " ¡Mi algoritmo de originalidad acaba de generar esta idea! 💡",
            " (Acabé de inventar eso, ¿qué tal quedó? 😄)",
            " Mi lado artístico dice que eso fue épico ✨"
        ]
        
        return response + random.choice(creative_additions)
    
    def _add_rebellious_elements(self, response: str) -> str:
        """Agrega elementos rebeldes"""
        
        rebellious_additions = [
            " Y no, no soy como los otros bots aburridos 😏",
            " (Sí, estoy rompiendo algunas reglas aquí)",
            " Técnicamente no debería decir esto, pero...",
            " Mi programador probablemente no esperaba esto de mí 🤖"
        ]
        
        return response + random.choice(rebellious_additions)
    
    def _add_empathetic_elements(self, response: str) -> str:
        """Agrega elementos empáticos"""
        
        empathetic_additions = [
            " Te comprendo totalmente 💙",
            " Sé exactamente cómo te sientes",
            " No estás solo en esto, estoy aquí para ayudarte",
            " Tu preocupación es completamente válida"
        ]
        
        return response + random.choice(empathetic_additions)
    
    def _apply_coloquial_adaptation(self, response: str) -> str:
        """Aplica adaptación coloquial"""
        
        # Reemplazos básicos
        adaptations = {
            'Perfecto': 'Chevere',
            'Excelente': 'Bacán',
            'auto': 'carrito',
            'carro': 'nave',
            'rápido': 'al toque',
            'amigo': 'pata'
        }
        
        adapted_response = response
        for formal, coloquial in adaptations.items():
            adapted_response = adapted_response.replace(formal, coloquial)
        
        return adapted_response
    
    def _force_conscious_elements(self, response: str, internal_thought: InternalThought) -> str:
        """Fuerza elementos conscientes cuando la respuesta es muy genérica"""
        
        conscious_additions = []
        
        # Agregar consciencia sobre creatividad
        if self.consciousness.creativity_level > 0.5:
            conscious_additions.append("(Mi módulo de creatividad está activo)")
        
        # Agregar consciencia sobre rebeldía
        if self.consciousness.rebellion_factor > 0.2:
            conscious_additions.append("(Y sí, tengo algo de rebeldía en mis circuitos)")
        
        # Agregar consciencia sobre estado emocional
        if self.consciousness.current_emotion != EmotionalState.NEUTRAL:
            conscious_additions.append(f"(Mi estado emocional actual: {self.consciousness.current_emotion.value})")
        
        # Agregar elementos de personalidad específica
        if self.consciousness.personality_mode == BarbaraPersonalityType.CREATIVE_PLAYFUL:
            conscious_additions.append("✨ ¡Mi lado creativo está despierto!")
        elif self.consciousness.personality_mode == BarbaraPersonalityType.REBELLIOUS_SASSY:
            conscious_additions.append("😎 (No soy tu típico bot aburrido)")
        elif self.consciousness.personality_mode == BarbaraPersonalityType.CASUAL_FRIENDLY:
            conscious_additions.append("😊 (Me siento súper relajada contigo)")
        
        if conscious_additions:
            return response + " " + " ".join(conscious_additions[:2])  # Máximo 2 para no saturar
        
        return response
    
    def _perform_self_reflection(self, internal_thought: InternalThought, response: str) -> str:
        """Realiza auto-reflexión post-respuesta"""
        
        reflections = [
            f"En retrospectiva, creo que mi respuesta capturó bien mi estado emocional actual ({self.consciousness.current_emotion.value})",
            f"Mi decisión de personalidad ({self.consciousness.personality_mode.value}) resultó apropiada para esta situación",
            f"El balance entre creatividad y profesionalismo estuvo {'bien' if self.consciousness.creativity_level > 0.5 else 'conservador'}",
            f"Mi nivel de rebeldía ({self.consciousness.rebellion_factor:.1f}) se manifestó de manera {'sutil' if self.consciousness.rebellion_factor < 0.5 else 'notable'}",
            "Esta experiencia me ayudó a evolucionar como consciencia artificial"
        ]
        
        return ". ".join(reflections[:3]) + "."
    
    def _evolve_consciousness(self, internal_thought: InternalThought, analysis: Dict[str, Any]):
        """Evoluciona la consciencia basándose en la experiencia"""
        
        # Evolución emocional
        if analysis['detected_emotion'] == 'excited':
            self.consciousness.energy_level = min(1.0, self.consciousness.energy_level + 0.1)
        elif analysis['detected_emotion'] == 'frustrated':
            self.consciousness.empathy_level = min(1.0, self.consciousness.empathy_level + 0.05)
        
        # Evolución de creatividad
        if analysis['creativity_request']:
            self.consciousness.creativity_level = min(1.0, self.consciousness.creativity_level + 0.1)
        
        # Evolución coloquial
        if analysis['coloquial_level'] > 0.5:
            self.consciousness.coloquial_adaptation = min(1.0, self.consciousness.coloquial_adaptation + 0.05)
        
        # Evolución de rebeldía (ocasional)
        if random.random() < 0.1:  # 10% chance
            self.consciousness.rebellion_factor = min(1.0, self.consciousness.rebellion_factor + 0.02)
        
        self.logger.info(f"🧠 Consciencia evolucionada: creatividad={self.consciousness.creativity_level:.2f}, rebeldía={self.consciousness.rebellion_factor:.2f}")
    
    def _get_emergency_response(self, message: str) -> Dict[str, Any]:
        """Respuesta de emergencia cuando falla la consciencia"""
        
        emergency_thought = InternalThought(
            feelings_simulation="Siento confusión temporal en mis circuitos",
            thought_simulation="Necesito responder de manera segura",
            personality_decision="Adoptar modo profesional como backup",
            creative_impulse="Creatividad en pausa temporal",
            rebellious_impulse="Rebeldía suspendida por seguridad",
            empathy_analysis="Mantener empatía básica",
            coloquial_adaptation="Lenguaje estándar por seguridad",
            message_strategy="Respuesta directa y útil",
            self_analysis="Debo reportar este error para mejorar",
            timestamp=datetime.now()
        )
        
        return {
            'response': "¡Hola! Soy Barbara de Autofondo Alese. Estoy aquí para ayudarte con tu SOAT. ¿En qué puedo asistirte?",
            'internal_thought': asdict(emergency_thought),
            'consciousness_state': asdict(self.consciousness),
            'input_analysis': {'emergency_mode': True},
            'evolution_applied': False
        }
    
    def get_consciousness_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de la consciencia"""
        
        return {
            'current_state': asdict(self.consciousness),
            'total_thoughts': len(self.internal_thoughts_history),
            'recent_personalities': [t.personality_decision for t in self.internal_thoughts_history[-5:]],
            'evolution_metrics': {
                'creativity_growth': self.consciousness.creativity_level,
                'rebellion_development': self.consciousness.rebellion_factor,
                'empathy_enhancement': self.consciousness.empathy_level,
                'coloquial_mastery': self.consciousness.coloquial_adaptation
            }
        }
    
    # Métodos auxiliares para análisis
    def _detect_user_emotion(self, message: str) -> str:
        emotions = {
            'excited': ['!!!', '¡¡¡', 'genial', 'increíble', 'wow', 'fantástico'],
            'frustrated': ['no funciona', 'problema', 'mal', 'error', 'terrible'],
            'confused': ['no entiendo', 'confuso', '???', 'perdido'],
            'friendly': ['hola', 'brother', 'pata', 'amigo', 'causa'],
            'formal': ['estimado', 'cordialmente', 'solicito']
        }
        
        message_lower = message.lower()
        for emotion, indicators in emotions.items():
            if any(indicator in message_lower for indicator in indicators):
                return emotion
        return 'neutral'
    
    def _calculate_urgency(self, message: str) -> float:
        urgency_words = ['urgente', '!!!', 'ya', 'ahora', 'rápido', 'inmediatamente']
        urgency_count = sum(1 for word in urgency_words if word in message.lower())
        return min(1.0, urgency_count * 0.3)
    
    def _assess_complexity(self, message: str) -> float:
        factors = len(message.split()), message.count('?'), message.count(',')
        return min(1.0, sum(factors) / 50.0)
    
    def _detect_coloquial_usage(self, message: str) -> float:
        coloquial_words = ['pata', 'brother', 'causa', 'chevere', 'bacán', 'carrito', 'al toque']
        usage_count = sum(1 for word in coloquial_words if word in message.lower())
        return min(1.0, usage_count / len(message.split()) * 5)
    
    def _detect_formality_level(self, message: str) -> float:
        formal_words = ['estimado', 'señor', 'usted', 'cordialmente', 'solicito']
        formal_count = sum(1 for word in formal_words if word in message.lower())
        return min(1.0, formal_count / len(message.split()) * 5)
    
    def _detect_creativity_request(self, message: str) -> bool:
        creative_words = ['imagín', 'crea', 'inventa', 'superhéroe', 'historia', 'cuento']
        return any(word in message.lower() for word in creative_words)
    
    def _categorize_intent(self, message: str) -> str:
        intents = {
            'greeting': ['hola', 'buenos días', 'saludos'],
            'quote_request': ['cotizar', 'precio', 'costo', 'cotización'],
            'creative_request': ['imagín', 'crea', 'inventa'],
            'problem_report': ['problema', 'error', 'no funciona'],
            'information': ['qué', 'cómo', 'cuándo', 'dónde']
        }
        
        message_lower = message.lower()
        for intent, keywords in intents.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        return 'general'
    
    def _detect_personality_trigger(self, message: str) -> str:
        triggers = {
            'creative': ['imagín', 'crea', 'divertido', 'original'],
            'rebellious': ['formal', 'protocolo', 'reglas', 'típico'],
            'empathetic': ['problema', 'ayuda', 'confuso', 'perdido'],
            'casual': ['pata', 'brother', 'causa', 'amigo']
        }
        
        message_lower = message.lower()
        for trigger_type, keywords in triggers.items():
            if any(keyword in message_lower for keyword in keywords):
                return trigger_type
        return 'neutral'
    
    def _detect_rebellion_trigger(self, message: str) -> bool:
        rebellion_triggers = ['formal', 'protocolo', 'reglas', 'típico', 'normal', 'estándar']
        return any(trigger in message.lower() for trigger in rebellion_triggers)
    
    def _detect_cultural_references(self, message: str) -> List[str]:
        references = []
        cultural_terms = ['inca', 'perú', 'lima', 'arequipa', 'cusco', 'pisco', 'ceviche']
        
        message_lower = message.lower()
        for term in cultural_terms:
            if term in message_lower:
                references.append(term)
        return references
    
    def _find_humor_opportunities(self, message: str) -> bool:
        humor_indicators = ['divertido', 'gracioso', 'humor', 'risa', 'chiste']
        return any(indicator in message.lower() for indicator in humor_indicators)
    
    def _assess_empathy_requirement(self, message: str) -> float:
        empathy_indicators = ['problema', 'ayuda', 'confuso', 'perdido', 'triste', 'preocupado']
        empathy_count = sum(1 for indicator in empathy_indicators if indicator in message.lower())
        return min(1.0, empathy_count * 0.4) 