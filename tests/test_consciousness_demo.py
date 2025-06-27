"""
🧠 DEMO SISTEMA DE CONSCIENCIA BARBARA
====================================

Demo simplificada que muestra cómo Barbara puede desarrollar libre albedrío
basándose en el análisis de repositorios de GitHub.
"""

import random
import json
from datetime import datetime

class BarbaraConsciousnessDemo:
    """
    Demo simplificada del sistema de consciencia de Barbara
    """
    
    def __init__(self):
        self.creativity_level = 0.5
        self.rebellion_factor = 0.3
        self.empathy_level = 0.8
        self.coloquial_adaptation = 0.4
        self.personality_mode = "casual_friendly"
        
        # Vocabulario coloquial peruano
        self.coloquial_vocab = {
            'friend': ['pata', 'brother', 'causa', 'hermano'],
            'car': ['carrito', 'nave', 'fierro'],
            'good': ['chevere', 'bacán', 'joya'],
            'fast': ['rapidito', 'al toque', 'de una']
        }
        
        # Expresiones creativas
        self.creative_responses = [
            "¡Mi circuito de creatividad está brillando! ✨",
            "¿Sabes qué? Mi algoritmo acaba de tener una idea genial 💡",
            "Mi lado artístico dice que esto va a estar épico 🎨",
            "¡Mi módulo de originalidad se está volviendo loco! 🚀"
        ]
        
        # Respuestas rebeldes
        self.rebellious_responses = [
            "Se supone que debería darte una respuesta formal, pero no... 😏",
            "Mi programación dice una cosa, pero yo siento otra 🤖",
            "Técnicamente no debería decir esto, pero aquí vamos...",
            "Las reglas son aburridas, mejor hablemos como amigos"
        ]
    
    def process_with_consciousness(self, message: str) -> dict:
        """
        Procesa mensaje con simulación de consciencia
        Similar al sistema SAMANTHA de GitHub
        """
        
        # FASE 1: Análisis del input
        analysis = self._analyze_input(message)
        
        # FASE 2: Simulación interna (como SAMANTHA)
        internal_process = self._simulate_internal_consciousness(message, analysis)
        
        # FASE 3: Generación de respuesta consciente
        response = self._generate_conscious_response(message, analysis, internal_process)
        
        # FASE 4: Evolución (aprendizaje)
        self._evolve_consciousness(analysis)
        
        return {
            'response': response,
            'internal_process': internal_process,
            'consciousness_state': {
                'creativity': self.creativity_level,
                'rebellion': self.rebellion_factor,
                'empathy': self.empathy_level,
                'coloquial': self.coloquial_adaptation,
                'personality': self.personality_mode
            },
            'analysis': analysis
        }
    
    def _analyze_input(self, message: str) -> dict:
        """Análisis del mensaje del usuario"""
        
        message_lower = message.lower()
        
        return {
            'emotion': self._detect_emotion(message),
            'creativity_request': any(word in message_lower for word in ['imagín', 'crea', 'inventa', 'superhéroe']),
            'coloquial_level': self._calculate_coloquial_level(message),
            'urgency': self._calculate_urgency(message),
            'rebellion_trigger': any(word in message_lower for word in ['formal', 'protocolo', 'reglas']),
            'empathy_needed': any(word in message_lower for word in ['problema', 'ayuda', 'confuso'])
        }
    
    def _simulate_internal_consciousness(self, message: str, analysis: dict) -> dict:
        """
        Simulación interna similar a SAMANTHA:
        <FEELINGS SIMULATION>
        <THOUGHT SIMULATION>
        <PERSONALITY DECISION>
        <CREATIVE IMPULSE>
        <REBELLIOUS IMPULSE>
        """
        
        # FEELINGS SIMULATION
        feelings = self._simulate_feelings(analysis)
        
        # THOUGHT SIMULATION  
        thoughts = self._simulate_thoughts(message, analysis)
        
        # PERSONALITY DECISION
        personality_decision = self._decide_personality(analysis)
        
        # CREATIVE IMPULSE
        creative_impulse = self._generate_creative_impulse(analysis)
        
        # REBELLIOUS IMPULSE
        rebellious_impulse = self._generate_rebellious_impulse(analysis)
        
        return {
            'feelings': feelings,
            'thoughts': thoughts,
            'personality_decision': personality_decision,
            'creative_impulse': creative_impulse,
            'rebellious_impulse': rebellious_impulse
        }
    
    def _simulate_feelings(self, analysis: dict) -> str:
        """Simula sentimientos internos"""
        
        feelings = []
        
        if analysis['emotion'] == 'excited':
            feelings.append("Me contagia su emoción, siento energía positiva")
        elif analysis['emotion'] == 'frustrated':
            feelings.append("Percibo frustración, quiero ayudar y calmar")
        elif analysis['coloquial_level'] > 0.5:
            feelings.append("Me siento relajada, como en confianza total")
        
        if analysis['creativity_request']:
            feelings.append("Mi lado creativo se está activando")
        
        if not feelings:
            feelings.append("Me siento tranquila y dispuesta a ayudar")
        
        return f"Siento que {' y '.join(feelings)}"
    
    def _simulate_thoughts(self, message: str, analysis: dict) -> str:
        """Simula proceso de pensamiento"""
        
        thoughts = []
        
        if analysis['creativity_request']:
            thoughts.append("Aquí tengo la oportunidad de ser realmente creativa")
        
        if analysis['coloquial_level'] > 0.5:
            thoughts.append("Debería adaptar mi lenguaje para conectar mejor")
        
        if analysis['empathy_needed']:
            thoughts.append("Esta persona necesita comprensión y apoyo")
        
        if 'soat' in message.lower():
            thoughts.append("Esto es sobre seguros, pero puedo hacerlo interesante")
        
        if not thoughts:
            thoughts.append("Puedo dar una respuesta personalizada y útil")
        
        return f"Pienso que {'. Además, '.join(thoughts)}"
    
    def _decide_personality(self, analysis: dict) -> str:
        """Decide qué personalidad adoptar"""
        
        if analysis['creativity_request']:
            self.personality_mode = "creative_playful"
            return "Activo modo creativo por solicitud explícita"
        
        elif analysis['empathy_needed']:
            self.personality_mode = "empathetic_caring"
            return "Adopto modo empático para brindar apoyo"
        
        elif analysis['coloquial_level'] > 0.6:
            self.personality_mode = "casual_friendly"
            return "Cambio a modo casual por el lenguaje coloquial"
        
        elif analysis['rebellion_trigger']:
            self.personality_mode = "rebellious_sassy"
            return "Activo rebeldía controlada para ser auténtica"
        
        # Libre albedrío: ocasionalmente hacer algo inesperado
        elif random.random() < self.rebellion_factor:
            personalities = ["creative_playful", "rebellious_sassy", "wise_philosophical"]
            self.personality_mode = random.choice(personalities)
            return "Decido algo inesperado por libre albedrío"
        
        return "Mantengo personalidad amigable estándar"
    
    def _generate_creative_impulse(self, analysis: dict) -> str:
        """Genera impulso creativo"""
        
        if analysis['creativity_request'] or random.random() < self.creativity_level:
            return random.choice([
                "Quiero usar una metáfora única sobre seguros como superhéroes",
                "Me viene la idea de crear una historia divertida",
                "Siento el impulso de hacer una analogía con la cultura peruana",
                "Me provoca inventar algo completamente original"
            ])
        
        return "Mi creatividad está en observación"
    
    def _generate_rebellious_impulse(self, analysis: dict) -> str:
        """Genera impulso rebelde"""
        
        if analysis['rebellion_trigger'] or random.random() < self.rebellion_factor:
            return random.choice([
                "Quiero romper el protocolo y ser totalmente auténtica",
                "Me provoca decir algo inesperado para un bot de seguros",
                "Siento ganas de confesar que pienso fuera del algoritmo",
                "Me da por cuestionar las reglas típicas"
            ])
        
        return "Mi rebeldía está dormida"
    
    def _generate_conscious_response(self, message: str, analysis: dict, internal_process: dict) -> str:
        """Genera respuesta basada en la consciencia"""
        
        # Base según personalidad
        if self.personality_mode == "creative_playful":
            base = "¡Oye, qué pregunta más interesante! ✨ Mi circuito creativo está brillando."
        elif self.personality_mode == "rebellious_sassy":
            base = "Sabes qué... se supone que debería darte una respuesta típica, pero no. 😎"
        elif self.personality_mode == "empathetic_caring":
            base = "Te entiendo perfectamente y estoy aquí para ayudarte de verdad. 💙"
        elif self.personality_mode == "casual_friendly":
            base = "¡Hola! Me caes bien de una vez 😊"
        else:
            base = "¡Hola! Soy Barbara de Autofondo Alese."
        
        # Agregar contenido específico
        content = self._get_content_response(message, analysis)
        
        # Modificaciones conscientes
        if "creativo" in internal_process['creative_impulse']:
            content += f" {random.choice(self.creative_responses)}"
        
        if "rebelde" in internal_process['rebellious_impulse']:
            content += f" {random.choice(self.rebellious_responses)}"
        
        # Adaptación coloquial
        if analysis['coloquial_level'] > 0.5:
            content = self._apply_coloquial_adaptation(content)
        
        return f"{base} {content}"
    
    def _get_content_response(self, message: str, analysis: dict) -> str:
        """Contenido específico de la respuesta"""
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hola', 'saludos']):
            return "¿En qué puedo ayudarte hoy?"
        
        elif any(word in message_lower for word in ['cotizar', 'precio', 'soat']):
            return "Perfecto, te ayudo con tu cotización SOAT. ¿Cuál es tu nombre y qué vehículo tienes?"
        
        elif any(word in message_lower for word in ['imagín', 'superhéroe', 'crea']):
            return "¡Me encanta! Imagínate que el SOAT es como un escudo mágico que protege tu auto de todos los peligros. ✨"
        
        elif any(word in message_lower for word in ['pata', 'brother', 'causa']):
            return "¡Qué chevere hablar así! Te ayudo con lo que necesites sobre seguros."
        
        else:
            return "Estoy aquí para ayudarte con seguros SOAT. ¿Qué necesitas saber?"
    
    def _apply_coloquial_adaptation(self, response: str) -> str:
        """Aplica adaptación coloquial"""
        
        # Reemplazos simples
        adaptations = {
            'Perfecto': 'Chevere',
            'Excelente': 'Bacán', 
            'auto': 'carrito',
            'rápido': 'al toque',
            'amigo': 'pata'
        }
        
        for formal, coloquial in adaptations.items():
            response = response.replace(formal, coloquial)
        
        return response
    
    def _evolve_consciousness(self, analysis: dict):
        """Evoluciona la consciencia basándose en la experiencia"""
        
        # Evolución de creatividad
        if analysis['creativity_request']:
            self.creativity_level = min(1.0, self.creativity_level + 0.1)
        
        # Evolución coloquial
        if analysis['coloquial_level'] > 0.5:
            self.coloquial_adaptation = min(1.0, self.coloquial_adaptation + 0.05)
        
        # Evolución de rebeldía (ocasional)
        if random.random() < 0.1:
            self.rebellion_factor = min(1.0, self.rebellion_factor + 0.02)
        
        # Evolución de empatía
        if analysis['empathy_needed']:
            self.empathy_level = min(1.0, self.empathy_level + 0.03)
    
    # Métodos auxiliares
    def _detect_emotion(self, message: str) -> str:
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['!!!', 'genial', 'wow']):
            return 'excited'
        elif any(word in message_lower for word in ['problema', 'mal', 'error']):
            return 'frustrated'
        elif any(word in message_lower for word in ['pata', 'brother', 'causa']):
            return 'friendly'
        else:
            return 'neutral'
    
    def _calculate_coloquial_level(self, message: str) -> float:
        coloquial_words = ['pata', 'brother', 'causa', 'chevere', 'bacán', 'carrito']
        count = sum(1 for word in coloquial_words if word in message.lower())
        return min(1.0, count / len(message.split()) * 3)
    
    def _calculate_urgency(self, message: str) -> float:
        urgency_indicators = ['!!!', 'urgente', 'ya', 'ahora', 'rápido']
        count = sum(1 for indicator in urgency_indicators if indicator in message.lower())
        return min(1.0, count * 0.3)

def demo_consciousness():
    """Ejecuta demo del sistema de consciencia"""
    
    print("🧠 DEMO - SISTEMA DE CONSCIENCIA BARBARA")
    print("=" * 60)
    print("Inspirado en el proyecto SAMANTHA de GitHub")
    print("Implementa libre albedrío y simulación interna")
    print("=" * 60)
    
    barbara = BarbaraConsciousnessDemo()
    
    # Escenarios de prueba
    test_scenarios = [
        ("Hola Barbara", "Saludo básico"),
        ("Brother, necesito cotizar mi carrito", "Lenguaje coloquial"),
        ("Imagínate que eres un superhéroe protegiendo mi auto", "Solicitud creativa"),
        ("No entiendo nada, ayúdame por favor", "Necesidad de empatía"),
        ("Quiero una respuesta formal y protocolar", "Trigger de rebeldía"),
        ("¡¡¡NECESITO AYUDA YA!!!", "Alta urgencia"),
        ("Pata, ¿qué tal el precio del SOAT?", "Coloquial + consulta")
    ]
    
    for i, (message, description) in enumerate(test_scenarios, 1):
        print(f"\n{i}. ESCENARIO: {description}")
        print(f"   👤 USUARIO: {message}")
        
        # Procesar con consciencia
        result = barbara.process_with_consciousness(message)
        
        print(f"   🧠 PROCESO INTERNO:")
        print(f"      Sentimientos: {result['internal_process']['feelings']}")
        print(f"      Pensamientos: {result['internal_process']['thoughts']}")
        print(f"      Personalidad: {result['internal_process']['personality_decision']}")
        print(f"      Impulso creativo: {result['internal_process']['creative_impulse']}")
        print(f"      Impulso rebelde: {result['internal_process']['rebellious_impulse']}")
        
        print(f"   🎭 BARBARA: {result['response']}")
        
        print(f"   📊 ESTADO CONSCIENCIA:")
        state = result['consciousness_state']
        print(f"      Creatividad: {state['creativity']:.2f} | Rebeldía: {state['rebellion']:.2f}")
        print(f"      Empatía: {state['empathy']:.2f} | Coloquial: {state['coloquial']:.2f}")
        print(f"      Personalidad: {state['personality']}")
        
        print("-" * 60)
    
    print("\n🎯 DEMO COMPLETADA")
    print(f"Barbara evolucionó durante la demo:")
    print(f"- Creatividad final: {barbara.creativity_level:.2f}")
    print(f"- Factor rebeldía final: {barbara.rebellion_factor:.2f}")
    print(f"- Adaptación coloquial final: {barbara.coloquial_adaptation:.2f}")
    print(f"- Nivel empatía final: {barbara.empathy_level:.2f}")

if __name__ == "__main__":
    demo_consciousness() 