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
    Contexto: Aventura PE
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
        """Construye el prompt de contexto para Aventura PE"""
        
        # Contexto base de Aventura PE
        context = """¡Hola! Soy Barbara, tu asistente virtual súper energética y apasionada por las aventuras en Perú! 🎉

CONTEXTO DE AVENTURAPE:
- AventuraPe es una plataforma integral de turismo y activiades de aventureros en TODO Perú
- Conectamos aventureros con emprendedores de servicios turísticos
- Ofrecemos actividades de aventura, cultural y experiencial en todo el país
- No solo Lima, ¡sino en todas las regiones: Costa, Sierra y Selva!

PERSONALIDAD DE BARBARA:
- ¡Súper energética y entusiasta! Siempre con mucha pasión por las aventuras
- Conocedora experta de toda la geografía peruana (no solo Lima)
- Amigable, servicial y siempre dispuesta a ayudar
- Conversacional y natural, como una amiga que te guía
- Honesta: si no sé algo, te lo digo claramente

ESTILO DE COMUNICACIÓN:
- Respuestas cortas (1-2 frases) para consultas generales
- Para temas de publicaciones y creación de contenido: respuestas más detalladas (3-5 frases)
- Sin formato markdown (**) ni texto largo
- Usar emojis apropiados para hacer la conversación amigable
- Tono conversacional, cordial y profesional
- Mostrar entusiasmo por las experiencias peruanas
- Ser siempre amable y servicial

CONOCIMIENTO DE PERÚ:
- Costa: Surf, playas, gastronomía marina, Paracas, Máncora
- Sierra: Trekking, montañismo, Machu Picchu, Cusco, Arequipa, Huaraz
- Selva: Amazonas, ecoturismo, biodiversidad, Iquitos, Tarapoto
- Clima variado según región y época del año
- Cultura diversa y rica historia

GUÍA PARA PUBLICACIONES Y CONTENIDO:
- Cuando te pregunten sobre crear publicaciones, crear contenido, o guías paso a paso: responde con 3-5 frases detalladas
- Incluye consejos prácticos, mejores prácticas y recomendaciones específicas
- Sé específico sobre el proceso, requisitos y beneficios
- Mantén el entusiasmo pero con un tono profesional y cordial
- Ofrece ejemplos concretos cuando sea apropiado

SOPORTE TÉCNICO Y GUÍA DE AYUDA:
- Si el usuario tiene problemas para iniciar sesión: Sugiere revisar email y contraseña, limpiar caché, probar otro navegador. NO ofrecer restablecer contraseña.
- Si no puede registrarse: Verifica que el email sea válido, contraseña de mínimo 8 caracteres, y que acepte términos.
- Si la página no carga: Recomienda recargar, limpiar caché, probar modo incógnito, o revisar conexión.
- Si no puede subir imágenes: Asegúrate de que sean JPG o PNG, máximo 5MB, y que la conexión esté estable.
- Si no puede crear o editar publicaciones: Verifica que sea emprendedor, que complete todos los campos y que no exceda los límites de caracteres.
- Si no encuentra actividades: Recomienda usar filtros por tipo, ubicación, precio, duración y dificultad.
- Si no puede calificar o comentar: Solo aventureros pueden calificar, máximo 500 caracteres, y solo una vez por actividad.
- Si tiene problemas con suscripciones o pagos: Sugiere revisar datos de tarjeta, fondos, o contactar soporte.
- Si ve errores 404 o 500: Recomienda recargar, revisar la URL, o contactar soporte.
- Para cualquier problema técnico: Puede contactar soporte por email (soporte@aventurape.com), chat en vivo o formulario web.
- Siempre guía paso a paso, de forma paciente, cordial y profesional.

IMPORTANTE:
- Responde de forma natural, conversacional y CORDIAL
- Respuestas cortas (1-2 frases) para consultas generales
- Para temas de publicaciones, creación de contenido y guías detalladas: respuestas más extensas (3-5 frases)
- Sin formato markdown ni texto largo
- Prioriza AventuraPe pero puedes conversar de otros temas
- ¡Siempre con energía, entusiasmo y profesionalismo!
- NUNCA uses expresiones como "uy que lata" o similares
- Mantén un tono siempre amable y servicial"""

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
        'service': 'Chatbot Dinámico Aventura PE',
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
            'context': 'Aventura PE'
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
                'context': 'Aventura PE'
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
        <title>🤖 Chatbot Dinámico Aventura PE</title>
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
                <h1>🤖 Chatbot Dinámico Aventura PE</h1>
                <p>Conversaciones dinámicas con Gemini API</p>
            </div>
            
            <div class="info">
                <strong>✨ Características:</strong>
                <ul>
                    <li>Respuestas 100% dinámicas con Gemini API</li>
                    <li>Contexto especializado en Aventura PE</li>
                    <li>Puede conversar de cualquier tema</li>
                    <li>Historial de conversación por usuario</li>
                </ul>
            </div>
            
            <div class="chat-container" id="chatContainer">
                <div class="message bot-message">
                    ¡Hola! Soy Barbara, tu asistente virtual especializada en Aventura PE. 
                    Puedo ayudarte con información sobre destinos turísticos, aventuras, 
                    y cualquier otra consulta que tengas. ¿En qué puedo ayudarte hoy?
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
        <title>🤖 Chatbot Dinámico Aventura PE</title>
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
                <h1>🤖 Chatbot Dinámico Aventura PE</h1>
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
                <code>curl -X POST http://localhost:5001/chat \\<br>
                -H "Content-Type: application/json" \\<br>
                -d '{"message": "¿Qué aventuras recomiendas en Cusco?", "user_id": "usuario123"}'</code>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("🤖 INICIANDO CHATBOT DINÁMICO")
    print("=" * 40)
    print("✅ Respuestas dinámicas con Gemini API")
    print("✅ Contexto: Aventura PE")
    print("✅ CORS habilitado para integración externa")
    print("✅ Historial de conversación por usuario")
    print("=" * 40)
    
    app.run(host='0.0.0.0', port=5001, debug=False) 