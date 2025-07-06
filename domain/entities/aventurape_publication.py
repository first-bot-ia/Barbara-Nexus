"""
🏛️ Domain Entity: AventuraPePublication
Entidad de dominio que representa una publicación de aventura turística.
"""

from typing import List, Optional
from datetime import datetime

class AventuraPePublication:
    """
    Entidad de dominio para representar una publicación de aventura turística.
    Contiene los atributos necesarios para una publicación en AventuraPe.
    """
    
    def __init__(
        self,
        id: Optional[str] = None,
        title: str = "",
        description: str = "",
        location: str = "",
        duration: str = "",
        difficulty: str = "",
        price: float = 0.0,
        capacity: int = 1,
        created_at: Optional[datetime] = None,
        tags: List[str] = None
    ):
        """
        Inicializa una nueva publicación de AventuraPe
        
        Args:
            id: Identificador único de la publicación
            title: Título de la publicación
            description: Descripción detallada de la aventura
            location: Ubicación donde se realizará la actividad
            duration: Duración estimada de la actividad
            difficulty: Nivel de dificultad (Fácil, Moderado, Difícil, Extremo)
            price: Precio de la actividad
            capacity: Cantidad de cupos disponibles
            created_at: Fecha de creación
            tags: Etiquetas para categorizar la publicación
        """
        self.id = id
        self.title = title
        self.description = description
        self.location = location
        self.duration = duration
        self.difficulty = difficulty
        self.price = price
        self.capacity = capacity
        self.created_at = created_at or datetime.now()
        self.tags = tags or []
        
    def to_dict(self) -> dict:
        """
        Convierte la entidad a un diccionario
        
        Returns:
            Diccionario con los atributos de la publicación
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "duration": self.duration,
            "difficulty": self.difficulty,
            "price": self.price,
            "capacity": self.capacity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "tags": self.tags
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'AventuraPePublication':
        """
        Crea una entidad a partir de un diccionario
        
        Args:
            data: Diccionario con los datos de la publicación
            
        Returns:
            Nueva instancia de AventuraPePublication
        """
        return AventuraPePublication(
            id=data.get("id"),
            title=data.get("title", ""),
            description=data.get("description", ""),
            location=data.get("location", ""),
            duration=data.get("duration", ""),
            difficulty=data.get("difficulty", ""),
            price=data.get("price", 0.0),
            capacity=data.get("capacity", 1),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else None,
            tags=data.get("tags", [])
        ) 