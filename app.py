#!/usr/bin/env python3
"""
Archivo de entrada para Render.com
Importa y configura la aplicación Flask del chatbot dinámico
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv('.env')

# Agregar el directorio actual al path de Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar la aplicación Flask del chatbot dinámico
from chatbot_dinamico import app

if __name__ == "__main__":
    # Obtener el puerto desde las variables de entorno de Render
    port = int(os.environ.get("PORT", 5001))
    
    # Ejecutar la aplicación
    app.run(host="0.0.0.0", port=port, debug=False) 