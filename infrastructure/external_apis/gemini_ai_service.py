"""
🏗️ Infrastructure Service: Gemini AI Service
Siguiendo principios de Domain-Driven Design (DDD)
"""

from typing import Optional, Dict, Any
import requests
import logging
import time

logger = logging.getLogger(__name__)

class GeminiAIService:
    """
    Infrastructure Service: Servicio para interactuar con Gemini AI
    
    Siguiendo DDD: Los servicios de infraestructura manejan 
    comunicación con sistemas externos
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.timeout = 15
        self.max_retries = 3
        
        # Configuración optimizada para Barbara
        self.default_config = {
            'temperature': 0.4,  # Consistencia conversacional
            'topK': 20,
            'topP': 0.8,
            'maxOutputTokens': 120  # Respuestas cortas
        }
    
    def generate_response(self, 
                         message: str, 
                         conversation_context: str,
                         config: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Genera respuesta usando Gemini AI
        
        Args:
            message: Mensaje del usuario
            conversation_context: Contexto conversacional completo
            config: Configuración personalizada (opcional)
            
        Returns:
            Respuesta generada o None si falla
        """
        
        try:
            # Preparar configuración
            generation_config = {**self.default_config}
            if config:
                generation_config.update(config)
            
            # Construir prompt optimizado para Barbara
            prompt = self._build_barbara_prompt(message, conversation_context)
            
            # Hacer petición con reintentos
            for attempt in range(self.max_retries):
                try:
                    response = self._make_api_request(prompt, generation_config)
                    if response:
                        logger.info(f"✅ Gemini respuesta generada (intento {attempt + 1})")
                        return response
                except Exception as e:
                    logger.warning(f"⚠️ Gemini intento {attempt + 1} falló: {e}")
                    if attempt < self.max_retries - 1:
                        time.sleep(1)  # Esperar antes del reintento
            
            logger.error("❌ Gemini falló después de todos los reintentos")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error inesperado en Gemini: {e}")
            return None
    
    def _build_barbara_prompt(self, message: str, context: str) -> str:
        """Construye prompt optimizado para Barbara"""
        return f"""{context}

INSTRUCCIONES CRÍTICAS PARA BARBARA:

⚠️ NUNCA repitas las palabras del cliente como si fueran tuyas
⚠️ NUNCA incluyas frases como "Quiero Cotizar" en tu respuesta
⚠️ Solo responde como Barbara, no como el cliente

PERSONALIDAD:
- Eres Barbara, persona real que trabaja en Autofondo Alese
- Habla natural y humano, NO como robot
- USA el historial para NO repetir información
- Si ya tienes el nombre, NO lo pidas otra vez
- Mantén flujo natural sin redundancias
- NUNCA te presentes dos veces
- Máximo 2 líneas de respuesta

REGLAS DE ORO:
1. Lee el contexto conversacional
2. Identifica qué dijo el CLIENTE vs qué dijo BARBARA
3. Responde SOLO como Barbara
4. NO repitas palabras del cliente

MENSAJE ACTUAL DEL CLIENTE: {message}

RESPUESTA DE BARBARA (máximo 2 líneas, sin repetir palabras del cliente):"""
    
    def _make_api_request(self, prompt: str, config: Dict[str, Any]) -> Optional[str]:
        """Hace la petición real a la API de Gemini"""
        
        url = f"{self.base_url}?key={self.api_key}"
        
        headers = {"Content-Type": "application/json"}
        
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": config
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']['parts'][0]['text'].strip()
                return self._clean_response(content)
        
        # Log del error para debugging
        logger.error(f"❌ Gemini API error: {response.status_code} - {response.text}")
        raise Exception(f"Gemini API error: {response.status_code}")
    
    def _clean_response(self, response: str) -> str:
        """Limpia la respuesta de Gemini"""
        # Remover prefijos comunes
        prefixes_to_remove = [
            "RESPUESTA DE BARBARA:",
            "Barbara:",
            "Respuesta:",
            "RESPUESTA:"
        ]
        
        cleaned = response
        for prefix in prefixes_to_remove:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
        
        # Remover asteriscos de markdown si están solos
        cleaned = cleaned.replace("**", "").replace("*", "")
        
        return cleaned
    
    def health_check(self) -> bool:
        """Verifica si el servicio está funcionando"""
        try:
            test_response = self.generate_response(
                message="test",
                conversation_context="Test de conectividad",
                config={'maxOutputTokens': 10}
            )
            return test_response is not None
        except Exception:
            return False
    
    def get_service_info(self) -> Dict[str, Any]:
        """Obtiene información del servicio"""
        return {
            'service': 'Gemini AI',
            'model': 'gemini-1.5-flash',
            'status': 'active' if self.health_check() else 'error',
            'config': self.default_config,
            'timeout': self.timeout,
            'max_retries': self.max_retries
        } 