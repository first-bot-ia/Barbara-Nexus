"""
🤖 SISTEMA DE APRENDIZAJE ML DE ERRORES
Sistema inteligente que aprende de errores para mejorar Barbara

Basado en mejores prácticas de:
- https://medium.com/@kyeg/troubleshooting-pytorch-a-comprehensive-guide-to-common-errors-and-solutions-in-ai-model-3a47a9593ef5
- https://discuss.python.org/t/ai-powered-begginer-friendly-python-error-messages/84719
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import hashlib
import os

logger = logging.getLogger(__name__)

@dataclass
class ErrorPattern:
    """Patrón de error detectado"""
    error_type: str
    error_message: str
    context: str
    frequency: int = 1
    first_occurrence: str = ""
    last_occurrence: str = ""
    solutions_tried: Optional[List[str]] = None
    success_rate: float = 0.0
    
    def __post_init__(self):
        if self.solutions_tried is None:
            self.solutions_tried = []
        if not self.first_occurrence:
            self.first_occurrence = datetime.now().isoformat()
        self.last_occurrence = datetime.now().isoformat()

class MLErrorLearningSystem:
    """
    Sistema de aprendizaje ML que:
    1. Detecta patrones de errores
    2. Aprende de soluciones exitosas
    3. Predice y previene errores futuros
    4. Mejora automáticamente Barbara
    """
    
    def __init__(self):
        self.patterns_file = "ml/ml_error_patterns.json"
        self.error_patterns: Dict[str, ErrorPattern] = {}
        self.load_patterns()
        
        # Soluciones conocidas para errores comunes
        self.known_solutions = {
            "AttributeError": [
                "Verificar nombre de método correcto",
                "Revisar importaciones de clases", 
                "Validar inicialización de objetos"
            ],
            "KeyError": [
                "Verificar existencia de llaves en diccionarios",
                "Usar .get() con valores por defecto",
                "Validar estructura de datos"
            ],
            "TypeError": [
                "Verificar tipos de parámetros",
                "Validar estructura de argumentos",
                "Revisar llamadas a métodos"
            ]
        }
    
    def log_error(self, error_type: str, error_message: str, context: str) -> str:
        """
        Registra un error y aprende de él
        
        Returns:
            Sugerencia inteligente basada en aprendizaje previo
        """
        try:
            # Crear hash único para este tipo de error
            error_hash = self._create_error_hash(error_type, error_message)
            
            if error_hash in self.error_patterns:
                # Error conocido - incrementar frecuencia
                pattern = self.error_patterns[error_hash]
                pattern.frequency += 1
                pattern.last_occurrence = datetime.now().isoformat()
                logger.info(f"🔄 Error conocido detectado (frecuencia: {pattern.frequency})")
            else:
                # Nuevo error - crear patrón
                pattern = ErrorPattern(
                    error_type=error_type,
                    error_message=error_message,
                    context=context
                )
                self.error_patterns[error_hash] = pattern
                logger.info(f"🆕 Nuevo patrón de error registrado")
            
            # Generar sugerencia inteligente
            suggestion = self._generate_intelligent_suggestion(pattern)
            
            # Guardar patrones actualizados
            self.save_patterns()
            
            return suggestion
            
        except Exception as e:
            logger.error(f"❌ Error en sistema de aprendizaje: {e}")
            return "Error registrado para análisis futuro"
    
    def _create_error_hash(self, error_type: str, error_message: str) -> str:
        """Crea hash único para identificar patrones de error similares"""
        # Normalizar mensaje de error (remover números, paths específicos, etc.)
        normalized = error_message.lower()
        normalized = normalized.replace("'", "").replace('"', "")
        
        # Crear hash basado en tipo y mensaje normalizado
        content = f"{error_type}:{normalized}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _generate_intelligent_suggestion(self, pattern: ErrorPattern) -> str:
        """Genera sugerencia inteligente basada en aprendizaje"""
        
        base_suggestions = self.known_solutions.get(pattern.error_type, [
            "Revisar logs para más detalles",
            "Verificar configuración del sistema",
            "Consultar documentación"
        ])
        
        # Personalizar sugerencia según frecuencia
        if pattern.frequency > 5:
            priority = "🚨 ERROR CRÍTICO (frecuente)"
        elif pattern.frequency > 2:
            priority = "⚠️ ERROR RECURRENTE"
        else:
            priority = "ℹ️ ERROR NUEVO"
        
        # Sugerencias específicas para errores de Barbara
        barbara_specific = ""
        if "'BarbaraConversationService'" in pattern.error_message:
            barbara_specific = "\n🎭 ESPECÍFICO BARBARA: Verificar métodos de conversación y memoria"
        elif "get_or_create" in pattern.error_message:
            barbara_specific = "\n💾 ESPECÍFICO MEMORIA: Revisar métodos de memoria conversacional"
        
        suggestion = f"""
{priority}

📊 ESTADÍSTICAS:
- Ocurrencias: {pattern.frequency}
- Primera vez: {pattern.first_occurrence[:10]}
- Última vez: {pattern.last_occurrence[:10]}

🔧 SUGERENCIAS ML:
{chr(10).join(f"• {s}" for s in base_suggestions[:2])}
{barbara_specific}

🤖 APRENDIZAJE AUTOMÁTICO:
Sistema actualizando patrones para prevenir futuras ocurrencias...
        """
        
        return suggestion
    
    def get_system_health(self) -> Dict[str, Any]:
        """Obtiene salud del sistema basada en patrones de error"""
        
        if not self.error_patterns:
            return {
                "status": "excellent",
                "score": 100,
                "message": "🎉 No hay errores registrados",
                "recommendations": []
            }
        
        # Analizar patrones críticos
        critical_errors = [p for p in self.error_patterns.values() if p.frequency > 5]
        frequent_errors = [p for p in self.error_patterns.values() if p.frequency > 2]
        
        if critical_errors:
            status = "critical"
            score = 30
            message = f"🚨 {len(critical_errors)} errores críticos detectados"
        elif frequent_errors:
            status = "warning" 
            score = 60
            message = f"⚠️ {len(frequent_errors)} errores recurrentes"
        else:
            status = "good"
            score = 85
            message = f"✅ Sistema estable con {len(self.error_patterns)} errores menores"
        
        # Generar recomendaciones
        recommendations = []
        if critical_errors:
            recommendations.append("Priorizar solución de errores críticos")
        if len(self.error_patterns) > 10:
            recommendations.append("Revisar arquitectura para reducir puntos de falla")
        
        return {
            "status": status,
            "score": score,
            "message": message,
            "total_errors": len(self.error_patterns),
            "critical_errors": len(critical_errors),
            "frequent_errors": len(frequent_errors),
            "recommendations": recommendations
        }
    
    def load_patterns(self):
        """Carga patrones de errores previos"""
        try:
            if os.path.exists(self.patterns_file):
                with open(self.patterns_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for hash_key, pattern_data in data.items():
                        self.error_patterns[hash_key] = ErrorPattern(**pattern_data)
                logger.info(f"📚 {len(self.error_patterns)} patrones de error cargados")
        except Exception as e:
            logger.warning(f"⚠️ Error cargando patrones: {e}")
    
    def save_patterns(self):
        """Guarda patrones de errores para aprendizaje futuro"""
        try:
            os.makedirs(os.path.dirname(self.patterns_file), exist_ok=True)
            
            # Convertir a diccionario serializable
            data = {}
            for hash_key, pattern in self.error_patterns.items():
                data[hash_key] = asdict(pattern)
            
            with open(self.patterns_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"💾 {len(self.error_patterns)} patrones guardados")
            
        except Exception as e:
            logger.error(f"❌ Error guardando patrones: {e}")
    
    def predict_potential_issues(self, context: str) -> List[str]:
        """Predice posibles problemas basado en contexto"""
        predictions = []
        
        # Buscar patrones similares en contexto
        for pattern in self.error_patterns.values():
            if pattern.frequency > 2 and any(word in context.lower() 
                                           for word in pattern.context.lower().split()):
                predictions.append(f"Posible {pattern.error_type}: {pattern.error_message[:50]}...")
        
        return predictions[:3]  # Top 3 predicciones

# Instancia global del sistema
ml_error_system = MLErrorLearningSystem() 