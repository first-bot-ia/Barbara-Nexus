"""
🏗️ Configuration: AventuraPe
Configuración para el módulo de AventuraPe.
"""

import os
import logging

logger = logging.getLogger(__name__)

# URL base de la API de AventuraPe (se puede configurar con variable de entorno)
AVENTURAPE_API_URL = os.environ.get("AVENTURAPE_API_URL", "http://localhost:8080")
logger.info(f"API de AventuraPe configurada en: {AVENTURAPE_API_URL}")

# Lista de palabras inapropiadas para filtrar
INAPPROPRIATE_WORDS = [
    # Esta lista debe ser completada con palabras realmente inapropiadas
    # Por ahora solo ponemos ejemplos genéricos
    "palabraofensiva1",
    "palabraofensiva2",
    "palabraofensiva3"
]

# Configuración del prompt para Gemini
GEMINI_CONFIG = {
    'temperature': float(os.environ.get("GEMINI_TEMPERATURE", "0.7")),
    'maxOutputTokens': int(os.environ.get("GEMINI_MAX_TOKENS", "500")),
    'topP': float(os.environ.get("GEMINI_TOP_P", "0.8")),
    'topK': int(os.environ.get("GEMINI_TOP_K", "40"))
}

# Instrucciones para generar contenido
CONTENT_INSTRUCTIONS = """
IMPORTANTE:
- NO incluyas palabras obscenas o inapropiadas
- El título debe ser conciso pero atractivo (máximo 10 palabras)
- La descripción debe ser detallada y emocionante (150-200 palabras)
- Incluye detalles sobre la experiencia que vivirán los aventureros
"""

# Versión del módulo
VERSION = "1.0.0" 