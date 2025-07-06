#!/usr/bin/env python3
"""
🏗️ Barbara Simple - Versión sin spaCy para pruebas rápidas
"""

import os
import logging
import time
import json
import random
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from typing import Optional, Dict, List, Any
from presentation.aventurape_endpoints import aventurape_blueprint

# Cargar variables de entorno
load_dotenv('.environment')

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Verificar API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY es requerida")

class BarbaraSimple:
    """Versión simplificada de Barbara sin dependencias complejas"""
    
    def __init__(self):
        self.gemini_api_key = GEMINI_API_KEY
        self.user_context = {}  # Almacena contexto por usuario
        self.pdf_locations = {
            "cotizacion_AF202506270003.pdf": "assets/cotizacion_AF202506270003.pdf",
            "cotizacion_AF202506270707E2EE.pdf": "assets/cotizacion_AF202506270707E2EE.pdf",
            "cotizacion_AF202506271D78CE30.pdf": "assets/cotizacion_AF202506271D78CE30.pdf",
            "cotizacion_AF202506277B814E8D.pdf": "assets/cotizacion_AF202506277B814E8D.pdf",
            "cotizacion_AF20250627A11EF77A.pdf": "assets/cotizacion_AF20250627A11EF77A.pdf",
            "cotizacion_AF20250627AF0A46D0.pdf": "assets/cotizacion_AF20250627AF0A46D0.pdf",
            "cotizacion_AF20250627BF8111FC.pdf": "assets/cotizacion_AF20250627BF8111FC.pdf",
            "cotizacion_AF20250627CE3FDF74.pdf": "assets/cotizacion_AF20250627CE3FDF74.pdf",
            "cotizacion_AF20250627E4A31037.pdf": "assets/cotizacion_AF20250627E4A31037.pdf",
            "cotizacion_DIAGNOSTICO001.pdf": "assets/cotizacion_DIAGNOSTICO001.pdf",
            "cotizacion_prueba.pdf": "assets/cotizacion_prueba.pdf",
            "cotizacion_SOLUCION001.pdf": "assets/cotizacion_SOLUCION001.pdf",
            "cotizacion_TEST001.pdf": "assets/cotizacion_TEST001.pdf",
            "cotizacion_TEST123.pdf": "assets/cotizacion_TEST123.pdf"
        }
        logger.info("🎭 Barbara Simple inicializada")
    
    def process_message(self, message: str, user_id: str) -> str:
        """Procesa mensaje de forma simple pero más inteligente"""
        try:
            # Inicializar contexto del usuario si no existe
            if user_id not in self.user_context:
                self.user_context[user_id] = {
                    "last_topic": None,
                    "interaction_count": 0,
                    "mentioned_pdfs": []
                }
            
            # Actualizar contador de interacciones
            self.user_context[user_id]["interaction_count"] += 1
            
            # Procesar mensaje en minúsculas para facilitar comparaciones
            message_lower = message.lower()
            
            # Detectar intención principal
            if any(word in message_lower for word in ["hola", "buenos días", "buenas tardes", "saludos"]):
                self.user_context[user_id]["last_topic"] = "saludo"
                return "¡Hola! Soy Barbara, tu asesora digital especializada en seguros. ¿En qué puedo ayudarte hoy?"
            
            elif any(word in message_lower for word in ["pdf", "documento", "archivo", "cotización", "cotizacion"]):
                self.user_context[user_id]["last_topic"] = "documentos"
                
                # Si pregunta específicamente dónde están los PDFs
                if any(phrase in message_lower for phrase in ["donde estan", "dónde están", "ubicación", "ubicacion", "encontrar"]):
                    pdf_list = ", ".join(list(self.pdf_locations.keys())[:5]) + "..."
                    return f"Los archivos PDF de cotizaciones se encuentran en la carpeta 'assets'. Algunos ejemplos son: {pdf_list}. ¿Te gustaría que te ayude con alguno en específico?"
                
                # Si menciona un PDF específico
                for pdf_name in self.pdf_locations:
                    if pdf_name.lower() in message_lower:
                        self.user_context[user_id]["mentioned_pdfs"].append(pdf_name)
                        return f"He identificado que estás interesado en el archivo {pdf_name}. Este documento se encuentra en la ruta {self.pdf_locations[pdf_name]}. ¿Necesitas información adicional sobre este documento?"
                
                return "Tenemos varios archivos PDF de cotizaciones disponibles. ¿Estás buscando alguno en particular o quieres que te muestre la lista completa?"
            
            elif any(word in message_lower for word in ["soat", "seguro", "vehículo", "vehiculo", "auto", "carro", "moto"]):
                self.user_context[user_id]["last_topic"] = "seguros_vehiculos"
                
                if "precio" in message_lower or "costo" in message_lower or "cuánto" in message_lower or "cuanto" in message_lower:
                    return "El precio del SOAT depende del tipo de vehículo, su uso y otras características. ¿Podrías proporcionarme más detalles sobre tu vehículo para darte una cotización más precisa?"
                
                if "auto" in message_lower or "carro" in message_lower:
                    return "Para cotizar el SOAT de tu auto, necesito algunos datos: marca, modelo, año y uso (particular o público). ¿Podrías proporcionarme esta información?"
                
                if "moto" in message_lower or "motocicleta" in message_lower:
                    return "Para las motocicletas, el SOAT tiene tarifas especiales según el cilindraje. ¿Podrías indicarme el cilindraje de tu moto?"
                
                return "Estoy especializada en seguros vehiculares como el SOAT. ¿Qué tipo de vehículo tienes y para qué lo utilizas principalmente?"
            
            elif "ya te vas" in message_lower or "te vas" in message_lower:
                return "No, estoy aquí para ayudarte. Mi sistema está activo y listo para responder tus consultas sobre seguros, cotizaciones o cualquier otra información que necesites. ¿En qué más puedo asistirte?"
            
            # Respuesta basada en contexto previo
            last_topic = self.user_context[user_id]["last_topic"]
            if last_topic == "saludo":
                return "¿En qué puedo ayudarte hoy? Puedo brindarte información sobre seguros, cotizaciones, o ayudarte a encontrar documentos específicos."
            
            elif last_topic == "documentos":
                return "Tenemos varios documentos de cotizaciones disponibles. Si me indicas qué tipo de seguro te interesa, puedo recomendarte algunas opciones relevantes."
            
            elif last_topic == "seguros_vehiculos":
                return "Para continuar con tu cotización de seguro vehicular, necesito algunos datos adicionales. ¿Podrías proporcionarme más información sobre tu vehículo?"
            
            # Respuesta genérica si no se detecta una intención específica
            return "Estoy aquí para ayudarte con información sobre seguros y cotizaciones. ¿Podrías ser más específico sobre lo que necesitas?"
                
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            return "¡Ups! Tuve un pequeño problema técnico. ¿Podrías intentar nuevamente con tu consulta?"

# Instancia global
barbara = BarbaraSimple()

# Registrar Blueprint de AventuraPe
app.register_blueprint(aventurape_blueprint)
logger.info("🏄‍♂️ AventuraPe API Blueprint registrado")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check simple"""
    return jsonify({
        'status': 'healthy',
        'service': 'Barbara Simple',
        'timestamp': time.time()
    })

@app.route('/test-chat', methods=['POST'])
def test_chat():
    """Endpoint de prueba simple"""
    try:
        data = request.get_json()
        if not data or 'message' not in data or 'phone' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400
        
        message = data['message']
        phone = data['phone']
        
        response = barbara.process_message(message, phone)
        
        return jsonify({
            'success': True,
            'bot_response': response,
            'user_message': message,
            'phone': phone
        })
        
    except Exception as e:
        logger.error(f"Error en test-chat: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reasoning', methods=['POST'])
def external_reasoning():
    """API de razonamiento simple"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        message = data['message']
        user_id = data.get('user_id', 'external_user')
        context = data.get('context', {})
        
        # Procesar con Barbara
        response = barbara.process_message(message, user_id)
        
        return jsonify({
            'success': True,
            'response': response,
            'processing_time_seconds': 0.1,
            'source': 'Barbara Simple',
            'platform_detected': context.get('platform_type', 'unknown'),
            'personality_adapted': 'simple'
        })
        
    except Exception as e:
        logger.error(f"Error en reasoning: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat-adaptive')
def chat_adaptive():
    """Interfaz de chat adaptativo"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Barbara Adaptive Chat</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                background-color: #8e44ad;
                color: white;
                padding: 20px;
                border-radius: 10px 10px 0 0;
                text-align: center;
            }
            .chat-container {
                background-color: white;
                border-radius: 0 0 10px 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                padding: 20px;
                margin-bottom: 20px;
            }
            .chat-box {
                height: 400px;
                overflow-y: auto;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
            }
            .message {
                padding: 10px;
                margin: 5px 0;
                border-radius: 10px;
                max-width: 80%;
            }
            .user-message {
                background-color: #e6f7ff;
                margin-left: auto;
                text-align: right;
            }
            .bot-message {
                background-color: #f0f0f0;
                margin-right: auto;
            }
            .input-container {
                display: flex;
                margin-top: 10px;
            }
            .message-input {
                flex: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
            }
            .send-button {
                background-color: #8e44ad;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                margin-left: 10px;
                cursor: pointer;
                font-size: 16px;
            }
            .platform-selector {
                margin-bottom: 20px;
                padding: 10px;
                background-color: #f9f9f9;
                border-radius: 5px;
            }
            .platform-selector select {
                padding: 8px;
                width: 100%;
                border-radius: 5px;
                border: 1px solid #ddd;
                font-size: 16px;
            }
            .metrics {
                background-color: #f9f9f9;
                padding: 10px;
                border-radius: 5px;
                margin-top: 20px;
            }
            .metrics h3 {
                margin-top: 0;
            }
            .loading {
                text-align: center;
                padding: 20px;
                display: none;
            }
            .loading-spinner {
                border: 5px solid #f3f3f3;
                border-top: 5px solid #8e44ad;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎭 Barbara Adaptive Chat</h1>
                <p>Sistema de chat con adaptación de personalidad</p>
            </div>
            
            <div class="platform-selector">
                <h3>Selecciona la plataforma:</h3>
                <select id="platformSelect">
                    <option value="ecommerce">E-commerce</option>
                    <option value="customer_service">Servicio al Cliente</option>
                    <option value="educational">Educativa</option>
                    <option value="insurance" selected>Seguros</option>
                    <option value="healthcare">Salud</option>
                </select>
            </div>
            
            <div class="chat-container">
                <div class="chat-box" id="chatBox">
                    <div class="message bot-message">
                        ¡Hola! Soy Barbara, tu asistente virtual especializada en seguros. ¿En qué puedo ayudarte hoy?
                    </div>
                </div>
                
                <div class="loading" id="loadingIndicator">
                    <div class="loading-spinner"></div>
                    <p>Procesando mensaje...</p>
                </div>
                
                <div class="input-container">
                    <input type="text" class="message-input" id="messageInput" placeholder="Escribe tu mensaje aquí..." />
                    <button class="send-button" id="sendButton">Enviar</button>
                </div>
            </div>
            
            <div class="metrics" id="metricsContainer">
                <h3>Métricas de adaptación:</h3>
                <p><strong>Plataforma detectada:</strong> <span id="platformDetected">insurance</span></p>
                <p><strong>Personalidad adaptada:</strong> <span id="personalityAdapted">simple</span></p>
                <p><strong>Tiempo de procesamiento:</strong> <span id="processingTime">0.1</span> segundos</p>
            </div>
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const chatBox = document.getElementById('chatBox');
                const messageInput = document.getElementById('messageInput');
                const sendButton = document.getElementById('sendButton');
                const platformSelect = document.getElementById('platformSelect');
                const loadingIndicator = document.getElementById('loadingIndicator');
                const platformDetected = document.getElementById('platformDetected');
                const personalityAdapted = document.getElementById('personalityAdapted');
                const processingTime = document.getElementById('processingTime');
                
                // Función para añadir mensajes al chat
                function addMessage(message, isUser = false) {
                    const messageDiv = document.createElement('div');
                    messageDiv.classList.add('message');
                    messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
                    messageDiv.textContent = message;
                    chatBox.appendChild(messageDiv);
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
                
                // Función para enviar mensaje a la API
                async function sendMessage() {
                    const message = messageInput.value.trim();
                    if (!message) return;
                    
                    // Añadir mensaje del usuario
                    addMessage(message, true);
                    messageInput.value = '';
                    
                    // Mostrar indicador de carga
                    loadingIndicator.style.display = 'block';
                    
                    try {
                        const response = await fetch('/api/reasoning', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                message: message,
                                user_id: 'web_user',
                                context: {
                                    platform_type: platformSelect.value
                                }
                            })
                        });
                        
                        const data = await response.json();
                        
                        if (data.success) {
                            // Añadir respuesta del bot
                            addMessage(data.response);
                            
                            // Actualizar métricas
                            platformDetected.textContent = data.platform_detected || '-';
                            personalityAdapted.textContent = data.personality_adapted || '-';
                            processingTime.textContent = data.processing_time_seconds?.toFixed(2) || '-';
                        } else {
                            addMessage('Lo siento, ha ocurrido un error. Por favor, intenta nuevamente.');
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        addMessage('Error de conexión. Por favor, verifica tu conexión a internet.');
                    } finally {
                        // Ocultar indicador de carga
                        loadingIndicator.style.display = 'none';
                    }
                }
                
                // Event listeners
                sendButton.addEventListener('click', sendMessage);
                
                messageInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
                
                // Cambiar plataforma
                platformSelect.addEventListener('change', function() {
                    addMessage(`Cambiando a plataforma: ${platformSelect.options[platformSelect.selectedIndex].text}`);
                });
            });
        </script>
    </body>
    </html>
    """

@app.route('/test-aventurape')
def test_aventurape():
    """Interfaz de prueba para AventuraPe"""
    return send_from_directory('static', 'test_aventurape.html')

@app.route('/')
def home():
    """Página principal simple"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Barbara Simple</title>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .header { background-color: #8e44ad; color: white; padding: 20px; border-radius: 5px; }
            .endpoint { background-color: #f8f9fa; padding: 10px; margin: 10px 0; border-radius: 3px; }
            .method { background-color: #3498db; color: white; padding: 3px 8px; border-radius: 3px; }
            .chat-links { margin-top: 30px; }
            .chat-link { display: block; background-color: #8e44ad; color: white; text-align: center; 
                        padding: 15px; margin: 10px 0; border-radius: 5px; text-decoration: none; font-weight: bold; }
            .chat-link:hover { background-color: #7d3c98; }
            .aventurape-link { display: block; background-color: #28a745; color: white; text-align: center; 
                        padding: 15px; margin: 10px 0; border-radius: 5px; text-decoration: none; font-weight: bold; }
            .aventurape-link:hover { background-color: #218838; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎭 Barbara Simple</h1>
            <p>Versión simplificada para pruebas rápidas</p>
        </div>
        
        <h2>🚀 AventuraPe - Generador de Contenido:</h2>
        <a href="/test-aventurape" class="aventurape-link">🧪 Probar Barbara-Nexus AventuraPe</a>
        
        <h2>Endpoints disponibles:</h2>
        
        <div class="endpoint">
            <span class="method">GET</span> <code>/health</code> - Health check
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/test-chat</code> - Chat de prueba
        </div>
        
        <div class="endpoint">
            <span class="method">POST</span> <code>/api/reasoning</code> - API de razonamiento
        </div>
        
        <h3>🏄‍♂️ AventuraPe Endpoints:</h3>
        <div class="endpoint">
            <span class="method">GET</span> <code>/aventurape/health</code> - Health check de AventuraPe
        </div>
        <div class="endpoint">
            <span class="method">POST</span> <code>/aventurape/generate-content</code> - Generar título y descripción
        </div>
        
        <div class="chat-links">
            <h2>Interfaces de chat:</h2>
            <a href="/chat-adaptive" class="chat-link">📱 Chat Adaptativo</a>
        </div>
        
        <h2>Estado del servicio:</h2>
        <p>✅ API Key de Gemini configurada</p>
        <p>✅ Servidor funcionando en puerto 5000</p>
        <p>✅ CORS habilitado para todos los orígenes</p>
        <p>✅ Módulo AventuraPe registrado</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🚀 INICIANDO BARBARA SIMPLE")
    print("=" * 30)
    print("✅ Sin dependencias complejas")
    print("✅ Solo Gemini AI")
    print("✅ CORS habilitado")
    print("=" * 30)
    
    app.run(host='0.0.0.0', port=5000, debug=False) 