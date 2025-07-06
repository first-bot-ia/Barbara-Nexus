# Configuración de Variables de Entorno

## Variables Requeridas

### GEMINI_API_KEY
- **Descripción**: API Key de Google Gemini para generar respuestas dinámicas
- **Obligatoria**: Sí
- **Formato**: String
- **Ejemplo**: `AIzaSyC...`

## Variables Opcionales

### PORT
- **Descripción**: Puerto donde se ejecutará el servidor
- **Obligatoria**: No
- **Valor por defecto**: 5001
- **Formato**: Número entero

### DEBUG
- **Descripción**: Modo debug para desarrollo
- **Obligatoria**: No
- **Valor por defecto**: False
- **Formato**: Boolean

## Configuración en Render

1. Ve a tu dashboard de Render
2. Selecciona tu servicio web
3. Ve a la pestaña "Environment"
4. Agrega las variables:
   - `GEMINI_API_KEY`: Tu API key de Gemini
   - `PORT`: 10000 (Render asigna automáticamente)

## Configuración Local

1. Crea un archivo `.env` en la raíz del proyecto
2. Agrega las variables:
```
GEMINI_API_KEY=tu_api_key_aqui
PORT=5001
DEBUG=False
```

## Obtener API Key de Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una nueva API key
3. Copia la key y configúrala en las variables de entorno 