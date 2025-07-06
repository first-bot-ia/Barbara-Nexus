#!/usr/bin/env python3
"""
🧪 Test específico para verificar mejoras del chatbot
- Tono cordial y profesional
- No ofrecer restablecer contraseña
- Respuestas más largas para publicaciones
"""

import requests
import json
import time

def test_chatbot_mejoras():
    """Test específico para las mejoras del chatbot"""
    
    base_url = "http://localhost:5001"
    
    print("🧪 TESTEANDO MEJORAS DEL CHATBOT")
    print("=" * 50)
    
    # Test 1: Verificar que NO ofrezca restablecer contraseña
    print("\n1. 🔐 Test: No ofrecer restablecer contraseña")
    response = requests.post(f"{base_url}/chat", json={
        "message": "No puedo iniciar sesión",
        "user_id": "test_user"
    })
    
    if response.status_code == 200:
        data = response.json()
        respuesta = data.get('response', '').lower()
        
        # Verificar que NO contenga palabras relacionadas con restablecer contraseña
        palabras_prohibidas = ['restablecer', 'reset', 'nueva contraseña', 'cambiar contraseña']
        contiene_prohibidas = any(palabra in respuesta for palabra in palabras_prohibidas)
        
        if not contiene_prohibidas:
            print("✅ NO ofrece restablecer contraseña")
            print(f"   Respuesta: {data.get('response', '')}")
        else:
            print("❌ AÚN ofrece restablecer contraseña")
            print(f"   Respuesta: {data.get('response', '')}")
    else:
        print(f"❌ Error en test: {response.status_code}")
    
    # Test 2: Verificar tono cordial (no "uy que lata")
    print("\n2. 😊 Test: Tono cordial y profesional")
    response = requests.post(f"{base_url}/chat", json={
        "message": "La página no carga",
        "user_id": "test_user"
    })
    
    if response.status_code == 200:
        data = response.json()
        respuesta = data.get('response', '').lower()
        
        # Verificar que NO contenga expresiones informales
        expresiones_informales = ['uy que lata', 'que lata', 'qué lata', 'uy', 'lata']
        contiene_informales = any(expresion in respuesta for expresion in expresiones_informales)
        
        if not contiene_informales:
            print("✅ Tono cordial y profesional")
            print(f"   Respuesta: {data.get('response', '')}")
        else:
            print("❌ AÚN usa expresiones informales")
            print(f"   Respuesta: {data.get('response', '')}")
    else:
        print(f"❌ Error en test: {response.status_code}")
    
    # Test 3: Verificar respuestas más largas para publicaciones
    print("\n3. 📝 Test: Respuestas detalladas para publicaciones")
    response = requests.post(f"{base_url}/chat", json={
        "message": "Ayúdame a crear una publicación",
        "user_id": "test_user"
    })
    
    if response.status_code == 200:
        data = response.json()
        respuesta = data.get('response', '')
        
        # Contar frases (separadas por puntos, signos de exclamación o interrogación)
        frases = len([f for f in respuesta.split('.') if f.strip()]) + \
                len([f for f in respuesta.split('!') if f.strip()]) + \
                len([f for f in respuesta.split('?') if f.strip()])
        
        # Contar palabras
        palabras = len(respuesta.split())
        
        print(f"   Respuesta: {respuesta}")
        print(f"   Frases: {frases}")
        print(f"   Palabras: {palabras}")
        
        if palabras >= 20 and frases >= 3:
            print("✅ Respuesta detallada para publicaciones")
        else:
            print("❌ Respuesta muy corta para publicaciones")
    else:
        print(f"❌ Error en test: {response.status_code}")
    
    # Test 4: Verificar que sugiera revisar credenciales
    print("\n4. 🔍 Test: Sugerir revisar credenciales")
    response = requests.post(f"{base_url}/chat", json={
        "message": "No puedo acceder a mi cuenta",
        "user_id": "test_user"
    })
    
    if response.status_code == 200:
        data = response.json()
        respuesta = data.get('response', '').lower()
        
        # Verificar que sugiera revisar credenciales
        sugerencias_credenciales = ['revisar', 'email', 'contraseña', 'credenciales', 'verificar']
        contiene_sugerencias = any(sugerencia in respuesta for sugerencia in sugerencias_credenciales)
        
        if contiene_sugerencias:
            print("✅ Sugiere revisar credenciales")
            print(f"   Respuesta: {data.get('response', '')}")
        else:
            print("❌ NO sugiere revisar credenciales")
            print(f"   Respuesta: {data.get('response', '')}")
    else:
        print(f"❌ Error en test: {response.status_code}")
    
    # Test 5: Verificar tono general cordial
    print("\n5. 🤝 Test: Tono general cordial")
    response = requests.post(f"{base_url}/chat", json={
        "message": "Hola, ¿cómo estás?",
        "user_id": "test_user"
    })
    
    if response.status_code == 200:
        data = response.json()
        respuesta = data.get('response', '')
        
        # Verificar que sea cordial
        palabras_cordiales = ['hola', '¡hola', 'encantada', 'bienvenido', 'ayudar', 'servir']
        es_cordial = any(palabra in respuesta.lower() for palabra in palabras_cordiales)
        
        if es_cordial:
            print("✅ Tono general cordial")
            print(f"   Respuesta: {respuesta}")
        else:
            print("❌ Tono no es cordial")
            print(f"   Respuesta: {respuesta}")
    else:
        print(f"❌ Error en test: {response.status_code}")

if __name__ == "__main__":
    print("🚀 INICIANDO TEST DE MEJORAS DEL CHATBOT")
    print("Asegúrate de que el servidor esté ejecutándose en puerto 5001")
    print("=" * 60)
    
    try:
        test_chatbot_mejoras()
        print("\n🎉 TEST DE MEJORAS COMPLETADO")
        print("=" * 60)
    except Exception as e:
        print(f"❌ Error en test: {e}")
        print("Asegúrate de que el servidor esté ejecutándose") 