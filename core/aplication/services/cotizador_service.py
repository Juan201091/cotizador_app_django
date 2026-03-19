# # core/aplication/services/cotizador_service.py
# from core.domain.models.models import Dinero
# import requests

# class CotizadorService:
#     def __init__(self, platos: list, fecha: str):
#         """
#         platos: lista de diccionarios ya parseados en cache
#         fecha: string YYYY-MM-DD para cotización USD/ARS
#         """
#         self.platos = platos
#         self.fecha = fecha

#     def _obtener_dolar(self) -> float:
#         url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{self.fecha}/v1/currencies/usd.json"
#         try:
#             r = requests.get(url, timeout=5)
#             r.raise_for_status()
#             data = r.json()
#             return float(data["usd"]["ars"])
#         except Exception as e:
#             print(f"⚠️ No se pudo obtener cotización del dólar: {e}. Usando ARS/USD = 1")
#             return 1.0

#     def calcular_costo(self, plato_nombre: str) -> list:
#         """
#         Calcula el costo de un plato por nombre y devuelve lista con un dict para render.
#         """
#         plato = next((p for p in self.platos if p["plato"] == plato_nombre), None)
#         if not plato:
#             return []

#         dolar_ars = self._obtener_dolar()
#         costo_total = 0.0

#         for ing in plato["ingredientes"]:
#             # Cada ingrediente ya tiene su precio por 250g en 'precio_unit_250g'
#             precio_250g = ing.get("precio_unit_250g")
#             cantidad_250g = ing.get("cantidad_gramos", 0) / 250
#             if precio_250g is not None:
#                 costo_total += precio_250g * cantidad_250g

#         costo_pesos = Dinero(costo_total, "ARS")
#         costo_usd = Dinero(costo_total / dolar_ars, "USD")

#         return [{
#             "plato": plato["plato"],
#             "ingredientes": [i["nombre"] for i in plato["ingredientes"]],
#             "instrucciones": plato.get("instrucciones", ""),
#             "costo_pesos": costo_pesos,
#             "costo_usd": costo_usd,
#         }]


# core/aplication/services/cotizador_service.py

import requests
from core.domain.models.models import Dinero


class CotizadorService:
    @staticmethod
    def obtener_dolar(fecha: str) -> float:
        """
        Obtiene el valor del USD/ARS para la fecha indicada.
        Retorna 1.0 si hay error.
        """
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{fecha}/v1/currencies/usd.json"
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()
            return float(data["usd"]["ars"])
        except Exception as e:
            print(f"⚠️ No se pudo obtener cotización del dólar: {e}. Usando ARS/USD = 1")
            return 1.0

    @staticmethod
    def calcular_costo_por_fecha(plato: dict, fecha: str) -> dict:
        """
        Recibe un diccionario de plato desde cache y la fecha.
        Devuelve un diccionario con costo en pesos y USD.
        """
        dolar_ars = CotizadorService.obtener_dolar(fecha)

        costo_usd = Dinero(plato["costo_pesos"].valor / dolar_ars, "USD")

        return {
            "plato": plato["plato"],
            "costo_pesos": plato["costo_pesos"],
            "costo_usd": costo_usd,
            "instrucciones": plato["instrucciones"],
            "ingredientes": plato["ingredientes"],
        }
