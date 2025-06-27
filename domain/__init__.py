"""
🏗️ Domain Layer - Autofondo Barbara
Siguiendo principios de Domain-Driven Design (DDD)
"""

# Importaciones principales del dominio
from .entities.cliente import Cliente
from .value_objects.money import Money
from .aggregates.cotizacion import Cotizacion, TipoVehiculo, EstadoCotizacion
from .services.barbara_conversation_service import BarbaraConversationService

__all__ = [
    'Cliente',
    'Money', 
    'Cotizacion',
    'TipoVehiculo',
    'EstadoCotizacion',
    'BarbaraConversationService'
] 