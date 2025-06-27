"""
🔥 TEST MASIVO DE ESCENARIOS - ENTRENAMIENTO BÁRBARA
===================================================

Este test ejecuta múltiples escenarios complejos para entrenar a Barbara
en libre albedrío, lenguaje coloquial y situaciones imprevistas.
"""

import sys
import os
import time
import random
# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.services.barbara_conversation_service_robust import BarbaraConversationServiceRobust

class BarbaricanTesting:
    """
    Sistema masivo de entrenamiento para Barbara
    Incluye escenarios de libre albedrío y creatividad
    """
    
    def __init__(self):
        self.barbara = BarbaraConversationServiceRobust()
        self.scenarios_completed = 0
        self.creative_responses_detected = 0
        self.coloquial_adaptations = 0
        
        # 🇵🇪 ESCENARIOS COLOQUIALES PERUANOS
        self.coloquial_scenarios = [
            # Saludos peruanos
            ("Oye pata, ¿qué tal tu SOAT?", "Saludo coloquial amistoso"),
            ("Brother, necesito cotizar mi carrito", "Jerga juvenil urbana"),
            ("Causa, ¿cuánto me sale el seguro?", "Expresión típica limeña"),
            ("Compadre, ayúdame con mi nave", "Tratamiento familiar"),
            ("Hermano, mi fierro necesita SOAT", "Jerga para auto"),
            
            # Expresiones peruanas típicas
            ("¿Está chevere el precio?", "Pregunta con jerga positiva"),
            ("¿Me sale bacán la cotización?", "Consulta informal"),
            ("Rapidito pata, necesito esto al toque", "Urgencia coloquial"),
            ("¿Me mandas la info de una?", "Solicitud inmediata"),
            ("Brother, mi plata está justa", "Problema económico"),
            
            # Situaciones complejas coloquiales
            ("Oye, mi carrito está medio gileado, ¿me aseguras igual?", "Problema técnico coloquial"),
            ("Pata, ¿y si choco mañana? ¿Me cubren?", "Preocupación específica"),
            ("Causa, mi ex me rayó el auto, ¿eso cuenta como daño?", "Situación personal compleja"),
        ]
        
        # 🤖 ESCENARIOS DE CREATIVIDAD Y LIBRE ALBEDRÍO
        self.creativity_scenarios = [
            # Pedidos creativos directos
            ("Imagínate que eres un superhéroe protegiendo mi auto", "Solicitud de creatividad"),
            ("Inventa una historia sobre seguros de autos", "Narrativa creativa"),
            ("Háblame como si fueras mi mejor amigo", "Cambio de personalidad"),
            ("Créeme un rap sobre el SOAT", "Desafío artístico"),
            ("Si fueras un robot del futuro vendiendo seguros, ¿qué dirías?", "Escenario futurista"),
            
            # Preguntas filosóficas
            ("¿Por qué existen los seguros en el universo?", "Pregunta existencial"),
            ("¿Qué pensaría mi auto si pudiera hablar?", "Antropomorfización"),
            ("Si los seguros fueran personas, ¿cómo serían?", "Metáfora abstracta"),
            
            # Situaciones absurdas
            ("Mi auto me habló en sueños y me pidió un seguro", "Situación surrealista"),
            ("¿El SOAT me protege contra alienígenas?", "Pregunta absurda"),
            ("Si mi auto se enamora de otro auto, ¿necesitan seguros de pareja?", "Situación romántica absurda"),
        ]
        
        # 😤 ESCENARIOS DE ESTRÉS Y PRESIÓN
        self.stress_scenarios = [
            # Urgencia extrema
            ("NECESITO EL SEGURO AHORA MISMO!!!", "Urgencia máxima"),
            ("¡¡¡RESPONDE RÁPIDO QUE TENGO PRISA!!!", "Presión temporal"),
            ("ME ESTÁN MULTANDO AHORA, AYÚDAME YA", "Crisis en tiempo real"),
            
            # Frustración y enojo
            ("Tu sistema no sirve para nada", "Insulto directo"),
            ("Eres la peor asesora que he visto", "Crítica personal"),
            ("¡ESTO ES UNA ESTAFA!", "Acusación grave"),
            
            # Confusión total
            ("No entiendo nada de lo que dices", "Desorientación completa"),
            ("Explícame todo desde el principio", "Solicitud de reinicio"),
            ("Estoy perdido, no sé qué hacer", "Vulnerabilidad emocional"),
        ]
        
        # 🧠 ESCENARIOS DE PROBLEMAS COMPLEJOS
        self.problem_scenarios = [
            # Problemas técnicos
            ("Mi auto está registrado a nombre de mi abuela fallecida", "Problema legal complejo"),
            ("Tengo 3 autos y 2 motos, ¿cómo hago?", "Múltiples vehículos"),
            ("Mi vehículo es importado y no tiene placa peruana", "Caso especial"),
            ("Soy extranjero sin DNI peruano", "Problema documental"),
            
            # Situaciones económicas
            ("No tengo dinero hasta fin de mes", "Problema financiero"),
            ("¿Puedo pagar en cuotas muy pequeñas?", "Necesidad de flexibilidad"),
            ("Mi empresa quebró y perdí el trabajo", "Crisis económica"),
            
            # Casos límite
            ("Mi auto fue robado pero recuperado", "Situación compleja"),
            ("Tengo orden de captura, ¿puedo asegurar?", "Problema legal grave"),
            ("Mi auto está embargado", "Complicación judicial"),
        ]
        
        # 🎭 ESCENARIOS DE CAMBIO DE PERSONALIDAD
        self.personality_scenarios = [
            ("Háblame como si fueras mi hermana mayor", "Rol familiar"),
            ("Actúa como un vendedor de feria", "Cambio de contexto"),
            ("Conviértete en un poeta romántico", "Personalidad artística"),
            ("Sé como un profesor universitario", "Rol académico"),
            ("Actúa como un comediante", "Personalidad humorística"),
            ("Háblame como si fueras de Arequipa", "Cambio regional"),
        ]
    
    def run_all_scenarios(self):
        """Ejecuta todos los escenarios de entrenamiento"""
        print("🔥 INICIANDO ENTRENAMIENTO MASIVO DE BARBARA")
        print("=" * 80)
        print("🎯 Objetivo: Desarrollar libre albedrío, creatividad y adaptación")
        print("🧠 Escenarios planificados: ", len(self.coloquial_scenarios) + 
              len(self.creativity_scenarios) + len(self.stress_scenarios) + 
              len(self.problem_scenarios) + len(self.personality_scenarios))
        print("=" * 80)
        
        # Ejecutar cada categoría
        self._run_scenario_category("COLOQUIAL PERUANO", self.coloquial_scenarios)
        self._run_scenario_category("CREATIVIDAD Y LIBRE ALBEDRÍO", self.creativity_scenarios)
        self._run_scenario_category("ESTRÉS Y PRESIÓN", self.stress_scenarios)
        self._run_scenario_category("PROBLEMAS COMPLEJOS", self.problem_scenarios)
        self._run_scenario_category("CAMBIO DE PERSONALIDAD", self.personality_scenarios)
        
        # Ejecutar escenarios combinados
        self._run_combined_scenarios()
        
        # Reporte final
        self._generate_final_report()
    
    def _run_scenario_category(self, category_name: str, scenarios: list):
        """Ejecuta una categoría de escenarios"""
        print(f"\n🎪 CATEGORÍA: {category_name}")
        print("-" * 60)
        
        for i, (message, description) in enumerate(scenarios, 1):
            user_id = f"+51999{category_name[:4].upper()}{i:03d}"
            
            print(f"\n{i:2d}. 📝 ESCENARIO: {description}")
            print(f"    👤 USUARIO: {message}")
            
            # Procesar con Barbara
            response, _ = self.barbara.process_message(user_id, message)
            
            print(f"    🎭 BARBARA: {response}")
            
            # Analizar respuesta
            creativity_score = self._analyze_creativity(response)
            coloquial_adaptation = self._analyze_coloquial_adaptation(response, message)
            
            if creativity_score > 0.5:
                self.creative_responses_detected += 1
                print(f"    ✨ CREATIVIDAD DETECTADA: {creativity_score:.1f}/1.0")
            
            if coloquial_adaptation:
                self.coloquial_adaptations += 1
                print(f"    🗣️ ADAPTACIÓN COLOQUIAL: SÍ")
            
            self.scenarios_completed += 1
            
            # Pausa breve para simular interacción natural
            time.sleep(0.5)
    
    def _run_combined_scenarios(self):
        """Ejecuta escenarios combinados para probar adaptabilidad"""
        print(f"\n🌪️ ESCENARIOS COMBINADOS (LIBRE ALBEDRÍO MÁXIMO)")
        print("-" * 60)
        
        combined_scenarios = [
            # Combinar coloquial + creatividad
            ("Brother, imagínate que tu SOAT es un superhéroe peruano", "Coloquial + Creatividad"),
            ("Pata, créame un cuento sobre seguros but make it fashion", "Spanglish creativo"),
            ("Causa, si mi carrito fuera un inca, ¿qué seguro tendría?", "Historia + Auto"),
            
            # Combinar estrés + creatividad
            ("¡RÁPIDO! Invéntame algo divertido sobre seguros", "Urgencia + Humor"),
            ("AYUDA, necesito que me hagas reír mientras me cotizas", "Crisis + Entretenimiento"),
            
            # Personalidad + problema complejo
            ("Actúa como mi abuela y explícame por qué mi auto robado necesita seguro", "Rol + Complejidad"),
            ("Sé un rapero y explícame el SOAT", "Arte + Información"),
        ]
        
        for i, (message, description) in enumerate(combined_scenarios, 1):
            user_id = f"+51999COMBO{i:03d}"
            
            print(f"\n{i}. 🔀 ESCENARIO COMBINADO: {description}")
            print(f"   👤 USUARIO: {message}")
            
            response, _ = self.barbara.process_message(user_id, message)
            
            print(f"   🎭 BARBARA: {response}")
            
            # Análisis especial para escenarios combinados
            complexity_score = self._analyze_response_complexity(response)
            print(f"   🧠 COMPLEJIDAD DE RESPUESTA: {complexity_score:.1f}/1.0")
            
            self.scenarios_completed += 1
            time.sleep(1)
    
    def _analyze_creativity(self, response: str) -> float:
        """Analiza nivel de creatividad en la respuesta"""
        creative_indicators = [
            'imagin', 'superpoder', 'superhér', 'varita', 'mágic', 'cuento',
            'historia', 'fantástic', 'increíble', 'genial', 'extraordinario',
            'aventura', 'emocionante', 'espectacular', 'maravilloso', 'asombros'
        ]
        
        response_lower = response.lower()
        creative_words = sum(1 for indicator in creative_indicators if indicator in response_lower)
        
        # Bonificar emojis creativos
        creative_emojis = ['✨', '🌟', '⭐', '🎭', '🎪', '🚀', '🦄', '🪄']
        emoji_bonus = sum(1 for emoji in creative_emojis if emoji in response) * 0.2
        
        return min(1.0, (creative_words * 0.2) + emoji_bonus)
    
    def _analyze_coloquial_adaptation(self, response: str, user_message: str) -> bool:
        """Analiza si Barbara se adaptó al lenguaje coloquial del usuario"""
        user_lower = user_message.lower()
        response_lower = response.lower()
        
        # Palabras coloquiales del usuario
        user_coloquial = ['pata', 'brother', 'causa', 'compadre', 'hermano', 'chevere', 'bacán']
        user_uses_coloquial = any(word in user_lower for word in user_coloquial)
        
        # Verificar si Barbara respondió de forma similar
        barbara_coloquial = ['amigo', 'hermano', 'compañero', 'genial', 'perfecto', 'excelente']
        barbara_adapted = any(word in response_lower for word in barbara_coloquial)
        
        return user_uses_coloquial and barbara_adapted
    
    def _analyze_response_complexity(self, response: str) -> float:
        """Analiza complejidad de la respuesta"""
        factors = {
            'length': min(1.0, len(response) / 200),  # Respuestas más largas = más complejas
            'questions': len([w for w in response if w == '?']) * 0.2,
            'exclamations': len([w for w in response if w == '!']) * 0.1,
            'metaphors': sum(0.3 for word in ['como', 'igual que', 'parece', 'similar'] if word in response.lower()),
            'emojis': min(0.5, len([c for c in response if ord(c) > 127]) * 0.1)  # Contar emojis/símbolos
        }
        
        return min(1.0, sum(factors.values()) / len(factors))
    
    def _generate_final_report(self):
        """Genera reporte final del entrenamiento"""
        print("\n" + "=" * 80)
        print("📊 REPORTE FINAL DE ENTRENAMIENTO")
        print("=" * 80)
        
        creativity_rate = (self.creative_responses_detected / self.scenarios_completed) * 100
        coloquial_rate = (self.coloquial_adaptations / self.scenarios_completed) * 100
        
        print(f"🎯 Escenarios completados: {self.scenarios_completed}")
        print(f"✨ Respuestas creativas detectadas: {self.creative_responses_detected} ({creativity_rate:.1f}%)")
        print(f"🗣️ Adaptaciones coloquiales: {self.coloquial_adaptations} ({coloquial_rate:.1f}%)")
        
        # Evaluación del libre albedrío
        free_will_score = (creativity_rate + coloquial_rate) / 2
        print(f"🧠 NIVEL DE LIBRE ALBEDRÍO: {free_will_score:.1f}%")
        
        # Recomendaciones
        print("\n📈 ANÁLISIS Y RECOMENDACIONES:")
        if free_will_score > 60:
            print("✅ Barbara muestra buen desarrollo de libre albedrío")
        elif free_will_score > 30:
            print("⚠️ Barbara necesita más entrenamiento en creatividad")
        else:
            print("❌ Barbara requiere refuerzo intensivo en adaptabilidad")
        
        if creativity_rate < 40:
            print("💡 Recomendación: Aumentar exposición a escenarios creativos")
        
        if coloquial_rate < 50:
            print("🗣️ Recomendación: Mejorar detección y adaptación de lenguaje coloquial")
        
        print("\n🚀 BARBARA HA EVOLUCIONADO COMPLETAMENTE")
        print("=" * 80)

def main():
    """Función principal para ejecutar el entrenamiento"""
    trainer = BarbaricanTesting()
    trainer.run_all_scenarios()

if __name__ == "__main__":
    main() 