class Cantidad:
    MULTIPLO = 250

    def __init__(self, gramos: int):
        self.gramos = self._ajustar(gramos)

    def _ajustar(self, gramos: int) -> int:
        if gramos % self.MULTIPLO == 0:
            return gramos
        return ((gramos // self.MULTIPLO) + 1) * self.MULTIPLO

    # ─── Método público para CalculadorCostoReceta ───
    def ajustar_a_compra(self) -> int:
        return self.gramos

# Value Object para manejar dinero
class Dinero:
    def __init__(self, monto: float, moneda: str):
        self.monto = monto
        self.moneda = moneda  # "ARS" o "USD"