#!/usr/bin/env python3
"""
Script de prueba para verificar que el módulo AventuraPe funciona correctamente
"""

import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Prueba las importaciones del módulo AventuraPe"""
    try:
        logger.info("🔍 Probando importaciones...")
        
        # Probar importación del servicio
        from domain.services.aventurape_service import AventuraPeService
        logger.info("✅ AventuraPeService importado correctamente")
        
        # Probar importación del servicio Gemini
        from infrastructure.external_apis.gemini_ai_service import GeminiAIService
        logger.info("✅ GeminiAIService importado correctamente")
        
        # Probar importación de configuración
        from config.aventurape_config import AVENTURAPE_API_URL
        logger.info("✅ Configuración importada correctamente")
        
        # Probar importación del blueprint
        from presentation.aventurape_endpoints import aventurape_blueprint
        logger.info("✅ Blueprint importado correctamente")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en importaciones: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def test_blueprint_creation():
    """Prueba la creación del blueprint"""
    try:
        from presentation.aventurape_endpoints import aventurape_blueprint
        
        # Verificar que el blueprint tiene las rutas correctas
        routes = [rule.rule for rule in aventurape_blueprint.url_map.iter_rules()]
        logger.info(f"📋 Rutas del blueprint: {routes}")
        
        expected_routes = ['/aventurape/health', '/aventurape/generate-content']
        for route in expected_routes:
            if route in routes:
                logger.info(f"✅ Ruta {route} encontrada")
            else:
                logger.error(f"❌ Ruta {route} NO encontrada")
                
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creando blueprint: {e}")
        return False

def test_flask_app():
    """Prueba la aplicación Flask completa"""
    try:
        from flask import Flask
        from presentation.aventurape_endpoints import aventurape_blueprint
        
        # Crear app de prueba
        app = Flask(__name__)
        app.register_blueprint(aventurape_blueprint)
        
        # Verificar rutas registradas
        all_routes = [rule.rule for rule in app.url_map.iter_rules()]
        logger.info(f"📋 Todas las rutas registradas: {all_routes}")
        
        # Verificar rutas específicas de AventuraPe
        aventurape_routes = [route for route in all_routes if '/aventurape' in route]
        logger.info(f"🏄‍♂️ Rutas de AventuraPe: {aventurape_routes}")
        
        return len(aventurape_routes) > 0
        
    except Exception as e:
        logger.error(f"❌ Error en aplicación Flask: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Iniciando pruebas del módulo AventuraPe...")
    
    # Verificar variables de entorno
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_key:
        logger.info("✅ GEMINI_API_KEY configurada")
    else:
        logger.warning("⚠️ GEMINI_API_KEY no configurada")
    
    # Ejecutar pruebas
    test1 = test_imports()
    test2 = test_blueprint_creation()
    test3 = test_flask_app()
    
    if test1 and test2 and test3:
        logger.info("🎉 Todas las pruebas pasaron exitosamente!")
    else:
        logger.error("❌ Algunas pruebas fallaron")
        sys.exit(1)