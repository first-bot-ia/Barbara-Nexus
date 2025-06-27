"""
🏗️ Domain Value Object: Money
Siguiendo principios de Domain-Driven Design (DDD)
"""

from decimal import Decimal
from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class Money:
    """
    Value Object Money - Representa un valor monetario
    
    Siguiendo DDD: Un value object es inmutable y se define por sus atributos
    """
    
    amount: Decimal
    currency: str = "PEN"  # Soles peruanos por defecto
    
    def __post_init__(self):
        """Validaciones post-inicialización"""
        if self.amount < 0:
            raise ValueError("El monto no puede ser negativo")
        
        if not self.currency or len(self.currency) != 3:
            raise ValueError("La moneda debe ser un código ISO de 3 caracteres")
        
        # Forzar uppercase para moneda
        object.__setattr__(self, 'currency', self.currency.upper())
    
    @classmethod
    def from_soles(cls, amount: Union[int, float, str, Decimal]) -> 'Money':
        """Crear Money en soles peruanos"""
        return cls(amount=Decimal(str(amount)), currency="PEN")
    
    @classmethod
    def from_dollars(cls, amount: Union[int, float, str, Decimal]) -> 'Money':
        """Crear Money en dólares americanos"""
        return cls(amount=Decimal(str(amount)), currency="USD")
    
    def add(self, other: 'Money') -> 'Money':
        """Suma dos valores monetarios de la misma moneda"""
        if self.currency != other.currency:
            raise ValueError(f"No se pueden sumar {self.currency} con {other.currency}")
        
        return Money(
            amount=self.amount + other.amount,
            currency=self.currency
        )
    
    def subtract(self, other: 'Money') -> 'Money':
        """Resta dos valores monetarios de la misma moneda"""
        if self.currency != other.currency:
            raise ValueError(f"No se pueden restar {self.currency} con {other.currency}")
        
        result_amount = self.amount - other.amount
        if result_amount < 0:
            raise ValueError("El resultado no puede ser negativo")
        
        return Money(
            amount=result_amount,
            currency=self.currency
        )
    
    def multiply(self, factor: Union[int, float, Decimal]) -> 'Money':
        """Multiplica el valor monetario por un factor"""
        return Money(
            amount=self.amount * Decimal(str(factor)),
            currency=self.currency
        )
    
    def is_zero(self) -> bool:
        """Verifica si el monto es cero"""
        return self.amount == 0
    
    def is_greater_than(self, other: 'Money') -> bool:
        """Compara si este monto es mayor que otro"""
        if self.currency != other.currency:
            raise ValueError(f"No se pueden comparar {self.currency} con {other.currency}")
        
        return self.amount > other.amount
    
    def formatted(self) -> str:
        """Retorna el valor formateado para mostrar"""
        if self.currency == "PEN":
            return f"S/ {self.amount:.2f}"
        elif self.currency == "USD":
            return f"$ {self.amount:.2f}"
        else:
            return f"{self.amount:.2f} {self.currency}"
    
    def __str__(self) -> str:
        """Representación string"""
        return self.formatted()
    
    def __lt__(self, other: 'Money') -> bool:
        """Operador menor que"""
        if self.currency != other.currency:
            raise ValueError(f"No se pueden comparar {self.currency} con {other.currency}")
        return self.amount < other.amount
    
    def __le__(self, other: 'Money') -> bool:
        """Operador menor o igual que"""
        if self.currency != other.currency:
            raise ValueError(f"No se pueden comparar {self.currency} con {other.currency}")
        return self.amount <= other.amount
    
    def __gt__(self, other: 'Money') -> bool:
        """Operador mayor que"""
        if self.currency != other.currency:
            raise ValueError(f"No se pueden comparar {self.currency} con {other.currency}")
        return self.amount > other.amount
    
    def __ge__(self, other: 'Money') -> bool:
        """Operador mayor o igual que"""
        if self.currency != other.currency:
            raise ValueError(f"No se pueden comparar {self.currency} con {other.currency}")
        return self.amount >= other.amount 