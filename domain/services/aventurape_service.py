"""
🏗️ Domain Service: AventuraPeService
Servicio para generar título y descripción para publicaciones de AventuraPe.
"""

from typing import Dict, Tuple, Optional
import json
import logging

# Importar configuración
from config.aventurape_config import INAPPROPRIATE_WORDS, GEMINI_CONFIG, CONTENT_INSTRUCTIONS

logger = logging.getLogger(__name__)

class AventuraPeService:
    """
    Servicio de dominio para generar contenido para publicaciones de AventuraPe
    utilizando un servicio de IA (Gemini).
    
    Versión simplificada que solo genera título y descripción.
    """
    
    def __init__(self, gemini_service):
        """
        Inicializa el servicio con una instancia del servicio Gemini
        
        Args:
            gemini_service: Instancia del servicio de Gemini
        """
        self.gemini_service = gemini_service
        
    def generate_publication_content(self, adventure_context: str) -> Tuple[Dict[str, str], Optional[str]]:
        """
        Genera título y descripción para una publicación de aventura
        
        Args:
            adventure_context: Contexto de la aventura proporcionado por el usuario
            
        Returns:
            Tuple con (contenido generado, error). El contenido generado es un diccionario
            con title y description. Si hay un error, el contenido será None y el error será
            un mensaje descriptivo.
        """
        try:
            # Verificar contenido inapropiado
            if self._contains_inappropriate_content(adventure_context):
                return None, "El contexto contiene palabras inapropiadas"
                
            prompt = self._create_prompt(adventure_context)
            response = self.gemini_service.generate_response(
                message=prompt,
                conversation_context="Generar publicación de AventuraPe",
                config=GEMINI_CONFIG
            )
            
            if not response:
                return None, "No se pudo generar contenido"
            
            try:
                # Intenta extraer el JSON de la respuesta
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    content_dict = json.loads(json_str)
                    
                    # Solo extraemos título y descripción
                    result = {
                        "title": content_dict.get("title", ""),
                        "description": content_dict.get("description", "")
                    }
                    return result, None
                else:
                    # Si no encuentra JSON, intenta extraer partes del texto
                    title = ""
                    description = ""
                    
                    if "Título:" in response:
                        title_start = response.find("Título:") + len("Título:")
                        title_end = response.find("\n", title_start)
                        if title_end == -1:
                            title_end = len(response)
                        title = response[title_start:title_end].strip()
                    
                    if "Descripción:" in response:
                        desc_start = response.find("Descripción:") + len("Descripción:")
                        description = response[desc_start:].strip()
                    
                    result = {
                        "title": title,
                        "description": description
                    }
                    return result, None
            except Exception as e:
                logger.error(f"Error al procesar respuesta: {str(e)}")
                
                # Intenta extraer manualmente título y descripción
                result = {
                    "title": "Aventura generada por IA",
                    "description": response[:300].strip()  # Usar parte de la respuesta como descripción
                }
                return result, None
        except Exception as e:
            logger.error(f"Error en generate_publication_content: {str(e)}")
            return None, f"Error al generar contenido: {str(e)}"
    
    def _create_prompt(self, adventure_context: str) -> str:
        """
        Crea el prompt para generar el contenido
        
        Args:
            adventure_context: Contexto de la aventura
            
        Returns:
            Prompt formateado
        """
        return f"""
        Actúa como un experto en turismo aventurero. Basado en el siguiente contexto, 
        genera un título atractivo y una descripción detallada para una publicación en una 
        plataforma de turismo aventurero llamada AventuraPe.
        
        CONTEXTO DEL USUARIO:
        {adventure_context}
        
        {CONTENT_INSTRUCTIONS}
        
        FORMATO DE RESPUESTA (solo JSON, sin comentarios adicionales):
        {{
          "title": "Título atractivo y conciso",
          "description": "Descripción detallada y emocionante de la aventura"
        }}
        """
        
    def _contains_inappropriate_content(self, text: str) -> bool:
        """
        Verifica si el texto contiene contenido inapropiado
        
        Args:
            text: Texto a verificar
            
        Returns:
            True si contiene contenido inapropiado, False en caso contrario
        """
        text_lower = text.lower()
        return any(word in text_lower for word in INAPPROPRIATE_WORDS) 