#!/usr/bin/env python3
"""
🏗️ Autofondo Barbara - Arquitectura DDD
Sistema de chatbot inteligente siguiendo Domain-Driven Design
"""

import os
import logging
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
from typing import Optional

# Importaciones locales (DDD)
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.external_apis.gemini_ai_service import GeminiAIService
from infrastructure.repositories.postgresql_client_repository import PostgreSQLClientRepository
from infrastructure.repositories.postgresql_quote_repository import PostgreSQLQuoteRepository

# Importar después para evitar importaciones circulares
from application.services.barbara_application_service import BarbaraApplicationService

# Cargar variables de entorno - Usando archivo renombrado para evitar eliminación automática
load_dotenv('.environment')

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración Flask
app = Flask(__name__)
CORS(app)

# 🚀 CONFIGURACIÓN DINÁMICA - CERO VALORES HARDCODEADOS
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

# APIs dinámicas - Con validación requerida
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY es requerida en el archivo .env")

# Configuración rutas ML para evitar archivos sueltos
ML_BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ml')
os.makedirs(ML_BASE_PATH, exist_ok=True)

class AutofondoBarbara:
    """
    🎭 Aplicación principal de Barbara
    Arquitectura DDD - Sin Claude, solo Gemini
    """
    
    def __init__(self):
        self.twilio_client = self._initialize_twilio()
        self.barbara_service = self._initialize_barbara_service()
        
        logger.info("🎭 Barbara DDD inicializada correctamente")
    
    def _initialize_twilio(self) -> Optional[Client]:
        """Inicializa cliente Twilio"""
        try:
            if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
                client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                logger.info("✅ Twilio configurado correctamente")
                return client
        except Exception as e:
            logger.warning(f"⚠️ Error configurando Twilio: {e}")
        return None
    
    def _initialize_barbara_service(self) -> BarbaraApplicationService:
        """Inicializa el servicio de aplicación de Barbara"""
        
        # Servicios de infraestructura - GEMINI_API_KEY ya validada
        gemini_service = GeminiAIService(str(GEMINI_API_KEY))
        
        # Repositorios (con fallback a implementación en memoria)
        try:
            client_repo = PostgreSQLClientRepository()
            quote_repo = PostgreSQLQuoteRepository()
            logger.info("✅ Repositorios PostgreSQL inicializados")
        except Exception as e:
            logger.warning(f"⚠️ Error con PostgreSQL, usando memoria: {e}")
            client_repo = None  # Fallback implementado en Barbara Service
            quote_repo = None
        
        # Servicio de aplicación
        return BarbaraApplicationService(
            gemini_service=gemini_service,
            client_repository=client_repo,
            quote_repository=quote_repo
        )
    
    def process_whatsapp_message(self, message: str, phone_number: str) -> str:
        """Procesa mensaje de WhatsApp"""
        
        start_time = time.time()
        
        try:
            logger.info(f"📱 Mensaje WhatsApp de {phone_number}: {message}")
            
            # Procesar con Barbara (DDD Application Service)
            response = self.barbara_service.process_message(message, phone_number)
            
            processing_time = time.time() - start_time
            logger.info(f"⏱️ Tiempo procesamiento: {processing_time:.2f}s")
            logger.info(f"📤 Respuesta enviada: {response[:100]}...")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error procesando mensaje: {e}")
            return self._get_error_response()
    
    def _get_error_response(self) -> str:
        """Respuesta de error estándar"""
        return """¡Ups! Tuve un pequeño inconveniente técnico 😅

Soy Barbara, tu asesora digital. ¿Podrías intentar nuevamente o contactar a nuestro asesor: +51 999 888 777?"""

# Instancia global de Barbara
barbara = AutofondoBarbara()

# ================ ENDPOINTS FLASK ================

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook principal para WhatsApp"""
    
    try:
        # Obtener datos del mensaje
        from_number = request.values.get('From', '')
        message = request.values.get('Body', '')
        
        # Limpiar número de teléfono
        phone_number = from_number.replace('whatsapp:', '')
        
        # Procesar mensaje con Barbara DDD
        response = barbara.process_whatsapp_message(message, phone_number)
        
        # Crear respuesta Twilio
        twiml_response = MessagingResponse()
        twiml_response.message(response)
        
        return str(twiml_response)
        
    except Exception as e:
        logger.error(f"❌ Error en webhook: {e}")
        
        # Respuesta de error para Twilio
        twiml_response = MessagingResponse()
        twiml_response.message(barbara._get_error_response())
        
        return str(twiml_response)

@app.route('/test-chat', methods=['POST'])
def test_chat():
    """Endpoint de prueba para chat"""
    try:
        # Asegurar encoding UTF-8 correcto
        if request.content_type != 'application/json':
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        # Obtener datos con manejo seguro de UTF-8
        try:
            data = request.get_json(force=True)
        except Exception as json_error:
            logger.error(f"❌ Error parsing JSON: {json_error}")
            return jsonify({
                'success': False,
                'error': 'Invalid JSON format'
            }), 400
        
        if not data or 'message' not in data or 'phone' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: message and phone'
            }), 400
        
        message = str(data['message']).strip()
        phone_number = str(data['phone']).strip()
        
        # Validar que no estén vacíos
        if not message or not phone_number:
            return jsonify({
                'success': False,
                'error': 'Message and phone cannot be empty'
            }), 400
        
        # Limpiar caracteres problemáticos si es necesario
        message = message.encode('utf-8', errors='ignore').decode('utf-8')
        
        # Procesar mensaje
        start_time = time.time_ns()
        
        response = barbara.barbara_service.process_message(
            message=message,
            phone_number=phone_number
        )
        
        processing_time = time.time_ns()
        
        return jsonify({
            'success': True,
            'bot_response': response,
            'processing_time': processing_time
        })
        
    except Exception as e:
        logger.error(f"❌ Error en test-chat: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'bot_response': barbara._get_error_response()
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check del sistema DDD"""
    
    try:
        # Verificar servicios
        service_status = barbara.barbara_service.get_service_status()
        
        return jsonify({
            'status': 'healthy',
            'system': 'Barbara DDD',
            'architecture': 'Domain-Driven Design',
            'version': '2.0',
            'services': service_status,
            'timestamp': time.time()
        })
        
    except Exception as e:
        logger.error(f"❌ Error en health check: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/service-info', methods=['GET'])
def service_info():
    """Información del servicio DDD"""
    
    return jsonify({
        'name': 'Autofondo Barbara',
        'architecture': 'Domain-Driven Design (DDD)',
        'version': '2.0',
        'description': 'Chatbot inteligente con arquitectura DDD',
        'features': [
            'Conversaciones naturales con memoria',
            'Generación de cotizaciones completas',
            'Delays humanos realistas',
            'Arquitectura DDD limpia',
            'Solo Gemini AI (Claude eliminado)',
            'Repositorios con fallback',
            'Generación y envío de PDFs'
        ],
        'ai_services': {
            'gemini': 'active',
            'claude': 'removed'
        },
        'layers': {
            'domain': 'Entities, Value Objects, Aggregates, Services',
            'application': 'Application Services, Use Cases',
            'infrastructure': 'Repositories, External APIs',
            'presentation': 'Controllers, API endpoints'
        }
    })

@app.route('/assets/<filename>')
def serve_pdf(filename):
    """Sirve archivos PDF generados (cotizaciones)"""
    try:
        assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
        return send_from_directory(assets_dir, filename)
    except Exception as e:
        logger.error(f"❌ Error sirviendo PDF {filename}: {e}")
        return jsonify({'error': 'File not found'}), 404

@app.route('/chat-test')
def chat_test():
    """Página de prueba del chat con efecto de escribiendo"""
    try:
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        return send_from_directory(static_dir, 'chat_test.html')
    except Exception as e:
        logger.error(f"❌ Error sirviendo chat test: {e}")
        return jsonify({'error': 'File not found'}), 404

@app.route('/')
def home():
    """Página principal"""
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Barbara - Arquitectura DDD</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .feature { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
            .status { color: #27ae60; font-weight: bold; }
            .removed { color: #e74c3c; font-weight: bold; }
            .architecture { background: #3498db; color: white; padding: 20px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎭 Barbara - Asesora Digital</h1>
            <h2>Arquitectura Domain-Driven Design (DDD)</h2>
            
            <div class="architecture">
                <h3>🏗️ Arquitectura DDD Implementada</h3>
                <ul>
                    <li><strong>Domain Layer:</strong> Entities, Value Objects, Aggregates, Domain Services</li>
                    <li><strong>Application Layer:</strong> Application Services, Use Cases</li>
                    <li><strong>Infrastructure Layer:</strong> Repositories, External APIs</li>
                    <li><strong>Presentation Layer:</strong> Controllers, API endpoints</li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>✅ Características Implementadas</h3>
                <ul>
                    <li>🧠 <span class="status">Memoria conversacional completa</span></li>
                    <li>🕐 <span class="status">Delays humanos realistas</span></li>
                    <li>💰 <span class="status">Generación de cotizaciones completas</span></li>
                    <li>🎯 <span class="status">Flujo conversacional sin redundancias</span></li>
                    <li>🏗️ <span class="status">Arquitectura DDD limpia</span></li> 
                </ul>
            </div>
            
            <div class="feature">
                <h3>🔧 APIs y Servicios</h3>
                <ul>
                    <li>✅ <span class="status">Gemini AI - Activo</span></li>
                    <li>❌ <span class="removed">Claude API - Eliminado</span></li>
                    <li>✅ <span class="status">PostgreSQL - Con fallback</span></li>
                    <li>✅ <span class="status">Twilio WhatsApp - Configurado</span></li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>🚀 Endpoints Disponibles</h3>
                <ul>
                    <li><code>/webhook</code> - Webhook principal para WhatsApp</li>
                    <li><code>/test-chat</code> - Endpoint para pruebas (API)</li>
                    <li><code><a href="/chat-test" target="_blank">/chat-test</a></code> - 💬 <strong>Chat de Prueba Interactivo</strong></li>
                    <li><code>/health</code> - Health check del sistema</li>
                    <li><code>/service-info</code> - Información del servicio</li>
                </ul>
            </div>
            
            <div class="feature" style="background: #27ae60; color: white;">
                <h3>✨ NUEVO: Chat de Prueba Mejorado</h3>
                <p><strong>¡Prueba el efecto de "escribiendo..." implementado!</strong></p>
                <ul>
                    <li>🚀 <strong>Respuestas ultra-rápidas del servidor</strong></li>
                    <li>✍️ <strong>Efecto de "escribiendo..." realista</strong></li>
                    <li>💫 <strong>Animaciones fluidas y modernas</strong></li>
                    <li>📱 <strong>Diseño responsive tipo WhatsApp</strong></li>
                </ul>
                <p style="margin-top: 15px; font-size: 16px;">
                    👉 <a href="/chat-test" target="_blank" style="color: white; text-decoration: underline;">
                        <strong>PROBAR CHAT AHORA</strong>
                    </a>
                </p>
            </div>
            
            <div class="feature">
                <h3>📱 Estado del Sistema</h3>
                <p>Sistema: <span class="status">Barbara DDD v2.0 - Funcionando</span></p>
                <p>Arquitectura: <span class="status">Domain-Driven Design</span></p>
                <p>IA: <span class="status">Solo Gemini (Claude eliminado)</span></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

if __name__ == '__main__':
    print("\n🎭 INICIANDO BARBARA - ARQUITECTURA DDD")
    print("=" * 50)
    print("✅ Claude API eliminado completamente")
    print("✅ Solo Gemini AI activo") 
    print("✅ Arquitectura DDD implementada")
    print("✅ Memoria conversacional completa")
    print("✅ Delays humanos realistas")
    print("✅ Generación de cotizaciones")
    print("=" * 50)
    
    # Ejecutar aplicación
    app.run(host='0.0.0.0', port=5000, debug=False) 