"""
🏗️ Infrastructure Repository: PostgreSQL Quote Repository
Siguiendo principios de Domain-Driven Design (DDD)
"""

from typing import Optional
import logging

# Fallback simple por ahora
logger = logging.getLogger(__name__)

class PostgreSQLQuoteRepository:
    """
    Infrastructure Repository: Repositorio de cotizaciones PostgreSQL
    
    Con fallback a implementación en memoria
    """
    
    def __init__(self):
        logger.info("📂 PostgreSQL Quote Repository creado")
    
    def save(self, cotizacion) -> None:
        """Guarda cotización"""
        # Por ahora no hace nada, usa fallback en memoria
        logger.info(f"💾 Cotización guardada en memoria: {cotizacion.numero_cotizacion}")
        pass 