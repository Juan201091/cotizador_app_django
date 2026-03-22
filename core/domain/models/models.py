from typing import List
from core.domain.models.helpers_domain import Cantidad


# Entidad Receta
class Receta:
    def __init__(self, id: int, nombre: str, instrucciones: str):
        self.id = id
        self.nombre = nombre
        self.instrucciones = instrucciones

    def __str__(self):
        return f"Receta: {self.nombre}, Instrucciones: {self.instrucciones}"


# Entidad Ingrediente
class Ingrediente:
    def __init__(self, id: int, nombre: str, tipo: str, precio_x_250g: float):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo  # "Carne", "Pescado", "Verdura"
        self.precio_x_250g = precio_x_250g

    def __str__(self):
        return f"Ingrediente: {self.nombre}, Tipo: {self.tipo}, Precio unitario (250g): {self.precio_x_250g}" 


# Entidad PlatoIngrediente
class PlatoIngrediente:
    def __init__(self, ingrediente: Ingrediente, cantidad_gramos: int):
        self.ingrediente = ingrediente
        self.cantidad = Cantidad(cantidad_gramos)

    def __str__(self):
        return f"PlatoIngrediente: {self.ingrediente.nombre}, Cantidad: {self.cantidad.valor}g"


# Entidad Plato
class Plato:
    def __init__(
        self, id: int, nombre: str, receta: Receta, ingredientes: List[PlatoIngrediente]
    ):
        self.id = id
        self.nombre = nombre
        self.receta = receta
        self.ingredientes = ingredientes

    def __str__(self):
        return f"Plato: {self.nombre}, Receta: {self.receta.nombre}, Ingredientes: {[i.ingrediente.nombre for i in self.ingredientes]}" 



class Dinero:
    def __init__(self, valor: float, moneda: str = "ARS"):
        self.valor = float(valor)
        self.moneda = moneda  # "ARS" o "USD"

    def sumar(self, otro):
        return Dinero(self.valor + otro.valor, self.moneda)

    def __repr__(self):
        return f"{self.moneda} ${self.valor:.2f}"