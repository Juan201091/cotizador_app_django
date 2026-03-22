from core.domain.services.calculador_costo import CalculadorCostoReceta
from core.domain.models.models import Dinero


class CalcularCostoRecetasUseCase:
    def __init__(self, cotizador_service):
        self.cotizador_service = cotizador_service
        self.calculador = CalculadorCostoReceta()

    def formatear_cantidad(self, gramos: int) -> str:
        if gramos >= 1000:
            return f"{gramos / 1000:.2f}".rstrip("0").rstrip(".") + "kg"
        return f"{gramos}gr"

    def execute(self, platos, precios, fecha: str, plato_nombre: str = None):
        dolar = self.cotizador_service.obtener_dolar(fecha)

        resultado = []

        for plato in platos:
            costo_ars = self.calculador.calcular(plato, precios)
            costo_usd = Dinero(costo_ars.valor / dolar, "USD")

            ingredientes = []
            for i in plato.ingredientes:
                gramos_receta = i.cantidad.gramos_reales
                gramos_compra = i.cantidad.ajustar_a_compra()

                ingredientes.append(
                    {
                        "nombre": i.ingrediente.nombre,
                        "cantidad_receta": self.formatear_cantidad(gramos_receta),
                        "cantidad_compra": self.formatear_cantidad(gramos_compra),
                    }
                )

            resultado.append(
                {
                    "plato": plato.nombre,
                    "costo_pesos": round(costo_ars.valor, 2),
                    "costo_usd": round(costo_usd.valor, 2),
                    "ingredientes": ingredientes,
                    "instrucciones": plato.receta.instrucciones,
                }
            )

        # 👇 lógica movida acá
        if plato_nombre:
            resultado = [r for r in resultado if r["plato"] == plato_nombre]

        return resultado