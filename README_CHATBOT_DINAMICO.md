# 🤖 Chatbot Dinámico Aventura PE

Chatbot con respuestas 100% dinámicas usando Gemini API, especializado en el contexto de Aventura PE.

## ✨ Características

- **Respuestas dinámicas**: Generadas por Gemini API en tiempo real
- **Contexto especializado**: Enfocado en Aventura PE y turismo de aventura en Perú
- **Historial de conversación**: Mantiene contexto por usuario
- **Integración externa**: Endpoints para llamadas desde cualquier plataforma
- **Interfaz web**: Chat visual para pruebas
- **CORS habilitado**: Compatible con cualquier frontend

## 🚀 Instalación y Uso

### 1. Verificar dependencias
```bash
pip install flask flask-cors requests python-dotenv
```

### 2. Configurar API Key
Asegúrate de que tu archivo `.environment` contenga:
```
GEMINI_API_KEY=tu_api_key_aqui
```

### 3. Ejecutar el chatbot
```bash
python chatbot_dinamico.py
```

### 4. Probar el servicio
```bash
python test_chatbot_dinamico.py
```

## 🌐 Endpoints Disponibles

### Health Check
```bash
GET /health
```
Verifica el estado del servicio y la conexión con Gemini API.

### Chat Principal
```bash
POST /chat
```
Endpoint principal para conversaciones dinámicas.

**Body:**
```json
{
    "message": "¿Qué aventuras recomiendas en Cusco?",
    "user_id": "usuario123"
}
```

**Respuesta:**
```json
{
    "success": true,
    "response": "¡Excelente elección! Cusco es uno de los mejores destinos para aventuras en Perú...",
    "user_message": "¿Qué aventuras recomiendas en Cusco?",
    "user_id": "usuario123",
    "processing_time_seconds": 1.23,
    "source": "Gemini API",
    "context": "Aventura PE"
}
```

### API Externa
```bash
POST /api/chat
```
Endpoint para integración con otras plataformas.

**Body:**
```json
{
    "message": "¿Cuáles son los mejores destinos para trekking?",
    "user_id": "usuario_externo",
    "platform": "mi_aplicacion"
}
```

### Interfaz Web
```
GET /chat-web
```
Interfaz visual para probar el chatbot directamente en el navegador.

## 🔧 Integración con Otras Plataformas

### JavaScript/Frontend
```javascript
async function enviarMensaje(mensaje, userId) {
    const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: mensaje,
            user_id: userId
        })
    });
    
    const data = await response.json();
    return data.response;
}

// Ejemplo de uso
const respuesta = await enviarMensaje("¿Qué aventuras hay en Machu Picchu?", "usuario123");
console.log(respuesta);
```

### Python
```python
import requests

def enviar_mensaje(mensaje, user_id):
    response = requests.post('http://localhost:5000/chat', 
                           json={'message': mensaje, 'user_id': user_id})
    return response.json()['response']

# Ejemplo de uso
respuesta = enviar_mensaje("¿Qué aventuras hay en Machu Picchu?", "usuario123")
print(respuesta)
```

### cURL
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué aventuras recomiendas en Cusco?", "user_id": "usuario123"}'
```

## 🎯 Contexto de Aventura PE

El chatbot está configurado con un contexto especializado que incluye:

- **Conocimiento sobre Perú**: Destinos turísticos, geografía, cultura
- **Aventuras y actividades**: Trekking, montañismo, ecoturismo
- **Planificación de viajes**: Recomendaciones, itinerarios, consejos
- **Flexibilidad**: Puede conversar de cualquier tema, pero prioriza Aventura PE

### Ejemplos de conversación:

**Usuario**: "¿Qué aventuras recomiendas en Cusco?"
**Barbara**: "¡Cusco es fantástico para aventuras! Te recomiendo el Camino Inca a Machu Picchu, una experiencia única de 4 días. También está el Valle Sagrado con rutas de trekking más cortas, y la montaña de 7 colores para senderismo de un día. ¿Qué tipo de aventura te interesa más?"

**Usuario**: "¿Cuánto tiempo necesito para visitar Machu Picchu?"
**Barbara**: "Para Machu Picchu, te recomiendo al menos 2-3 días. Un día para el viaje desde Cusco y la visita a las ruinas, y tiempo extra para aclimatarte a la altura. Si quieres hacer el Camino Inca, necesitarás 4-5 días. ¿Prefieres una visita rápida o una experiencia más completa?"

## 🔍 Diferencias con el Sistema Anterior

| Característica | Sistema Anterior | Chatbot Dinámico |
|---|---|---|
| Respuestas | Preconfiguradas (if/else) | **Generadas por Gemini API** |
| Contexto | Seguros | **Aventura PE** |
| Flexibilidad | Limitada | **Alta - conversa de cualquier tema** |
| Integración | Básica | **Completa - cualquier plataforma** |
| Historial | No | **Por usuario** |
| Tiempo de respuesta | Instantáneo | **1-3 segundos** |

## 🧪 Testing

Ejecuta los tests para verificar que todo funciona:

```bash
python test_chatbot_dinamico.py
```

Los tests verifican:
- ✅ Health check del servicio
- ✅ Chat básico con respuestas dinámicas
- ✅ API externa para integración
- ✅ Conversación con contexto mantenido
- ✅ Manejo de errores

## 🚨 Solución de Problemas

### Error: "GEMINI_API_KEY es requerida"
- Verifica que tu archivo `.environment` contenga la API key
- Asegúrate de que el archivo esté en el directorio correcto

### Error: "Gemini API error"
- Verifica que tu API key sea válida
- Comprueba tu conexión a internet
- Revisa los logs para más detalles

### Respuestas lentas
- Es normal, Gemini API toma 1-3 segundos
- Las respuestas dinámicas requieren más tiempo que las preconfiguradas

### Error de CORS
- El servidor ya tiene CORS habilitado para todos los orígenes
- Si persiste, verifica que estés usando el puerto correcto (5000)

## 📊 Métricas y Monitoreo

El chatbot incluye métricas automáticas:
- **Tiempo de procesamiento**: Medido en cada respuesta
- **Estado de Gemini API**: Verificado en health check
- **Historial de conversación**: Mantenido por usuario
- **Logs detallados**: Para debugging

## 🎉 ¡Listo para Usar!

Tu chatbot dinámico está configurado y listo para:
- ✅ Generar respuestas inteligentes con Gemini API
- ✅ Mantener contexto de conversación
- ✅ Integrarse con cualquier plataforma
- ✅ Proporcionar información especializada sobre Aventura PE

¡Disfruta de conversaciones dinámicas y naturales! 