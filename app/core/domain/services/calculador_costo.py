from core.domain.models.models import Dinero

class CalculadorCostoReceta:

    def calcular(self, plato, precios_por_ingrediente: dict) -> Dinero:
        total = Dinero(0)

        for item in plato.ingredientes:
            nombre = item.ingrediente.nombre

            if nombre not in precios_por_ingrediente:
                raise ValueError(f"No hay precio para {nombre}")

            precio_250g = precios_por_ingrediente[nombre]

            gramos_ajustados = item.cantidad.ajustar_a_compra()
            factor = gramos_ajustados / 250

            costo = Dinero(precio_250g * factor)

            total = total.sumar(costo)

        return total