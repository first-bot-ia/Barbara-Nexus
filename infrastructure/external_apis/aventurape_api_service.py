"""
🏗️ Infrastructure Service: AventuraPe API Service
Servicio para conectar con la API de AventuraPe.
"""

import requests
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class AventuraPeApiService:
    """
    Servicio de infraestructura para interactuar con la API de AventuraPe.
    Implementación simplificada que solo gestiona la publicación de actividades.
    """
    
    def __init__(self, base_url: str):
        """
        Inicializa el servicio con la URL base de la API
        
        Args:
            base_url: URL base de la API de AventuraPe
        """
        self.base_url = base_url.rstrip('/')
        
    def get_publications(self) -> List[Dict[str, Any]]:
        """
        Obtiene la lista de publicaciones desde AventuraPe
        
        Returns:
            Lista de publicaciones
        """
        try:
            response = requests.get(f"{self.base_url}/api/publications")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error al obtener publicaciones: {str(e)}")
            return []
    
    def create_publication(self, publication_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Crea una nueva publicación en AventuraPe
        
        Args:
            publication_data: Datos de la publicación (título, descripción, etc.)
            
        Returns:
            Datos de la publicación creada o None si falla
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/publications",
                json=publication_data
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error al crear publicación: {str(e)}")
            return None
    
    def health_check(self) -> bool:
        """
        Verifica la conectividad con la API de AventuraPe
        
        Returns:
            True si la API está disponible, False en caso contrario
        """
        try:
            response = requests.get(f"{self.base_url}/api/health")
            return response.status_code == 200
        except Exception:
            return False 