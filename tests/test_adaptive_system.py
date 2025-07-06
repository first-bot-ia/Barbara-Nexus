#!/usr/bin/env python3
"""
🧠 TEST SISTEMA ADAPTATIVO DE BARBARA
Este script demuestra cómo Barbara se adapta a diferentes plataformas
"""

import requests
import json
import time
import sys
import os

# Agregar el directorio raíz al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_adaptive_system():
    """Test del sistema adaptativo de Barbara"""
    
    print("🧠 TEST SISTEMA ADAPTATIVO DE BARBARA")
    print("=" * 60)
    print("Este test demuestra cómo Barbara se adapta a diferentes plataformas")
    print("=" * 60)
    
    # URL del servicio
    API_URL = "http://localhost:5000/api/reasoning"
    
    # Casos de prueba para diferentes plataformas
    test_cases = [
        {
            "name": "🛒 E-commerce",
            "platform": "ecommerce",
            "messages": [
                "¿Tienes productos en oferta?",
                "Quiero comprar algo para mi auto",
                "¿Cuánto cuesta el envío?"
            ]
        },
        {
            "name": "🎧 Servicio al Cliente",
            "platform": "customer_service",
            "messages": [
                "Tengo un problema con mi cuenta",
                "Necesito ayuda urgente",
                "¿Pueden resolver mi queja?"
            ]
        },
        {
            "name": "📚 Educativa",
            "platform": "educational",
            "messages": [
                "¿Puedes explicarme cómo funciona esto?",
                "Tengo dudas sobre el tema",
                "¿Hay algún curso disponible?"
            ]
        },
        {
            "name": "🏥 Salud",
            "platform": "healthcare",
            "messages": [
                "Tengo síntomas de dolor de cabeza",
                "¿Cuándo puedo agendar una cita?",
                "Necesito información médica"
            ]
        },
        {
            "name": "💰 Financiera",
            "platform": "financial",
            "messages": [
                "¿Cuál es el saldo de mi cuenta?",
                "Quiero información sobre inversiones",
                "¿Puedo solicitar un préstamo?"
            ]
        },
        {
            "name": "🎮 Entretenimiento",
            "platform": "entertainment",
            "messages": [
                "¿Qué juegos recomiendas?",
                "Quiero divertirme un rato",
                "¿Hay contenido nuevo disponible?"
            ]
        },
        {
            "name": "📱 Redes Sociales",
            "platform": "social_media",
            "messages": [
                "¿Cómo puedo subir una foto?",
                "Quiero conectar con amigos",
                "¿Hay alguna tendencia nueva?"
            ]
        },
        {
            "name": "⚡ Productividad",
            "platform": "productivity",
            "messages": [
                "¿Cómo puedo organizar mejor mi trabajo?",
                "Necesito herramientas de productividad",
                "¿Hay alguna forma de automatizar tareas?"
            ]
        },
        {
            "name": "🎲 Gaming",
            "platform": "gaming",
            "messages": [
                "¿Cuál es el mejor juego para jugar ahora?",
                "Quiero mejorar mi ranking",
                "¿Hay algún torneo disponible?"
            ]
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}")
        print("-" * 40)
        
        platform_results = []
        
        for i, message in enumerate(test_case['messages'], 1):
            print(f"  Mensaje {i}: {message}")
            
            try:
                # Preparar datos para la API
                payload = {
                    "message": message,
                    "user_id": f"test_user_{test_case['platform']}_{i}",
                    "context": {
                        "platform_type": test_case['platform'],
                        "domain": test_case['name'].split()[1].lower(),
                        "user_role": "tester",
                        "business_context": f"Testing adaptive system for {test_case['name']}",
                        "language_preference": "es",
                        "formality_level": 0.5,
                        "technical_level": 0.5,
                        "urgency_level": 0.3
                    }
                }
                
                # Enviar petición
                response = requests.post(API_URL, json=payload, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data['success']:
                        print(f"    ✅ Respuesta: {data['response'][:100]}...")
                        print(f"    🎯 Plataforma detectada: {data.get('platform_detected', 'N/A')}")
                        print(f"    🎭 Personalidad: {data.get('personality_adapted', 'N/A')}")
                        
                        platform_results.append({
                            'message': message,
                            'response': data['response'],
                            'platform_detected': data.get('platform_detected'),
                            'personality_adapted': data.get('personality_adapted'),
                            'adaptation_insights': data.get('adaptation_insights'),
                            'success': True
                        })
                    else:
                        print(f"    ❌ Error: {data.get('error', 'Error desconocido')}")
                        platform_results.append({
                            'message': message,
                            'error': data.get('error'),
                            'success': False
                        })
                else:
                    print(f"    ❌ Error HTTP: {response.status_code}")
                    platform_results.append({
                        'message': message,
                        'error': f"HTTP {response.status_code}",
                        'success': False
                    })
                
                # Pausa entre mensajes
                time.sleep(1)
                
            except requests.exceptions.RequestException as e:
                print(f"    ❌ Error de conexión: {e}")
                platform_results.append({
                    'message': message,
                    'error': str(e),
                    'success': False
                })
            except Exception as e:
                print(f"    ❌ Error inesperado: {e}")
                platform_results.append({
                    'message': message,
                    'error': str(e),
                    'success': False
                })
        
        results.append({
            'platform': test_case['name'],
            'platform_type': test_case['platform'],
            'results': platform_results
        })
    
    # Generar reporte
    generate_adaptive_report(results)
    
    return results

def generate_adaptive_report(results):
    """Genera un reporte detallado de las pruebas adaptativas"""
    
    print("\n" + "=" * 60)
    print("📊 REPORTE DEL SISTEMA ADAPTATIVO")
    print("=" * 60)
    
    total_tests = 0
    successful_tests = 0
    platform_stats = {}
    
    for platform_result in results:
        platform_name = platform_result['platform']
        platform_type = platform_result['platform_type']
        platform_tests = platform_result['results']
        
        successful = sum(1 for test in platform_tests if test['success'])
        total = len(platform_tests)
        
        total_tests += total
        successful_tests += successful
        
        success_rate = (successful / total) * 100 if total > 0 else 0
        
        platform_stats[platform_name] = {
            'total': total,
            'successful': successful,
            'success_rate': success_rate,
            'platform_type': platform_type
        }
        
        print(f"\n{platform_name}:")
        print(f"  ✅ Exitosos: {successful}/{total} ({success_rate:.1f}%)")
        
        # Mostrar ejemplos de adaptación
        for test in platform_tests:
            if test['success']:
                print(f"    💬 '{test['message']}' → {test['response'][:80]}...")
                if test.get('adaptation_insights'):
                    print(f"    🧠 Adaptación: {test['adaptation_insights']}")
                break
    
    # Estadísticas generales
    overall_success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"📈 ESTADÍSTICAS GENERALES")
    print(f"{'='*60}")
    print(f"Total de pruebas: {total_tests}")
    print(f"Pruebas exitosas: {successful_tests}")
    print(f"Tasa de éxito: {overall_success_rate:.1f}%")
    
    # Mejores plataformas
    best_platforms = sorted(platform_stats.items(), key=lambda x: x[1]['success_rate'], reverse=True)
    
    print(f"\n🏆 MEJORES PLATAFORMAS:")
    for i, (platform, stats) in enumerate(best_platforms[:3], 1):
        print(f"{i}. {platform}: {stats['success_rate']:.1f}%")
    
    # Guardar reporte en archivo
    report_data = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_tests': total_tests,
        'successful_tests': successful_tests,
        'overall_success_rate': overall_success_rate,
        'platform_stats': platform_stats,
        'detailed_results': results
    }
    
    report_filename = f"adaptive_test_report_{int(time.time())}.json"
    with open(report_filename, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Reporte guardado en: {report_filename}")

def test_single_platform_adaptation():
    """Test de adaptación para una plataforma específica"""
    
    print("\n🎯 TEST DE ADAPTACIÓN ESPECÍFICA")
    print("=" * 40)
    
    # Ejemplo: E-commerce
    platform = "ecommerce"
    messages = [
        "Hola, ¿tienes productos?",
        "Quiero comprar algo",
        "¿Cuál es el precio?",
        "¿Hacen envíos?",
        "Gracias por la ayuda"
    ]
    
    API_URL = "http://localhost:5000/api/reasoning"
    
    print(f"Probando adaptación para: {platform}")
    print("-" * 30)
    
    for i, message in enumerate(messages, 1):
        print(f"\nMensaje {i}: {message}")
        
        try:
            payload = {
                "message": message,
                "user_id": f"single_test_user_{i}",
                "context": {
                    "platform_type": platform,
                    "domain": "ecommerce",
                    "user_role": "customer",
                    "business_context": "Testing single platform adaptation"
                }
            }
            
            response = requests.post(API_URL, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['success']:
                    print(f"  ✅ Respuesta: {data['response']}")
                    print(f"  🎯 Plataforma: {data.get('platform_detected', 'N/A')}")
                    print(f"  🎭 Personalidad: {data.get('personality_adapted', 'N/A')}")
                    print(f"  🧠 Adaptación: {data.get('adaptation_insights', 'N/A')}")
                else:
                    print(f"  ❌ Error: {data.get('error', 'Error desconocido')}")
            else:
                print(f"  ❌ Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        time.sleep(1)

if __name__ == "__main__":
    print("🧠 INICIANDO PRUEBAS DEL SISTEMA ADAPTATIVO")
    print("Asegúrate de que el servidor esté ejecutándose en http://localhost:5000")
    print("=" * 60)
    
    try:
        # Test completo del sistema adaptativo
        results = test_adaptive_system()
        
        # Test específico de una plataforma
        test_single_platform_adaptation()
        
        print("\n🎉 ¡Pruebas completadas!")
        
    except KeyboardInterrupt:
        print("\n⏹️ Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error en las pruebas: {e}")
        sys.exit(1) 