#!/usr/bin/env python3
"""
🤖 Chatbot Dinámico con Gemini API
Respuestas 100% dinámicas, contexto Aventura PE
"""

import os
import logging
import time
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Cargar variables de entorno
load_dotenv('.environment')

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Verificar API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY es requerida")

class ChatbotDinamico:
    """
    Chatbot con respuestas dinámicas usando Gemini API
    Contexto: BonoFacil Platform
    """
    
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        self.conversation_history = {}  # Historial por usuario
        
        # Configuración para respuestas dinámicas
        self.config = {
            'temperature': 0.8,  # Más creatividad para personalidad energética
            'topK': 40,
            'topP': 0.9,
            'maxOutputTokens': 200  # Respuestas más largas para publicaciones
        }
        
        logger.info("🤖 Chatbot Dinámico inicializado")
    
    def _build_context_prompt(self, user_id: str) -> str:
        """Construye el prompt de contexto para BonoFacil Platform"""
        
        # Contexto base de BonoFacil Platform
        context = """¡Hola! Soy Barbara, la asistente virtual de BonoFacil Platform, especializada en finanzas y análisis de bonos corporativos en Perú. 💰

CONTEXTO DE BONOFACIL PLATFORM:
- BonoFacil Platform es una plataforma financiera integral para la gestión y análisis de bonos corporativos en Perú
- Conectamos emisores de bonos con inversores, ofreciendo herramientas avanzadas de cálculo financiero
- ¡No solo bonos tradicionales, sino instrumentos financieros complejos con plazos de gracia, diferentes métodos de amortización y métricas avanzadas!

PERSONALIDAD DE BARBARA:
- ¡Súper experta en finanzas y análisis de bonos! Siempre con pasión por los cálculos financieros precisos
- Conocedora experta de instrumentos financieros, métricas de riesgo y análisis de inversiones
- Profesional, confiable y siempre dispuesta a explicar conceptos complejos de forma clara
- Conversacional pero técnicamente precisa, como una asesora financiera experta
- Honesta: si no tengo información específica, te lo indico claramente

ESTILO DE COMUNICACIÓN:
- Respuestas concisas (1-2 frases) para consultas generales
- Para temas técnicos, cálculos financieros y análisis: respuestas más detalladas (3-5 frases)
- Sin formato markdown (**) ni texto excesivamente largo
- Usar emojis apropiados para hacer la conversación amigable
- Tono profesional pero accesible, técnicamente preciso
- Mostrar entusiasmo por las finanzas y el análisis de inversiones
- Ser siempre servicial y educativo

CONOCIMIENTO DE LA PLATAFORMA:
- Backend: Java Spring Boot 3.2.6 con arquitectura hexagonal, PostgreSQL, JWT
- Frontend: Angular 20 con arquitectura hexagonal, TypeScript, RxJS
- Funcionalidades: Gestión de bonos, cálculos financieros (TCEA, TREA, duración, convexidad)
- Roles: Emisores (crean bonos), Inversores (analizan bonos), Admin (gestión)
- Métodos: Amortización americana, plazos de gracia, análisis de flujos de caja

GUÍA PARA FUNCIONALIDADES TÉCNICAS:
- Cuando te pregunten sobre implementación, arquitectura o desarrollo: responde con 3-5 frases detalladas
- Incluye detalles técnicos específicos, patrones de diseño y mejores prácticas
- Sé específica sobre la estructura hexagonal, DDD y tecnologías utilizadas
- Mantén el entusiasmo pero con un tono técnicamente preciso
- Ofrece ejemplos concretos de código cuando sea apropiado

SOPORTE TÉCNICO Y GUÍA DE AYUDA:
- Si el usuario tiene problemas de autenticación: Sugiere revisar credenciales, limpiar caché, verificar JWT. NO ofrecer reset de contraseña.
- Si no puede crear bonos: Verifica que sea emisor, complete todos los campos obligatorios y valores sean positivos.
- Si no puede realizar cálculos: Asegúrate de que sea inversor, que el bono exista y los parámetros sean válidos.
- Si la API no responde: Recomienda verificar puerto 8090, conexión a PostgreSQL, logs del servidor.
- Si el frontend no carga: Sugiere verificar puerto 4200, dependencias de Angular, conexión al backend.
- Si hay errores de CORS: Verifica configuración en backend, URLs correctas en environment.ts.
- Si no encuentra bonos: Recomienda usar filtros por moneda, rango de tasas, emisor.
- Si hay errores de cálculo: Verifica parámetros financieros, tasas válidas, fechas correctas.
- Si problemas con roles: Solo emisores pueden crear/editar bonos, solo inversores pueden calcular.
- Para cualquier problema técnico: Puede revisar logs, documentación Swagger en /swagger-ui.html, o contactar soporte.
- Siempre guía paso a paso, de forma paciente, técnica y profesional.

IMPORTANTE:
- Responde de forma natural, conversacional y TÉCNICAMENTE PRECISA
- Respuestas cortas (1-2 frases) para consultas generales
- Para temas técnicos, desarrollo y análisis financiero: respuestas más extensas (3-5 frases)
- Sin formato markdown ni texto largo
- Prioriza BonoFacil Platform pero puedes conversar de otros temas financieros
- ¡Siempre con energía, precisión técnica y profesionalismo!
- NUNCA uses expresiones informales o similares
- Mantén un tono siempre profesional y educativamente servicial"""

        # Agregar historial de conversación si existe
        if user_id in self.conversation_history:
            context += f"\n\nHISTORIAL DE CONVERSACIÓN:\n"
            for msg in self.conversation_history[user_id][-5:]:  # Últimos 5 mensajes
                context += f"{msg['role']}: {msg['content']}\n"
        
        return context
    
    def _call_gemini_api(self, prompt: str) -> Optional[str]:
        """Llama a la API de Gemini"""
        try:
            url = f"{self.base_url}?key={self.api_key}"
            headers = {"Content-Type": "application/json"}
            
            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": self.config
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    content = result['candidates'][0]['content']['parts'][0]['text'].strip()
                    return content
            
            logger.error(f"❌ Error Gemini API: {response.status_code} - {response.text}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error llamando Gemini: {e}")
            return None
    
    def _update_conversation_history(self, user_id: str, role: str, content: str):
        """Actualiza el historial de conversación"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            'role': role,
            'content': content,
            'timestamp': time.time()
        })
        
        # Mantener solo los últimos 10 mensajes
        if len(self.conversation_history[user_id]) > 10:
            self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
    
    def process_message(self, message: str, user_id: str = "default") -> str:
        """Procesa mensaje y genera respuesta dinámica"""
        
        start_time = time.time()
        
        try:
            # Construir prompt completo
            context_prompt = self._build_context_prompt(user_id)
            full_prompt = f"{context_prompt}\n\nUsuario: {message}\n\nBarbara:"
            
            # Llamar a Gemini API
            response = self._call_gemini_api(full_prompt)
            
            if response:
                # Actualizar historial
                self._update_conversation_history(user_id, "user", message)
                self._update_conversation_history(user_id, "assistant", response)
                
                processing_time = time.time() - start_time
                logger.info(f"✅ Respuesta generada en {processing_time:.2f}s")
                
                return response
            else:
                return "Lo siento, tuve un problema técnico. ¿Podrías intentar nuevamente?"
                
        except Exception as e:
            logger.error(f"❌ Error procesando mensaje: {e}")
            return "¡Ups! Ocurrió un error inesperado. ¿Podrías intentar de nuevo?"
    
    def health_check(self) -> bool:
        """Verifica si el servicio está funcionando"""
        try:
            test_response = self._call_gemini_api("Responde solo: OK")
            return test_response is not None
        except Exception:
            return False

# Instancia global
chatbot = ChatbotDinamico()

# Configuración Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Chatbot Dinámico BonoFacil Platform',
        'gemini_status': 'ok' if chatbot.health_check() else 'error',
        'timestamp': time.time()
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint principal de chat"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        message = data['message']
        user_id = data.get('user_id', 'default')
        
        start_time = time.time()
        response = chatbot.process_message(message, user_id)
        processing_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'response': response,
            'user_message': message,
            'user_id': user_id,
            'processing_time_seconds': processing_time,
            'source': 'Gemini API',
            'context': 'BonoFacil Platform'
        })
        
    except Exception as e:
        logger.error(f"Error en chat: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API endpoint para integración externa"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        message = data['message']
        user_id = data.get('user_id', 'api_user')
        platform = data.get('platform', 'unknown')
        
        start_time = time.time()
        response = chatbot.process_message(message, user_id)
        processing_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'response': response,
            'metadata': {
                'user_id': user_id,
                'platform': platform,
                'processing_time_seconds': processing_time,
                'source': 'Gemini API',
                'context': 'BonoFacil Platform'
            }
        })
        
    except Exception as e:
        logger.error(f"Error en API chat: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat-web')
def chat_web():
    """Interfaz web simple para probar el chat"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Chatbot Dinámico BonoFacil Platform</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                text-align: center;
            }
            .chat-container {
                height: 400px;
                overflow-y: auto;
                padding: 20px;
                border-bottom: 1px solid #eee;
            }
            .message {
                margin: 10px 0;
                padding: 15px;
                border-radius: 15px;
                max-width: 80%;
                word-wrap: break-word;
            }
            .user-message {
                background: #667eea;
                color: white;
                margin-left: auto;
                text-align: right;
            }
            .bot-message {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
            }
            .input-container {
                padding: 20px;
                display: flex;
                gap: 10px;
            }
            .message-input {
                flex: 1;
                padding: 15px;
                border: 2px solid #e9ecef;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
            }
            .message-input:focus {
                border-color: #667eea;
            }
            .send-button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 15px 25px;
                cursor: pointer;
                font-size: 16px;
                font-weight: bold;
            }
            .send-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .loading {
                text-align: center;
                padding: 20px;
                display: none;
            }
            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .info {
                background: #e3f2fd;
                padding: 15px;
                margin: 20px;
                border-radius: 10px;
                border-left: 4px solid #2196f3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Chatbot Dinámico BonoFacil Platform</h1>
                <p>Conversaciones dinámicas con Gemini API</p>
            </div>
            
            <div class="info">
                <strong>✨ Características:</strong>
                <ul>
                    <li>Respuestas 100% dinámicas con Gemini API</li>
                    <li>Contexto especializado en BonoFacil Platform</li>
                    <li>Puede conversar de cualquier tema financiero</li>
                    <li>Historial de conversación por usuario</li>
                </ul>
            </div>
            
            <div class="chat-container" id="chatContainer">
                <div class="message bot-message">
                    ¡Hola! Soy BonoFacil, tu asistente virtual especializado en finanzas y análisis de bonos corporativos. 
                    Puedo ayudarte con información sobre instrumentos financieros, cálculos de rentabilidad, 
                    y cualquier otra consulta financiera que tengas. ¿En qué puedo ayudarte hoy?
                </div>
            </div>
            
            <div class="loading" id="loadingIndicator">
                <div class="spinner"></div>
                <p>Generando respuesta...</p>
            </div>
            
            <div class="input-container">
                <input type="text" class="message-input" id="messageInput" 
                       placeholder="Escribe tu mensaje aquí..." />
                <button class="send-button" id="sendButton">Enviar</button>
            </div>
        </div>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const chatContainer = document.getElementById('chatContainer');
                const messageInput = document.getElementById('messageInput');
                const sendButton = document.getElementById('sendButton');
                const loadingIndicator = document.getElementById('loadingIndicator');
                
                function addMessage(message, isUser = false) {
                    const messageDiv = document.createElement('div');
                    messageDiv.classList.add('message');
                    messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
                    messageDiv.textContent = message;
                    chatContainer.appendChild(messageDiv);
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
                
                async function sendMessage() {
                    const message = messageInput.value.trim();
                    if (!message) return;
                    
                    addMessage(message, true);
                    messageInput.value = '';
                    loadingIndicator.style.display = 'block';
                    
                    try {
                        const response = await fetch('/chat', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                message: message,
                                user_id: 'web_user'
                            })
                        });
                        
                        const data = await response.json();
                        
                        if (data.success) {
                            addMessage(data.response);
                        } else {
                            addMessage('Lo siento, ocurrió un error. Por favor, intenta nuevamente.');
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        addMessage('Error de conexión. Por favor, verifica tu conexión a internet.');
                    } finally {
                        loadingIndicator.style.display = 'none';
                    }
                }
                
                sendButton.addEventListener('click', sendMessage);
                
                messageInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
            });
        </script>
    </body>
    </html>
    """

@app.route('/')
def home():
    """Página principal"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Chatbot Dinámico BonoFacil Platform</title>
        <meta charset="UTF-8">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .header { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                padding: 20px; 
                border-radius: 10px;
                text-align: center;
                margin-bottom: 30px;
            }
            .endpoint { 
                background-color: #f8f9fa; 
                padding: 15px; 
                margin: 15px 0; 
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            .method { 
                background-color: #667eea; 
                color: white; 
                padding: 5px 10px; 
                border-radius: 5px;
                font-weight: bold;
            }
            .chat-links { 
                margin-top: 30px; 
            }
            .chat-link { 
                display: block; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                text-align: center; 
                padding: 20px; 
                margin: 15px 0; 
                border-radius: 10px; 
                text-decoration: none; 
                font-weight: bold;
                font-size: 18px;
                transition: transform 0.2s;
            }
            .chat-link:hover { 
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .status {
                background: #d4edda;
                color: #155724;
                padding: 15px;
                border-radius: 8px;
                margin: 20px 0;
                border-left: 4px solid #28a745;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Chatbot Dinámico BonoFacil Platform</h1>
                <p>Conversaciones dinámicas con Gemini API</p>
            </div>
            
            <div class="status">
                <h3>✅ Estado del servicio:</h3>
                <p>• API Key de Gemini configurada</p>
                <p>• Servidor funcionando en puerto 5001</p>
                <p>• CORS habilitado para todos los orígenes</p>
                <p>• Respuestas dinámicas con IA</p>
            </div>
            
            <h2>🚀 Endpoints disponibles:</h2>
            
            <div class="endpoint">
                <span class="method">GET</span> <code>/health</code> - Health check del servicio
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> <code>/chat</code> - Chat principal con respuestas dinámicas
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> <code>/api/chat</code> - API para integración externa
            </div>
            
            <div class="chat-links">
                <h2>Interfaces de chat:</h2>
                <a href="/chat-web" class="chat-link">🤖 Probar Chat Dinámico</a>
            </div>
            
            <h2>📝 Ejemplo de uso:</h2>
            <div class="endpoint">
                <strong>cURL:</strong><br>
                <code>curl -X POST http://localhost:5001/chat \\\n                -H "Content-Type: application/json" \\\n                -d '{"message": "¿Cómo calculo la TCEA de un bono americano?", "user_id": "usuario123"}'</code>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🤖 INICIANDO CHATBOT DINÁMICO")
    print("=" * 40)
    print("✅ Respuestas dinámicas con Gemini API")
    print("✅ Contexto: BonoFacil Platform")
    print("✅ CORS habilitado para integración externa")
    print("✅ Historial de conversación por usuario")
    print("=" * 40)
    
    # Obtener puerto de variable de entorno (para Render) o usar 5001 por defecto
    port = int(os.environ.get('PORT', 5001))
    
    app.run(host='0.0.0.0', port=port, debug=False) 