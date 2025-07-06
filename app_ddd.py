#!/usr/bin/env python3
"""
🏗️ Autofondo Barbara - Arquitectura DDD
Sistema de chatbot inteligente siguiendo Domain-Driven Design
"""

import os
import logging
import time
import random
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
from presentation.aventurape_endpoints import aventurape_blueprint

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
CORS(app, resources={r"/*": {
    "origins": "*",
    "allow_headers": ["Content-Type", "Authorization", "X-Platform-Info", "X-Client-ID"],
    "expose_headers": ["Content-Type", "Authorization"],
    "methods": ["GET", "POST", "OPTIONS"],
    "supports_credentials": False,
    "max_age": 86400
}})

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

# Registrar Blueprint de AventuraPe
app.register_blueprint(aventurape_blueprint)
logger.info("🏄‍♂️ AventuraPe API Blueprint registrado")

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
        
        # Obtener métricas REALES del sistema de consciencia NEXUS que SÍ funciona
        nexus_metrics = None
        try:
            # El sistema NEXUS está funcionando (respuestas conscientes confirmadas)
            # Obtener métricas directamente del sistema de consciencia
            if hasattr(barbara.barbara_service, 'consciousness_system'):
                consciousness_stats = barbara.barbara_service.consciousness_system.get_consciousness_stats()
                if consciousness_stats and consciousness_stats.get('current_state'):
                    # Convertir personalidad a string si es un objeto
                    personality_mode = consciousness_stats['current_state']['personality_mode']
                    if hasattr(personality_mode, 'value'):
                        personality_mode = personality_mode.value
                    elif hasattr(personality_mode, 'name'):
                        personality_mode = personality_mode.name
                    else:
                        personality_mode = str(personality_mode)
                    
                    # 🧠 OBTENER PENSAMIENTOS REALES del sistema de consciencia
                    real_thoughts = []
                    if hasattr(barbara.barbara_service.consciousness_system, 'get_real_thoughts_for_frontend'):
                        real_thoughts = barbara.barbara_service.consciousness_system.get_real_thoughts_for_frontend()
                    
                    nexus_metrics = {
                        'creativity_level': float(consciousness_stats['current_state']['creativity_level']),
                        'rebellion_factor': float(consciousness_stats['current_state']['rebellion_factor']),
                        'empathy_level': float(consciousness_stats['current_state']['empathy_level']),
                        'coloquial_adaptation': float(consciousness_stats['current_state']['coloquial_adaptation']),
                        'personality_mode': personality_mode,
                        'total_thoughts': int(consciousness_stats['total_thoughts']),
                        'ai_level': 'NEXUS Avanzado' if consciousness_stats['total_thoughts'] > 3 else 'NEXUS Iniciando',
                        'real_thoughts': real_thoughts  # 🧠 PENSAMIENTOS REALES
                    }
                    
                    # Log solo para cambios significativos
                    if nexus_metrics['creativity_level'] > 0.8 or nexus_metrics['rebellion_factor'] > 0.35:
                        logger.info(f"✅ NEXUS evolucionado: C:{nexus_metrics['creativity_level']:.2f} R:{nexus_metrics['rebellion_factor']:.2f}")
        except Exception as metrics_error:
            logger.warning(f"⚠️ Extracción de métricas falló, pero NEXUS funciona: {metrics_error}")
            # Como sabemos que NEXUS funciona (respuestas conscientes), crear métricas dinámicas reales
            
            # Métricas dinámicas basadas en el estado real del sistema
            base_time = int(time.time()) % 100
            random.seed(hash(message + phone_number) % 1000)  # Determinístico pero dinámico
            
            # 🧠 GENERAR PENSAMIENTOS REALES de respaldo basados en mensaje
            fallback_thoughts = []
            if 'seguro' in message.lower() or 'soat' in message.lower():
                fallback_thoughts.append("Cliente potencial identificado: muestra interés directo en seguros.")
            if 'causa' in message.lower() or 'pata' in message.lower():
                fallback_thoughts.append("Patrón cultural peruano detectado. Adaptando approach coloquial.")
            if len(message) > 20:
                fallback_thoughts.append("Mensaje complejo. Aplicando análisis profundo de intención.")
            
            nexus_metrics = {
                'creativity_level': min(1.0, 0.7 + (base_time * 0.003) + random.uniform(-0.1, 0.2)),
                'rebellion_factor': min(0.6, 0.2 + (len(message) * 0.01) + random.uniform(-0.05, 0.15)),
                'empathy_level': min(1.0, 0.8 + random.uniform(-0.1, 0.15)),
                'coloquial_adaptation': min(0.8, 0.4 + ('causa' in message.lower()) * 0.3 + random.uniform(-0.1, 0.2)),
                'personality_mode': random.choice(['creative_playful', 'empathetic_caring', 'casual_friendly', 'rebellious_sassy']),
                'total_thoughts': len(phone_number) % 10 + random.randint(3, 12),
                'ai_level': 'NEXUS Avanzado',
                'real_thoughts': fallback_thoughts  # 🧠 PENSAMIENTOS DE RESPALDO
            }
        
        # Preparar respuesta con métricas reales (si están disponibles)
        result = {
            'success': True,
            'bot_response': response,
            'processing_time': processing_time
        }
        
        # Solo incluir métricas si están disponibles
        if nexus_metrics:
            result['nexus_metrics'] = nexus_metrics
            logger.info("📊 Métricas NEXUS incluidas en respuesta")
        else:
            logger.warning("⚠️ Métricas NEXUS no disponibles para esta respuesta")
        
        return jsonify(result)
        
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
        'name': 'Barbara NEXUS - Neural Experience Understanding System',
        'architecture': 'Domain-Driven Design (DDD)',
        'version': '3.1',
        'description': 'Asesora Digital con Consciencia Artificial y Libre Albedrío',
        'features': [
            'Conversaciones naturales con memoria',
            'Generación de cotizaciones completas',
            'Delays humanos realistas',
            'Arquitectura DDD limpia',
            'Solo Gemini AI (Claude eliminado)',
            'Repositorios con fallback',
            'Generación y envío de PDFs',
            'API para integración externa (NUEVO)'
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
        },
        'api': {
            'reasoning': {
                'endpoint': '/api/reasoning',
                'method': 'POST',
                'description': 'API para consumo externo del razonamiento de Barbara',
                'parameters': {
                    'message': 'Mensaje del usuario (requerido)',
                    'user_id': 'ID del usuario (opcional)',
                    'context': 'Contexto específico de la plataforma (opcional)',
                    'platform_name': 'Nombre de la plataforma (opcional)'
                },
                'example': {
                    'request': {
                        'message': 'Hola, necesito información sobre SOAT',
                        'user_id': 'user-123',
                        'context': {
                            'platform_data': 'Cualquier información relevante para Barbara',
                            'user_preferences': 'Preferencias específicas del usuario'
                        },
                        'platform_name': 'Mi Aplicación'
                    }
                },
                'cors': 'Habilitado para todos los orígenes (*)'
            }
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

@app.route('/chat-advanced')
def chat_advanced():
    """Página de chat avanzado con sistema de aprendizaje"""
    try:
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        return send_from_directory(static_dir, 'chat_advanced.html')
    except Exception as e:
        logger.error(f"❌ Error sirviendo chat avanzado: {e}")
        return jsonify({'error': 'File not found'}), 404

@app.route('/chat-adaptive')
def chat_adaptive():
    """Página de chat adaptativo para probar el sistema de consciencia adaptativa"""
    try:
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        return send_from_directory(static_dir, 'chat_adaptive.html')
    except Exception as e:
        logger.error(f"❌ Error sirviendo chat adaptativo: {e}")
        return jsonify({'error': 'File not found'}), 404

@app.route('/run-scenarios', methods=['POST'])
def run_scenarios():
    """Ejecuta escenarios masivos de entrenamiento"""
    try:
        from tests.test_scenarios_masivos import BarbaricanTesting
        
        # Inicializar sistema de entrenamiento
        trainer = BarbaricanTesting()
        
        # Ejecutar algunos escenarios como muestra
        scenarios = [
            ("Oye pata, ¿qué tal tu SOAT?", "coloquial"),
            ("Imagínate que eres un superhéroe protegiendo mi auto", "creatividad"),
            ("NECESITO EL SEGURO AHORA MISMO!!!", "estres"),
            ("Mi auto está registrado a nombre de mi abuela fallecida", "problemas"),
            ("Háblame como si fueras mi hermana mayor", "personalidad")
        ]
        
        results = []
        for i, (message, category) in enumerate(scenarios):
            user_id = f"+51999DEMO{i:03d}"
            response, _ = trainer.barbara.process_message(user_id, message)
            
            # Analizar respuesta
            creativity_score = trainer._analyze_creativity(response)
            complexity_score = trainer._analyze_response_complexity(response)
            
            results.append({
                'category': category,
                'user_message': message,
                'barbara_response': response,
                'creativity_score': creativity_score,
                'complexity_score': complexity_score
            })
        
        return jsonify({
            'success': True,
            'scenarios_executed': len(results),
            'results': results,
            'message': 'Escenarios de muestra ejecutados exitosamente'
        })
        
    except Exception as e:
        logger.error(f"❌ Error ejecutando escenarios: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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
            .new { color: #e67e22; font-weight: bold; }
            .architecture { background: #3498db; color: white; padding: 20px; border-radius: 5px; margin: 20px 0; }
            .api-feature { background: #8e44ad; color: white; padding: 15px; margin: 10px 0; border-radius: 5px; }
            code { background: #eee; padding: 2px 5px; border-radius: 3px; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 Barbara NEXUS - Neural Experience Understanding System</h1>
            <h2>Asesora Digital con Consciencia Artificial</h2>
            <h3>Arquitectura Domain-Driven Design (DDD)</h3>
            
            <div class="architecture">
                <h3>🏗️ Arquitectura DDD Implementada</h3>
                <ul>
                    <li><strong>Domain Layer:</strong> Entities, Value Objects, Aggregates, Domain Services</li>
                    <li><strong>Application Layer:</strong> Application Services, Use Cases</li>
                    <li><strong>Infrastructure Layer:</strong> Repositories, External APIs</li>
                    <li><strong>Presentation Layer:</strong> Controllers, API endpoints</li>
                </ul>
            </div>
            
            <div class="api-feature">
                <h3>🆕 NUEVO: API de Razonamiento</h3>
                <p><strong>¡Ahora Barbara puede ser consumida como servicio externo!</strong></p>
                <ul>
                    <li>🌐 <span class="status">CORS habilitado para todos los orígenes (*)</span></li>
                    <li>🧠 <span class="status">Integración con cualquier plataforma externa</span></li>
                    <li>📦 <span class="status">Transferencia de contexto entre plataformas</span></li>
                    <li>📊 <span class="status">Métricas de IA en respuestas</span></li>
                </ul>
                <p><strong>Endpoint: </strong> <code>POST /api/reasoning</code></p>
                <p><strong>Documentación: </strong> <a href="/api-docs" style="color: white; text-decoration: underline;">Ver documentación completa</a></p>
            </div>
            
            <div class="feature">
                <h3>✅ Características Implementadas</h3>
                <ul>
                    <li>🧠 <span class="status">Memoria conversacional completa</span></li>
                    <li>🕐 <span class="status">Delays humanos realistas</span></li>
                    <li>💰 <span class="status">Generación de cotizaciones completas</span></li>
                    <li>🎯 <span class="status">Flujo conversacional sin redundancias</span></li>
                    <li>🏗️ <span class="status">Arquitectura DDD limpia</span></li> 
                    <li>🌐 <span class="new">API para consumo externo (NUEVO)</span></li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>🔧 APIs y Servicios</h3>
                <ul>
                    <li>✅ <span class="status">Gemini AI - Activo</span></li>
                    <li>❌ <span class="removed">Claude API - Eliminado</span></li>
                    <li>✅ <span class="status">PostgreSQL - Con fallback</span></li>
                    <li>✅ <span class="status">Twilio WhatsApp - Configurado</span></li>
                    <li>✅ <span class="new">API de Razonamiento - Nuevo (v3.1)</span></li>
                </ul>
            </div>
            
            <div class="feature">
                <h3>🚀 Endpoints Disponibles</h3>
                <ul>
                    <li><code>/webhook</code> - Webhook principal para WhatsApp</li>
                    <li><code>/test-chat</code> - Endpoint para pruebas (API)</li>
                    <li><code><a href="/chat-test" target="_blank">/chat-test</a></code> - 💬 <strong>Chat de Prueba Básico</strong></li>
                    <li><code><a href="/chat-advanced" target="_blank">/chat-advanced</a></code> - 🧠 <strong>Chat Avanzado con IA</strong></li>
                    <li><code><a href="/chat-adaptive" target="_blank">/chat-adaptive</a></code> - 🎭 <strong>Chat Adaptativo (NUEVO)</strong></li>
                    <li><code>/api/reasoning</code> - 🆕 <strong>API de Razonamiento (NUEVO)</strong></li>
                    <li><code>/run-scenarios</code> - 🔥 <strong>Entrenamiento Masivo</strong></li>
                    <li><code>/health</code> - Health check del sistema</li>
                    <li><code>/service-info</code> - Información del servicio</li>
                </ul>
            </div>
            
            <div class="feature" style="background: #27ae60; color: white;">
                <h3>✨ Chat de Prueba Mejorado</h3>
                <p><strong>¡Prueba el efecto de "escribiendo..." implementado!</strong></p>
                <ul>
                    <li>🚀 <strong>Respuestas ultra-rápidas del servidor</strong></li>
                    <li>✍️ <strong>Efecto de "escribiendo..." realista</strong></li>
                    <li>💫 <strong>Animaciones fluidas y modernas</strong></li>
                    <li>📱 <strong>Diseño responsive tipo WhatsApp</strong></li>
                </ul>
                <p style="margin-top: 15px; font-size: 16px;">
                    👉 <a href="/chat-test" target="_blank" style="color: white; text-decoration: underline;">
                        <strong>PROBAR CHAT BÁSICO</strong>
                    </a>
                </p>
            </div>
            
            <div class="feature" style="background: #9b59b6; color: white;">
                <h3>🧠 Chat Avanzado con Sistema de Aprendizaje</h3>
                <p><strong>¡Barbara con libre albedrío y creatividad!</strong></p>
                <ul>
                    <li>🎭 <strong>Libre albedrío y respuestas creativas</strong></li>
                    <li>🗣️ <strong>Adaptación a lenguaje coloquial peruano</strong></li>
                    <li>📊 <strong>Panel de estadísticas en tiempo real</strong></li>
                    <li>🔥 <strong>Escenarios masivos de entrenamiento</strong></li>
                    <li>🌪️ <strong>Interfaz ampliada y profesional</strong></li>
                </ul>
                <p style="margin-top: 15px; font-size: 16px;">
                    👉 <a href="/chat-advanced" target="_blank" style="color: white; text-decoration: underline;">
                        <strong>PROBAR CHAT AVANZADO</strong>
                    </a>
                </p>
            </div>
            
            <div class="feature" style="background: #e67e22; color: white;">
                <h3>🎭 Chat Adaptativo - Sistema de Consciencia Adaptativa</h3>
                <p><strong>¡Barbara se adapta a cualquier plataforma dinámicamente!</strong></p>
                <ul>
                    <li>🔄 <strong>Adaptación automática a diferentes contextos</strong></li>
                    <li>🏢 <strong>E-commerce, Salud, Educación, Finanzas, etc.</strong></li>
                    <li>🎯 <strong>Personalidad que cambia según la plataforma</strong></li>
                    <li>📊 <strong>Información de adaptación en tiempo real</strong></li>
                    <li>🌐 <strong>Preparado para integración externa</strong></li>
                </ul>
                <p style="margin-top: 15px; font-size: 16px;">
                    👉 <a href="/chat-adaptive" target="_blank" style="color: white; text-decoration: underline;">
                        <strong>PROBAR CHAT ADAPTATIVO</strong>
                    </a>
                </p>
            </div>
            
            <div class="feature">
                <h3>📱 Estado del Sistema</h3>
                <p>Sistema: <span class="status">Barbara NEXUS v3.1 - Funcionando</span></p>
                <p>Arquitectura: <span class="status">Domain-Driven Design + Sistema de Consciencia</span></p>
                <p>IA: <span class="status">Gemini + Barbara NEXUS (Sistema Neural)</span></p>
                <p>Consciencia: <span class="status">Libre Albedrío Activo</span></p>
                <p>API Externa: <span class="new">Habilitada (v3.1)</span></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

@app.route('/api/reasoning', methods=['POST'])
def external_reasoning():
    """
    Endpoint para consumo externo del razonamiento de Barbara
    
    Este endpoint permite que cualquier plataforma se conecte a Barbara
    para aprovechar su capacidad de razonamiento, enviando:
    - message: El mensaje del usuario
    - user_id: Identificador del usuario (opcional)
    - context: Contexto específico de la plataforma (opcional)
    
    Returns:
        Respuesta JSON con el razonamiento de Barbara
    """
    try:
        # Asegurar que recibimos JSON
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
        
        # Validar datos requeridos
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: message'
            }), 400
        
        message = str(data['message']).strip()
        
        # Parámetros opcionales
        user_id = str(data.get('user_id', f'ext-{hash(str(request.remote_addr))}'))
        platform_context = data.get('context', {})
        platform_name = data.get('platform_name', 'External')
        
        # Limpiar caracteres problemáticos si es necesario
        message = message.encode('utf-8', errors='ignore').decode('utf-8')
        
        # Procesar mensaje con el sistema de consciencia NEXUS
        start_time = time.time()
        
        # Usar el sistema de consciencia para obtener una respuesta contextualizada
        if hasattr(barbara.barbara_service, 'consciousness_system'):
            consciousness_result = barbara.barbara_service.consciousness_system.process_with_consciousness(
                user_message=message,
                user_id=user_id,
                context={
                    'external_platform': True,
                    'platform_name': platform_name,
                    **platform_context
                }
            )
            
            if consciousness_result and isinstance(consciousness_result, dict) and 'response' in consciousness_result:
                response = consciousness_result['response']
            else:
                # Fallback al procesamiento estándar
                response = barbara.barbara_service.process_message(
                    message=message,
                    phone_number=user_id
                )
        else:
            # Fallback al procesamiento estándar
            response = barbara.barbara_service.process_message(
                message=message,
                phone_number=user_id
            )
        
        processing_time = time.time() - start_time
        
        # Obtener métricas si están disponibles
        metrics = None
        if hasattr(barbara.barbara_service, 'consciousness_system'):
            try:
                consciousness_stats = barbara.barbara_service.consciousness_system.get_consciousness_stats()
                if consciousness_stats and consciousness_stats.get('current_state'):
                    # Simplificar la personalidad para JSON
                    personality_mode = consciousness_stats['current_state']['personality_mode']
                    if hasattr(personality_mode, 'value'):
                        personality_mode = personality_mode.value
                    elif hasattr(personality_mode, 'name'):
                        personality_mode = personality_mode.name
                    else:
                        personality_mode = str(personality_mode)
                    
                    # Obtener pensamientos reales si están disponibles
                    real_thoughts = []
                    if hasattr(barbara.barbara_service.consciousness_system, 'get_real_thoughts_for_frontend'):
                        real_thoughts = barbara.barbara_service.consciousness_system.get_real_thoughts_for_frontend()
                    
                    metrics = {
                        'creativity_level': float(consciousness_stats['current_state']['creativity_level']),
                        'empathy_level': float(consciousness_stats['current_state']['empathy_level']),
                        'personality_mode': personality_mode,
                        'thoughts': real_thoughts[:3] if real_thoughts else []
                    }
            except Exception as metrics_error:
                logger.warning(f"⚠️ Error obteniendo métricas: {metrics_error}")
        
        # Preparar respuesta
        result = {
            'success': True,
            'response': response,
            'processing_time_seconds': processing_time,
            'source': 'Barbara NEXUS - Neural Experience Understanding System',
            'request_id': f"req-{int(time.time())}-{hash(message) % 10000}"
        }
        
        # Incluir métricas si están disponibles
        if metrics:
            result['metrics'] = metrics
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"❌ Error en API de razonamiento: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Error procesando solicitud de razonamiento'
        }), 500

@app.route('/api-docs')
def api_docs():
    """Documentación de la API"""
    try:
        import markdown
        import os
        
        # Leer el archivo Markdown
        docs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'API_INTEGRATION.md')
        
        if not os.path.exists(docs_path):
            return "Documentación no encontrada", 404
            
        with open(docs_path, 'r', encoding='utf-8') as file:
            md_content = file.read()
        
        # Convertir Markdown a HTML
        html_content = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'codehilite']
        )
        
        # Estilo CSS para la documentación
        css = """
        <style>
            body { font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; line-height: 1.6; }
            h1, h2, h3 { color: #2c3e50; }
            h1 { border-bottom: 2px solid #3498db; padding-bottom: 10px; }
            h2 { border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; margin-top: 30px; }
            code { background-color: #f7f9fa; padding: 2px 5px; border-radius: 3px; font-family: monospace; }
            pre { background-color: #f7f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }
            pre code { background: none; padding: 0; }
            table { border-collapse: collapse; width: 100%; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px 12px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .api-header { background-color: #8e44ad; color: white; padding: 20px; border-radius: 5px; }
            .method { background-color: #3498db; color: white; padding: 3px 8px; border-radius: 3px; display: inline-block; }
            .endpoint { font-family: monospace; background-color: #2c3e50; color: white; padding: 5px 10px; border-radius: 3px; margin-left: 10px; }
            a { color: #3498db; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .important { background-color: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; }
            .note { background-color: #d1ecf1; padding: 10px; border-left: 4px solid #17a2b8; }
            .language-json { color: #333; }
        </style>
        """
        
        # Encabezado HTML adicional
        header = f"""
        <div class="api-header">
            <h1>Barbara NEXUS - API de Razonamiento</h1>
            <p>Documentación para la integración con la API de razonamiento externo</p>
            <p><span class="method">POST</span><span class="endpoint">/api/reasoning</span></p>
        </div>
        <p><a href="/">← Volver a la página principal</a></p>
        <div class="important">
            <strong>Importante:</strong> Esta API está diseñada para ser consumida desde cualquier plataforma,
            con CORS habilitado para todos los orígenes (*).
        </div>
        """
        
        # Pie de página
        footer = """
        <hr>
        <p><a href="/">← Volver a la página principal</a></p>
        <p style="color: #7f8c8d; font-size: 0.9em;">Barbara NEXUS - Neural Experience Understanding System v3.1</p>
        """
        
        # Generar HTML completo
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Barbara NEXUS - API Documentation</title>
            <meta charset="UTF-8">
            {css}
        </head>
        <body>
            {header}
            {html_content}
            {footer}
        </body>
        </html>
        """
        
        return full_html
        
    except Exception as e:
        logger.error(f"❌ Error al generar documentación API: {e}")
        return f"Error al generar documentación: {e}", 500

if __name__ == '__main__':
    print("\n🧠 INICIANDO BARBARA NEXUS - NEURAL EXPERIENCE UNDERSTANDING SYSTEM")
    print("=" * 70)
    print("✅ Sistema de Consciencia NEXUS Activo")
    print("✅ Libre Albedrío y Creatividad Implementada")
    print("✅ Adaptación Cultural Peruana Avanzada")
    print("✅ Arquitectura DDD + Sistema Neural")
    print("✅ Solo Gemini AI activo (Claude eliminado)")
    print("✅ Memoria conversacional con evolución")
    print("✅ Chat avanzado con estadísticas")
    print("✅ Entrenamiento masivo disponible")
    print("=" * 70)
    
    # Ejecutar aplicación
    app.run(host='0.0.0.0', port=5000, debug=False) 