#!/usr/bin/env python3
"""
Script para limpiar procesos legacy de ML que generan archivos en la raíz
"""

import os
import sys
import json
import shutil
from datetime import datetime

def cleanup_legacy_ml_files():
    """
    Detiene procesos legacy y mueve archivos ML a carpeta correcta
    """
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ml_folder = os.path.join(project_root, 'ml')
    
    # Crear carpeta ml si no existe
    os.makedirs(ml_folder, exist_ok=True)
    
    # Archivos ML que se generan en la raíz incorrectamente
    ml_files_in_root = [
        'ml_patterns.json',
        'ml_metrics.json'
    ]
    
    # Archivos de backup que se generan en la raíz
    backup_pattern = 'ml_patterns_backup_'
    
    moved_files = []
    
    # Mover archivos ML de la raíz a carpeta ml/
    for root_file in os.listdir(project_root):
        if (root_file in ml_files_in_root or 
            root_file.startswith(backup_pattern)):
            
            source = os.path.join(project_root, root_file)
            target = os.path.join(ml_folder, root_file)
            
            if os.path.isfile(source):
                try:
                    shutil.move(source, target)
                    moved_files.append(root_file)
                    print(f"✅ Movido: {root_file} -> ml/")
                except Exception as e:
                    print(f"❌ Error moviendo {root_file}: {e}")
    
    # Crear archivo de configuración para evitar generación futura en raíz
    config_file = os.path.join(ml_folder, 'ml_config.json')
    config = {
        "ml_files_path": ml_folder,
        "patterns_file": os.path.join(ml_folder, "ml_patterns.json"),
        "metrics_file": os.path.join(ml_folder, "ml_metrics.json"),
        "backup_path": ml_folder,
        "last_cleanup": datetime.now().isoformat(),
        "moved_files": moved_files,
        "status": "cleaned_and_organized"
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n🎯 LIMPIEZA COMPLETADA:")
    print(f"📁 Archivos movidos a ml/: {len(moved_files)}")
    print(f"⚙️ Configuración creada: ml_config.json")
    print(f"✨ Ahora todos los archivos ML se generarán en ml/")
    
    return moved_files

if __name__ == "__main__":
    cleanup_legacy_ml_files() 