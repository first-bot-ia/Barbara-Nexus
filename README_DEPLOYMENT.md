# 🤖 Barbara - Chatbot BonoFacil Platform

## 🚀 Despliegue en Render

### 1. Preparación del Repositorio

Asegúrate de tener estos archivos en tu repositorio:
- `chatbot_dinamico.py` - Código principal del chatbot
- `requirements.txt` - Dependencias de Python
- `render.yaml` - Configuración de Render
- `Procfile` - Comando de inicio
- `runtime.txt` - Versión de Python

### 2. Configuración en Render

1. **Crear cuenta en Render**: Ve a [render.com](https://render.com) y crea una cuenta
2. **Conectar repositorio**: Conecta tu repositorio de GitHub/GitLab
3. **Crear nuevo servicio web**:
   - Tipo: Web Service
   - Nombre: `barbara-bonofacil-chatbot`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

### 3. Variables de Entorno

En Render, configura estas variables de entorno:

#### Variables Requeridas:
- `GEMINI_API_KEY`: Tu clave de API de Google Gemini (obligatoria)

#### Variables Opcionales:
- `PYTHON_VERSION`: 3.9.16 (por defecto)
- `PORT`: Puerto del servidor (Render asigna automáticamente)

#### Cómo configurar en Render:
1. Ve a tu dashboard de Render
2. Selecciona tu servicio web
3. Ve a la pestaña "Environment"
4. Agrega la variable `GEMINI_API_KEY` con tu API key de Gemini

#### Obtener API Key de Gemini:
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una nueva API key
3. Copia la key y configúrala en Render

### 4. Despliegue

Render detectará automáticamente la configuración y desplegará tu chatbot. La URL será algo como:
`https://barbara-bonofacil-chatbot.onrender.com`

---

## 🔗 Conexión desde Otras Plataformas

### API Endpoints Disponibles

Tu chatbot expone estos endpoints:

#### 1. Health Check
```http
GET https://tu-app.onrender.com/health
```

#### 2. Chat Principal
```http
POST https://tu-app.onrender.com/chat
Content-Type: application/json

{
  "message": "¿Cómo calculo la TCEA de un bono?",
  "user_id": "usuario123"
}
```

#### 3. API para Integración Externa
```http
POST https://tu-app.onrender.com/api/chat
Content-Type: application/json

{
  "message": "¿Qué es la duración de un bono?",
  "user_id": "usuario456",
  "platform": "web"
}
```

### Ejemplos de Integración

#### JavaScript/HTML
```html
<!DOCTYPE html>
<html>
<head>
    <title>Chat con Barbara</title>
</head>
<body>
    <div id="chat-container"></div>
    <input type="text" id="message-input" placeholder="Escribe tu mensaje...">
    <button onclick="sendMessage()">Enviar</button>

    <script>
        async function sendMessage() {
            const message = document.getElementById('message-input').value;
            const response = await fetch('https://tu-app.onrender.com/chat', {
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
                document.getElementById('chat-container').innerHTML += 
                    `<p><strong>Barbara:</strong> ${data.response}</p>`;
            }
        }
    </script>
</body>
</html>
```

#### React
```jsx
import React, { useState } from 'react';

function ChatComponent() {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');

    const sendMessage = async () => {
        try {
            const response = await fetch('https://tu-app.onrender.com/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: inputMessage,
                    user_id: 'react_user'
                })
            });
            
            const data = await response.json();
            if (data.success) {
                setMessages([...messages, 
                    { type: 'user', content: inputMessage },
                    { type: 'barbara', content: data.response }
                ]);
                setInputMessage('');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div>
            <div className="messages">
                {messages.map((msg, index) => (
                    <div key={index} className={msg.type}>
                        <strong>{msg.type === 'barbara' ? 'Barbara' : 'Tú'}:</strong> {msg.content}
                    </div>
                ))}
            </div>
            <input 
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Escribe tu mensaje..."
            />
            <button onClick={sendMessage}>Enviar</button>
        </div>
    );
}
```

#### Python
```python
import requests
import json

def chat_with_barbara(message, user_id="python_user"):
    url = "https://tu-app.onrender.com/chat"
    headers = {"Content-Type": "application/json"}
    data = {
        "message": message,
        "user_id": user_id
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Ejemplo de uso
response = chat_with_barbara("¿Cómo funciona la amortización americana?")
print(f"Barbara: {response['response']}")
```

#### Node.js
```javascript
const axios = require('axios');

async function chatWithBarbara(message, userId = 'node_user') {
    try {
        const response = await axios.post('https://tu-app.onrender.com/chat', {
            message: message,
            user_id: userId
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        return response.data;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// Ejemplo de uso
chatWithBarbara("¿Qué es la convexidad de un bono?")
    .then(data => {
        if (data.success) {
            console.log(`Barbara: ${data.response}`);
        }
    });
```

#### PHP
```php
<?php
function chatWithBarbara($message, $userId = 'php_user') {
    $url = 'https://tu-app.onrender.com/chat';
    $data = [
        'message' => $message,
        'user_id' => $userId
    ];
    
    $options = [
        'http' => [
            'header' => "Content-type: application/json\r\n",
            'method' => 'POST',
            'content' => json_encode($data)
        ]
    ];
    
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    
    return json_decode($result, true);
}

// Ejemplo de uso
$response = chatWithBarbara("¿Cómo se calcula el TREA?");
if ($response['success']) {
    echo "Barbara: " . $response['response'];
}
?>
```

### Integración con Chatbots Existentes

#### Dialogflow Webhook
```javascript
// En tu webhook de Dialogflow
app.post('/webhook', (req, res) => {
    const userMessage = req.body.queryResult.queryText;
    
    // Enviar a Barbara
    fetch('https://tu-app.onrender.com/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: userMessage,
            user_id: 'dialogflow_user'
        })
    })
    .then(response => response.json())
    .then(data => {
        res.json({
            fulfillmentText: data.response,
            fulfillmentMessages: [{
                text: { text: [data.response] }
            }]
        });
    });
});
```

#### Botpress
```javascript
// En tu hook de Botpress
bp.events.on('message', async (event) => {
    if (event.type === 'text') {
        const response = await fetch('https://tu-app.onrender.com/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: event.payload.text,
                user_id: event.target
            })
        });
        
        const data = await response.json();
        if (data.success) {
            bp.events.replyToEvent({
                botId: event.botId,
                channel: event.channel,
                target: event.target,
                payload: {
                    type: 'text',
                    text: data.response
                }
            });
        }
    }
});
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno Adicionales
```bash
# Para desarrollo local
GEMINI_API_KEY=tu_api_key_aqui
FLASK_ENV=development
FLASK_DEBUG=1

# Para producción
GEMINI_API_KEY=tu_api_key_aqui
FLASK_ENV=production
FLASK_DEBUG=0
```

### Monitoreo y Logs
- Render proporciona logs automáticos
- Endpoint `/health` para monitoreo de salud
- Métricas de tiempo de respuesta incluidas en las respuestas

### Escalabilidad
- Render escala automáticamente según la demanda
- El plan gratuito incluye 750 horas/mes
- Para mayor tráfico, considera el plan pago

---

## 🚨 Consideraciones Importantes

1. **Rate Limiting**: La API gratuita de Gemini tiene límites de 50 requests/día
2. **CORS**: Configurado para permitir todos los orígenes
3. **Seguridad**: Considera implementar autenticación para uso en producción
4. **Backup**: Mantén respaldos de tu configuración y código

---

## 📞 Soporte

Para problemas técnicos o consultas sobre la integración, revisa:
- Logs en Render Dashboard
- Documentación de Gemini API
- Issues en el repositorio del proyecto 