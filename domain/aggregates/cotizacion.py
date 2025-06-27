"""
🏗️ Domain Aggregate: Cotización
Siguiendo principios de Domain-Driven Design (DDD)
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass, field
from decimal import Decimal
import uuid

from ..entities.cliente import Cliente
from ..value_objects.money import Money

class TipoVehiculo(Enum):
    """Tipos de vehículo soportados"""
    AUTO = "auto"
    MOTO = "moto" 
    TAXI = "taxi"
    CAMION = "camion"
    OMNIBUS = "omnibus"

class EstadoCotizacion(Enum):
    """Estados posibles de una cotización"""
    BORRADOR = "borrador"
    GENERADA = "generada"
    ENVIADA = "enviada"
    ACEPTADA = "aceptada"
    RECHAZADA = "rechazada"
    EXPIRADA = "expirada"

@dataclass
class Cotizacion:
    """
    Aggregate Root: Cotización
    
    Siguiendo DDD: Un agregado encapsula reglas de negocio complejas
    y mantiene consistencia de los datos
    """
    
    # Referencias a otras entidades (campos requeridos primero)
    cliente: Cliente
    
    # Value Objects requeridos
    tipo_vehiculo: TipoVehiculo
    precio_min: Money
    precio_max: Money
    
    # Campos opcionales con valores por defecto
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    numero_cotizacion: str = field(default="")
    precio_final: Optional[Money] = None
    ubicacion: str = "lima"
    uso_vehiculo: str = "particular"
    año_vehiculo: Optional[int] = None
    aseguradora_seleccionada: Optional[str] = None
    estado: EstadoCotizacion = EstadoCotizacion.BORRADOR
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_expiracion: Optional[datetime] = field(default=None)
    datos_adicionales: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Inicialización después de creación"""
        if not self.numero_cotizacion:
            self.numero_cotizacion = self._generar_numero_cotizacion()
        
        if self.fecha_expiracion is None:
            self.fecha_expiracion = self.fecha_creacion + timedelta(days=15)
        
        # Validar reglas de negocio
        self._validar_cotizacion()
    
    def _generar_numero_cotizacion(self) -> str:
        """Genera un número único de cotización"""
        timestamp = self.fecha_creacion.strftime("%Y%m%d")
        return f"AF{timestamp}{self.id[:8].upper()}"
    
    def _validar_cotizacion(self) -> None:
        """Valida las reglas de negocio de la cotización"""
        if not self.cliente.tiene_informacion_completa():
            raise ValueError("El cliente debe tener información completa")
        
        if self.precio_min.is_greater_than(self.precio_max):
            raise ValueError("El precio mínimo no puede ser mayor al máximo")
        
        if self.año_vehiculo and self.año_vehiculo < 1990:
            raise ValueError("El año del vehículo no puede ser anterior a 1990")
        
        if self.año_vehiculo and self.año_vehiculo > datetime.now().year + 1:
            raise ValueError("El año del vehículo no puede ser futuro")
    
    def generar_cotizacion(self) -> None:
        """Genera la cotización final con precio específico"""
        if self.estado != EstadoCotizacion.BORRADOR:
            raise ValueError("Solo se pueden generar cotizaciones en estado borrador")
        
        # Aplicar reglas de negocio para precio final
        self.precio_final = self._calcular_precio_final()
        self.estado = EstadoCotizacion.GENERADA
        
        # Agregar metadatos
        self.datos_adicionales.update({
            'fecha_generacion': datetime.now().isoformat(),
            'algoritmo_precio': 'v2.0',
            'factores_aplicados': self._obtener_factores_precio()
        })
    
    def _calcular_precio_final(self) -> Money:
        """Calcula el precio final basado en reglas de negocio"""
        import random
        from decimal import Decimal
        
        # Precio base según tipo de vehículo
        precio_base = self._obtener_precio_base()
        
        # Aplicar factores de ajuste
        factor_ubicacion = self._factor_ubicacion()
        factor_año = self._factor_año_vehiculo()
        factor_uso = self._factor_uso_vehiculo()
        
        # Calcular precio final
        factor_total = factor_ubicacion * factor_año * factor_uso
        precio_calculado = precio_base.multiply(factor_total)
        
        # Asegurar que esté dentro del rango
        if precio_calculado < self.precio_min:
            precio_calculado = self.precio_min
        elif precio_calculado > self.precio_max:
            precio_calculado = self.precio_max
        
        return precio_calculado
    
    def _obtener_precio_base(self) -> Money:
        """Obtiene el precio base según tipo de vehículo"""
        precios_base = {
            TipoVehiculo.AUTO: Money.from_soles(160),
            TipoVehiculo.MOTO: Money.from_soles(110),
            TipoVehiculo.TAXI: Money.from_soles(250),
            TipoVehiculo.CAMION: Money.from_soles(330),
            TipoVehiculo.OMNIBUS: Money.from_soles(375)
        }
        return precios_base.get(self.tipo_vehiculo, Money.from_soles(160))
    
    def _factor_ubicacion(self) -> Decimal:
        """Factor de ajuste por ubicación"""
        from decimal import Decimal
        if self.ubicacion.lower() == "lima":
            return Decimal("1.0")
        else:
            return Decimal("0.85")  # Descuento provincias
    
    def _factor_año_vehiculo(self) -> Decimal:
        """Factor de ajuste por año del vehículo"""
        from decimal import Decimal
        if not self.año_vehiculo:
            return Decimal("1.0")
        
        años_antiguedad = datetime.now().year - self.año_vehiculo
        
        if años_antiguedad <= 3:
            return Decimal("1.1")  # Recargo vehículos nuevos
        elif años_antiguedad <= 10:
            return Decimal("1.0")  # Precio normal
        else:
            return Decimal("0.95")  # Descuento vehículos antiguos
    
    def _factor_uso_vehiculo(self) -> Decimal:
        """Factor de ajuste por uso del vehículo"""
        from decimal import Decimal
        factores = {
            "particular": Decimal("1.0"),
            "comercial": Decimal("1.2"),
            "taxi": Decimal("1.5"),
            "transporte_publico": Decimal("1.8")
        }
        return factores.get(self.uso_vehiculo.lower(), Decimal("1.0"))
    
    def _obtener_factores_precio(self) -> Dict[str, Any]:
        """Obtiene los factores aplicados en el cálculo"""
        return {
            'factor_ubicacion': float(self._factor_ubicacion()),
            'factor_año': float(self._factor_año_vehiculo()),
            'factor_uso': float(self._factor_uso_vehiculo()),
            'ubicacion': self.ubicacion,
            'año_vehiculo': self.año_vehiculo,
            'uso_vehiculo': self.uso_vehiculo
        }
    
    def enviar_cotizacion(self) -> None:
        """Marca la cotización como enviada"""
        if self.estado != EstadoCotizacion.GENERADA:
            raise ValueError("Solo se pueden enviar cotizaciones generadas")
        
        self.estado = EstadoCotizacion.ENVIADA
        self.datos_adicionales['fecha_envio'] = datetime.now().isoformat()
    
    def aceptar_cotizacion(self, aseguradora: str) -> None:
        """Acepta la cotización con una aseguradora específica"""
        if self.estado not in [EstadoCotizacion.ENVIADA, EstadoCotizacion.GENERADA]:
            raise ValueError("Solo se pueden aceptar cotizaciones enviadas o generadas")
        
        if self.esta_expirada():
            raise ValueError("La cotización ha expirado")
        
        self.aseguradora_seleccionada = aseguradora
        self.estado = EstadoCotizacion.ACEPTADA
        self.datos_adicionales['fecha_aceptacion'] = datetime.now().isoformat()
    
    def rechazar_cotizacion(self, razon: Optional[str] = None) -> None:
        """Rechaza la cotización"""
        if self.estado == EstadoCotizacion.ACEPTADA:
            raise ValueError("No se puede rechazar una cotización ya aceptada")
        
        self.estado = EstadoCotizacion.RECHAZADA
        self.datos_adicionales.update({
            'fecha_rechazo': datetime.now().isoformat(),
            'razon_rechazo': razon
        })
    
    def esta_expirada(self) -> bool:
        """Verifica si la cotización ha expirado"""
        if self.fecha_expiracion is None:
            return False
        return datetime.now() > self.fecha_expiracion
    
    def marcar_como_expirada(self) -> None:
        """Marca la cotización como expirada"""
        if self.estado == EstadoCotizacion.ACEPTADA:
            raise ValueError("No se puede expirar una cotización aceptada")
        
        self.estado = EstadoCotizacion.EXPIRADA
        self.datos_adicionales['fecha_expiracion_real'] = datetime.now().isoformat()
    
    def extender_vigencia(self, dias: int) -> None:
        """Extiende la vigencia de la cotización"""
        if self.estado == EstadoCotizacion.EXPIRADA:
            raise ValueError("No se puede extender una cotización expirada")
        
        if dias <= 0:
            raise ValueError("Los días de extensión deben ser positivos")
        
        if self.fecha_expiracion is None:
            raise ValueError("La cotización no tiene fecha de expiración")
        
        self.fecha_expiracion += timedelta(days=dias)
        self.datos_adicionales.update({
            'extension_aplicada': dias,
            'fecha_extension': datetime.now().isoformat()
        })
    
    def generar_resumen(self) -> Dict[str, Any]:
        """Genera un resumen completo de la cotización"""
        return {
            'numero_cotizacion': self.numero_cotizacion,
            'cliente': {
                'nombre': self.cliente.nombre,
                'telefono': self.cliente.telefono
            },
            'vehiculo': {
                'tipo': self.tipo_vehiculo.value,
                'año': self.año_vehiculo,
                'uso': self.uso_vehiculo
            },
            'precios': {
                'rango': f"{self.precio_min} - {self.precio_max}",
                'final': str(self.precio_final) if self.precio_final else None
            },
            'estado': self.estado.value,
            'vigencia': {
                'fecha_expiracion': self.fecha_expiracion.isoformat() if self.fecha_expiracion else None,
                'dias_restantes': (self.fecha_expiracion - datetime.now()).days if self.fecha_expiracion else None,
                'expirada': self.esta_expirada()
            },
            'aseguradora': self.aseguradora_seleccionada,
            'ubicacion': self.ubicacion
        }
    
    def __str__(self) -> str:
        """Representación string de la cotización"""
        return (f"Cotización {self.numero_cotizacion} - "
                f"{self.cliente.nombre} - "
                f"{self.tipo_vehiculo.value.title()} - "
                f"{self.estado.value.title()}")
    
    def __eq__(self, other) -> bool:
        """Igualdad basada en ID único"""
        if not isinstance(other, Cotizacion):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash basado en ID único"""
        return hash(self.id) 