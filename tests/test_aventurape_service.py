"""
🧪 Test: AventuraPe Service
Pruebas unitarias para el servicio de AventuraPe.
"""

import unittest
from unittest.mock import MagicMock, patch

from domain.services.aventurape_service import AventuraPeService

class TestAventuraPeService(unittest.TestCase):
    """Pruebas para AventuraPeService"""
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        # Crear un mock del servicio Gemini
        self.gemini_mock = MagicMock()
        # Crear una instancia del servicio con el mock
        self.aventurape_service = AventuraPeService(self.gemini_mock)
    
    def test_generate_publication_content_success(self):
        """Prueba generación exitosa de contenido"""
        # Configurar respuesta del mock
        self.gemini_mock.generate_response.return_value = """
        {
            "title": "Aventura en los Andes",
            "description": "Una increíble travesía por las montañas andinas donde experimentarás la magia de la naturaleza y la adrenalina de las alturas."
        }
        """
        
        # Llamar al método
        content, error = self.aventurape_service.generate_publication_content("Quiero una aventura en las montañas")
        
        # Verificaciones
        self.assertIsNone(error)
        self.assertIsNotNone(content)
        self.assertEqual(content["title"], "Aventura en los Andes")
        self.assertTrue("travesía por las montañas" in content["description"])
    
    def test_generate_publication_content_api_error(self):
        """Prueba manejo de error en la API"""
        # Configurar que el mock retorne None (error en API)
        self.gemini_mock.generate_response.return_value = None
        
        # Llamar al método
        content, error = self.aventurape_service.generate_publication_content("Contexto")
        
        # Verificaciones
        self.assertIsNone(content)
        self.assertEqual(error, "No se pudo generar contenido")
    
    def test_contains_inappropriate_content(self):
        """Prueba detección de contenido inapropiado"""
        with patch("domain.services.aventurape_service.INAPPROPRIATE_WORDS", ["palabraofensiva1"]):
            # Texto sin contenido inapropiado
            self.assertFalse(
                self.aventurape_service._contains_inappropriate_content("Texto normal")
            )
            
            # Texto con contenido inapropiado
            self.assertTrue(
                self.aventurape_service._contains_inappropriate_content("Texto con palabraofensiva1 inapropiada")
            )

if __name__ == "__main__":
    unittest.main() 