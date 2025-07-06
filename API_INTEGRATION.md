# Integración con Barbara NEXUS - API de Razonamiento

## Introducción

Barbara NEXUS ofrece un servicio de razonamiento avanzado que puede ser consumido por cualquier plataforma externa. Esta API permite aprovechar la capacidad de razonamiento de Barbara sin necesidad de implementar toda la lógica en su proyecto.

La API está diseñada para ser flexible y adaptarse a diferentes contextos, permitiendo que las plataformas externas envíen información contextual para mejorar las respuestas.

## Características principales

- **Integración universal**: Se puede integrar con cualquier plataforma (web, móvil, CRM, chatbots)
- **CORS habilitado**: Configurado para aceptar solicitudes desde cualquier origen (*)
- **Transferencia contextual**: Posibilidad de enviar contexto específico de la plataforma
- **Métricas de IA**: Información sobre el proceso de razonamiento (opcional)

## Endpoint de la API

```
POST /api/reasoning
```

### Parámetros de solicitud

| Parámetro      | Tipo     | Requerido | Descripción                                   |
|----------------|----------|-----------|-----------------------------------------------|
| message        | string   | Sí        | El mensaje del usuario                        |
| user_id        | string   | No        | Identificador único del usuario               |
| platform_name  | string   | No        | Nombre de la plataforma que realiza la llamada|
| context        | object   | No        | Datos contextuales para Barbara              |

### Ejemplo de solicitud

```json
{
  "message": "Hola, necesito información sobre SOAT",
  "user_id": "user-123",
  "platform_name": "MiAplicación",
  "context": {
    "platform_type": "web",
    "user_preferences": {
      "vehicle_type": "auto",
      "language": "es"
    },
    "session_data": {
      "previous_topics": ["seguros", "cotizaciones"]
    }
  }
}
```

### Respuesta

| Campo             | Tipo     | Descripción                                   |
|-------------------|----------|-----------------------------------------------|
| success           | boolean  | Estado de la operación                        |
| response          | string   | Respuesta de Barbara                          |
| processing_time_seconds | number | Tiempo de procesamiento en segundos       |
| request_id        | string   | Identificador único de la solicitud           |
| metrics           | object   | Métricas opcionales del proceso de razonamiento |

### Ejemplo de respuesta

```json
{
  "success": true,
  "response": "¡Hola! Soy Barbara, asesora de seguros. El SOAT es un seguro obligatorio para vehículos en Perú que cubre daños personales en accidentes de tránsito. ¿Te gustaría recibir una cotización para tu vehículo?",
  "processing_time_seconds": 0.234,
  "request_id": "req-1625184000-1234",
  "metrics": {
    "creativity_level": 0.7,
    "empathy_level": 0.85,
    "personality_mode": "helpful_professional",
    "thoughts": [
      "El usuario está interesado en información general sobre SOAT",
      "Debo explicar de manera clara y concisa qué es el SOAT",
      "Ofrecer cotización puede ser un buen siguiente paso"
    ]
  }
}
```

## Ejemplos de integración

### JavaScript / Frontend

```javascript
async function consultarBarbara(mensaje, usuarioId) {
  try {
    const respuesta = await fetch('https://tu-servidor/api/reasoning', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: mensaje,
        user_id: usuarioId,
        platform_name: 'Web App Cliente',
        context: {
          platform_type: 'web',
          user_agent: navigator.userAgent
        }
      })
    });
    
    return await respuesta.json();
  } catch (error) {
    console.error('Error al consultar a Barbara:', error);
    return { success: false, error: error.message };
  }
}

// Uso
consultarBarbara('Necesito un SOAT para mi auto', 'cliente123')
  .then(data => {
    console.log('Respuesta de Barbara:', data.response);
    
    // Mostrar la respuesta en la interfaz
    document.getElementById('respuesta').textContent = data.response;
  });
```

### Python / Backend

```python
import requests
import json

def consultar_barbara(mensaje, usuario_id, contexto=None):
    """
    Consulta a Barbara NEXUS desde cualquier aplicación Python
    
    Args:
        mensaje (str): Mensaje del usuario
        usuario_id (str): ID del usuario
        contexto (dict, optional): Contexto adicional
        
    Returns:
        dict: Respuesta de Barbara
    """
    url = "https://tu-servidor/api/reasoning"
    
    datos = {
        "message": mensaje,
        "user_id": usuario_id,
        "platform_name": "Python Backend",
        "context": contexto or {}
    }
    
    try:
        respuesta = requests.post(
            url, 
            json=datos,
            headers={"Content-Type": "application/json"}
        )
        
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            return {"success": False, "error": f"Error {respuesta.status_code}: {respuesta.text}"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

# Ejemplo de uso
resultado = consultar_barbara(
    "¿Cuánto cuesta un SOAT para taxi?",
    "usuario-456",
    {
        "platform_type": "crm",
        "vehicle_data": {
            "type": "taxi",
            "brand": "Toyota",
            "year": 2018
        }
    }
)

print(f"Respuesta: {resultado['response']}")
```

### PHP / Web

```php
<?php
/**
 * Consulta a Barbara NEXUS desde PHP
 */
function consultarBarbara($mensaje, $usuarioId, $contexto = []) {
    $url = "https://tu-servidor/api/reasoning";
    
    $datos = [
        "message" => $mensaje,
        "user_id" => $usuarioId,
        "platform_name" => "PHP App",
        "context" => $contexto
    ];
    
    $opciones = [
        'http' => [
            'header' => "Content-type: application/json\r\n",
            'method' => 'POST',
            'content' => json_encode($datos)
        ]
    ];
    
    $contexto = stream_context_create($opciones);
    $resultado = file_get_contents($url, false, $contexto);
    
    if ($resultado === FALSE) {
        return ["success" => false, "error" => "Error al conectar con Barbara"];
    }
    
    return json_decode($resultado, true);
}

// Ejemplo de uso
$respuesta = consultarBarbara(
    "Necesito cotizar SOAT para mi moto",
    "cliente-789",
    [
        "platform_type" => "web_php",
        "user_preferences" => [
            "vehicle_type" => "moto"
        ]
    ]
);

if ($respuesta["success"]) {
    echo "Barbara dice: " . $respuesta["response"];
} else {
    echo "Error: " . $respuesta["error"];
}
?>
```

## Recomendaciones

1. **Persistencia de IDs**: Mantener el mismo `user_id` para un mismo usuario a través de diferentes interacciones
2. **Contexto relevante**: Enviar solo datos contextuales que puedan ser útiles para mejorar las respuestas
3. **Manejo de errores**: Implementar un adecuado manejo de excepciones y reintentos en caso de fallos
4. **Caché**: Considerar almacenar en caché ciertas respuestas para mejorar el rendimiento
5. **Monitoreo**: Implementar un sistema de monitoreo para las llamadas a la API

## Soporte

Para cualquier consulta sobre la integración con Barbara NEXUS, contacte a nuestro equipo de soporte.

---

*Documentación generada para Barbara NEXUS - Neural Experience Understanding System v3.1* 