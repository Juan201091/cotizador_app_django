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
    
    def __str__(self):
        return f"{self.gramos}g"