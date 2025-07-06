"""
🏗️ Presentation Layer: AventuraPe Endpoints
Endpoints REST para el servicio de AventuraPe.
"""

from flask import Blueprint, request, jsonify
from flask_cors import CORS
import logging
import os
import json
import traceback
from dotenv import load_dotenv

from domain.services.aventurape_service import AventuraPeService
from infrastructure.external_apis.gemini_ai_service import GeminiAIService
from config.aventurape_config import AVENTURAPE_API_URL

# Cargar variables de entorno desde .environment
load_dotenv('.environment')

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtener API key de Gemini desde variables de entorno
gemini_api_key = os.getenv("GEMINI_API_KEY", "")
if not gemini_api_key:
    logger.warning("⚠️ GEMINI_API_KEY no está configurada. Las funcionalidades de IA no estarán disponibles.")

# Crear instancia del servicio Gemini
gemini_service = GeminiAIService(api_key=gemini_api_key)

# Crear instancia del servicio de AventuraPe
aventurape_service = AventuraPeService(gemini_service)

# Crear Blueprint
aventurape_blueprint = Blueprint('aventurape', __name__, url_prefix='/aventurape')

# Configurar CORS para permitir solicitudes desde AventuraPe-web
CORS(aventurape_blueprint, resources={r"/*": {"origins": "*"}})

@aventurape_blueprint.route('/generate-content', methods=['POST'])
def generate_content():
    """
    Endpoint para generar título y descripción de una publicación
    
    Body:
    {
        "context": "Descripción de la aventura por el usuario"
    }
    
    Response:
    {
        "success": true,
        "content": {
            "title": "Título generado",
            "description": "Descripción generada"
        }
    }
    """
    try:
        # Verificar que Gemini esté configurado
        if not gemini_api_key:
            logger.error("Servicio de IA no configurado. Falta GEMINI_API_KEY.")
            return jsonify({
                "success": False,
                "error": "Servicio de IA no configurado. Contacte al administrador."
            }), 503
        
        # Obtener datos del request
        data = request.json
        if not data:
            logger.warning("Request sin datos JSON")
            return jsonify({
                "success": False,
                "error": "Se requiere un objeto JSON en el cuerpo de la solicitud"
            }), 400
            
        if not data.get('context'):
            logger.warning("Request sin campo 'context'")
            return jsonify({
                "success": False,
                "error": "Se requiere el campo 'context' en el objeto JSON"
            }), 400
        
        adventure_context = data.get('context')
        
        # Validar longitud del contexto
        if len(adventure_context) < 10:
            logger.warning(f"Contexto demasiado corto: '{adventure_context}'")
            return jsonify({
                "success": False,
                "error": "El contexto proporcionado es demasiado corto. Por favor, proporcione una descripción más detallada."
            }), 400
        
        # Generar contenido
        logger.info(f"Generando contenido para contexto: '{adventure_context[:50]}...'")
        content, error = aventurape_service.generate_publication_content(adventure_context)
        
        if error:
            logger.error(f"Error al generar contenido: {error}")
            return jsonify({
                "success": False,
                "error": error
            }), 400
            
        logger.info("Contenido generado correctamente")
        return jsonify({
            "success": True,
            "content": content
        }), 200
            
    except Exception as e:
        # Capturar stack trace para debugging
        stack_trace = traceback.format_exc()
        logger.error(f"Error no controlado al generar contenido: {str(e)}")
        logger.error(f"Stack trace: {stack_trace}")
        
        return jsonify({
            "success": False,
            "error": "Error interno del servidor"
        }), 500

@aventurape_blueprint.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificar la salud del servicio
    
    Response:
    {
        "status": "healthy",
        "services": {
            "gemini": "ok"
        },
        "aventurape_api": {
            "url": "http://localhost:8080"
        }
    }
    """
    try:
        # Verificar si el servicio de Gemini está disponible
        gemini_status = gemini_service.health_check() if gemini_api_key else False
        
        # Verificar si se ha configurado la API key de Gemini
        api_key_status = "configured" if gemini_api_key else "not_configured"
        
        # Construir respuesta detallada
        response = {
            "status": "healthy",
            "timestamp": os.popen('date -u +"%Y-%m-%dT%H:%M:%SZ"').read().strip(),
            "services": {
                "gemini": {
                    "status": "ok" if gemini_status else "error",
                    "api_key": api_key_status
                }
            },
            "aventurape_api": {
                "url": AVENTURAPE_API_URL
            },
            "version": "1.0.0"
        }
        
        logger.info("Health check exitoso")
        return jsonify(response), 200
    except Exception as e:
        stack_trace = traceback.format_exc()
        logger.error(f"Error en health check: {str(e)}")
        logger.error(f"Stack trace: {stack_trace}")
        
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500
        
@aventurape_blueprint.errorhandler(404)
def handle_not_found(e):
    """Manejador para rutas no encontradas"""
    return jsonify({
        "success": False,
        "error": "Recurso no encontrado"
    }), 404
    
@aventurape_blueprint.errorhandler(405)
def handle_method_not_allowed(e):
    """Manejador para métodos no permitidos"""
    return jsonify({
        "success": False,
        "error": "Método no permitido"
    }), 405 