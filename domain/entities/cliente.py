"""
🏗️ Domain Entity: Cliente
Siguiendo principios de Domain-Driven Design (DDD)
"""

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class Cliente:
    """
    Entidad Cliente - Representa un cliente único en el sistema
    
    Siguiendo DDD: Una entidad tiene identidad única y ciclo de vida
    """
    
    # Identidad única
    telefono: str  # Primary identifier para WhatsApp
    
    # Atributos de dominio
    nombre: Optional[str] = None
    email: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Inicialización después de creación"""
        if self.created_at is None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def actualizar_nombre(self, nombre: str) -> None:
        """Actualiza el nombre del cliente"""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        
        self.nombre = nombre.strip()
        self.updated_at = datetime.now()
    
    def actualizar_email(self, email: str) -> None:
        """Actualiza el email del cliente"""
        if not self._es_email_valido(email):
            raise ValueError("Email inválido")
        
        self.email = email.lower().strip()
        self.updated_at = datetime.now()
    
    def tiene_informacion_completa(self) -> bool:
        """Verifica si el cliente tiene información completa"""
        return bool(self.nombre and self.telefono)
    
    def _es_email_valido(self, email: str) -> bool:
        """Validación básica de email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def __eq__(self, other) -> bool:
        """Igualdad basada en identidad única"""
        if not isinstance(other, Cliente):
            return False
        return self.telefono == other.telefono
    
    def __hash__(self) -> int:
        """Hash basado en identidad única"""
        return hash(self.telefono) 