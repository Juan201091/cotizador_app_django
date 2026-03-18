from typing import List
from core.domain.models.helpers_domain import Cantidad


# Entidad Receta
class Receta:
    def __init__(self, id: int, nombre: str, instrucciones: str):
        self.id = id
        self.nombre = nombre
        self.instrucciones = instrucciones


# Entidad Ingrediente
class Ingrediente:
    def __init__(self, id: int, nombre: str, tipo: str, precio_unit_250g: float):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo  # "Carne", "Pescado", "Verdura"
        self.precio_unit_250g = precio_unit_250g


# Entidad PlatoIngrediente
class PlatoIngrediente:
    def __init__(self, ingrediente: Ingrediente, cantidad_gramos: int):
        self.ingrediente = ingrediente
        self.cantidad = Cantidad(cantidad_gramos)


# Entidad Plato
class Plato:
    def __init__(
        self, id: int, nombre: str, receta: Receta, ingredientes: List[PlatoIngrediente]
    ):
        self.id = id
        self.nombre = nombre
        self.receta = receta
        self.ingredientes = ingredientes


# Corregimos la clase Dinero
class Dinero:
    def __init__(self, valor: float, moneda: str = "ARS"):
        self.valor = float(valor)
        self.moneda = moneda  # "ARS" o "USD"

    def sumar(self, otro):
        return Dinero(self.valor + otro.valor, self.moneda)

    def __repr__(self):
        return f"{self.moneda} ${self.valor:.2f}"