# Configuración del Módulo AventuraPe para Barbara-Nexus

Este documento describe los pasos necesarios para instalar, configurar y ejecutar el módulo AventuraPe en Barbara-Nexus.

## Requisitos previos

1. Python 3.8 o superior
2. Barbara-Nexus instalado y funcionando
3. API key de Gemini AI
4. Servidor AventuraPe-Backend ejecutándose

## Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements_aventurape.txt
```

### 2. Configurar variables de entorno

Copia el archivo `env.aventurape.example` a `.env` y edita las variables según tu entorno:

```bash
cp env.aventurape.example .env
```

Edita el archivo `.env` con tu editor preferido:

```bash
# Ejemplo de configuración
GEMINI_API_KEY=tu_api_key_aqui
AVENTURAPE_API_URL=http://localhost:8080
```

## Verificación de la instalación

Para verificar que el módulo AventuraPe está correctamente instalado y configurado, ejecuta:

```bash
python app_simple.py
```

Luego, abre en tu navegador:

```
http://localhost:5000/aventurape/health
```

Deberías ver una respuesta JSON con el estado de salud del servicio.

## Generación de contenido de ejemplo

Para probar la generación de contenido, puedes usar la siguiente solicitud curl:

```bash
curl -X POST http://localhost:5000/aventurape/generate-content \
    -H "Content-Type: application/json" \
    -d '{"context": "Quiero una aventura de trekking por las montañas de los Andes, con vistas a lagos glaciares y la posibilidad de observar cóndores volando."}'
```

## Integración con AventuraPe-web

Para integrar este módulo con AventuraPe-web, sigue estos pasos:

1. Asegúrate de que Barbara-Nexus esté ejecutándose y accesible desde AventuraPe-web
2. Configura la URL de Barbara-Nexus en AventuraPe-web
3. Implementa el botón "IA EXPERIENCE" en AventuraPe-web

### Ejemplo de código Vue.js para AventuraPe-web

```javascript
async function generateContent() {
  try {
    this.isLoading = true;
    const response = await axios.post('http://localhost:5000/aventurape/generate-content', {
      context: this.adventureContext
    });
    
    if (response.data.success) {
      this.title = response.data.content.title;
      this.description = response.data.content.description;
      this.showResults = true;
    } else {
      this.error = response.data.error || "Error al generar contenido";
    }
  } catch (error) {
    console.error("Error:", error);
    this.error = "Error de conexión con el servicio de IA";
  } finally {
    this.isLoading = false;
  }
}
```

## Solución de problemas

### Error "Servicio de IA no configurado"

Asegúrate de que la variable de entorno `GEMINI_API_KEY` está correctamente configurada.

### Error de CORS

Si encuentras errores de CORS al llamar desde AventuraPe-web, verifica:

1. Que `flask-cors` esté instalado
2. Que la configuración CORS en `presentation/aventurape_endpoints.py` incluya el origen de AventuraPe-web

### Error de conexión con AventuraPe-Backend

Verifica que el servidor de AventuraPe-Backend esté ejecutándose y sea accesible desde Barbara-Nexus.

## Contacto y soporte

Si tienes problemas o preguntas, contacta a [correo@ejemplo.com](mailto:correo@ejemplo.com). 