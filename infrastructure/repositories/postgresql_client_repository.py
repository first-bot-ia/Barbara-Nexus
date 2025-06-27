"""
🏗️ Infrastructure Repository: PostgreSQL Client Repository
Siguiendo principios de Domain-Driven Design (DDD)
"""

from typing import Optional
import logging

# Fallback simple por ahora
logger = logging.getLogger(__name__)

class PostgreSQLClientRepository:
    """
    Infrastructure Repository: Repositorio de clientes PostgreSQL
    
    Con fallback a implementación en memoria
    """
    
    def __init__(self):
        logger.info("📂 PostgreSQL Client Repository creado")
    
    def find_by_phone(self, phone: str) -> Optional[object]:
        """Busca cliente por teléfono"""
        # Por ahora retorna None para usar fallback en memoria
        return None
    
    def save(self, cliente) -> None:
        """Guarda cliente"""
        # Por ahora no hace nada, usa fallback en memoria
        pass 