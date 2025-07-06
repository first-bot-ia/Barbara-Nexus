# Barbara Nexus - Módulo AventuraPe

Este módulo integra las capacidades de Barbara Nexus con AventuraPe, permitiendo generar contenido para publicaciones de aventuras turísticas.

## Características

- Generación de título y descripción para publicaciones de aventuras
- Filtrado de contenido inapropiado
- Integración con Gemini AI para generación de contenido
- API REST para interactuar con el servicio

## Configuración

### 1. Configurar API Key de Gemini

Debes tener una API Key de Gemini AI. Puedes configurarla como variable de entorno en el archivo `.env`:

```bash
# Copia el archivo de ejemplo
cp env.aventurape.example .env

# Edita el archivo con tu API key
nano .env
```

### 2. Configuración del módulo

El archivo `config/aventurape_config.py` contiene la configuración del módulo:

- `AVENTURAPE_API_URL`: URL base de la API de AventuraPe (configurable por variable de entorno)
- `INAPPROPRIATE_WORDS`: Lista de palabras inapropiadas a filtrar
- `GEMINI_CONFIG`: Configuración para el modelo de Gemini
- `CONTENT_INSTRUCTIONS`: Instrucciones para generar contenido

Para instrucciones detalladas de instalación, configuración y solución de problemas, consulta el archivo `AVENTURAPE_SETUP.md`.

## Uso de la API

### Generar contenido para una publicación

**Endpoint**: `POST /aventurape/generate-content`

**Body**:
```json
{
    "context": "Descripción de la aventura por el usuario"
}
```

**Respuesta exitosa**:
```json
{
    "success": true,
    "content": {
        "title": "Título generado",
        "description": "Descripción generada"
    }
}
```

### Verificar estado del servicio

**Endpoint**: `GET /aventurape/health`

**Respuesta**:
```json
{
    "status": "healthy",
    "services": {
        "gemini": "ok"
    },
    "aventurape_api": {
        "url": "http://localhost:8080"
    }
}
```

## Integración con AventuraPe Frontend

Para integrar con el frontend de AventuraPe, debes hacer una solicitud al endpoint `/aventurape/generate-content` desde tu componente Vue.js, proporcionando el contexto de la aventura escrito por el usuario.

### Ejemplo de uso en Vue.js:

```javascript
async function generateContent() {
  const response = await fetch('http://localhost:5000/aventurape/generate-content', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      context: "Quiero una aventura de trekking por las montañas con vistas impresionantes y actividades como rappel"
    })
  });
  
  const data = await response.json();
  
  if (data.success) {
    // Usar título y descripción generados
    console.log(data.content.title);
    console.log(data.content.description);
  }
}
``` 