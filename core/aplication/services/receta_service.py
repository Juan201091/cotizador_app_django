import re
import unicodedata
from typing import List
from datetime import datetime
import requests
from core.domain.models.models import (
    Receta,
    Ingrediente,
    PlatoIngrediente,
    Plato,
    Dinero,
    Cantidad,
)


class RecetaService:
    def __init__(self, excel_reader, pdf_reader, md_reader, fecha: str = None):
        self.excel_reader = excel_reader
        self.pdf_reader = pdf_reader
        self.md_reader = md_reader
        # si no se pasa fecha, usamos hoy
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d")

    # ─── Normalización de strings ───
    def normalizar(self, texto: str) -> str:
        texto = texto.lower()
        texto = "".join(
            c
            for c in unicodedata.normalize("NFD", texto)
            if unicodedata.category(c) != "Mn"
        )
        return texto.strip()

    # ─── Mapear precios a 250g y normalizar nombre ───
    def _mapear_precios(self, data: List[dict]) -> dict:
        precios = {}
        for item in data:
            nombre = self.normalizar(item["nombre"])
            precio_kg = float(item["precio"])
            precio_250g = precio_kg / 4  # cada 250 gramos
            precios[nombre] = precio_250g
        return precios

    # ─── Parsear Markdown a objetos de dominio ───
    def _mapear_recetas(self, recetas_raw: List[dict]) -> List[Plato]:
        platos = []

        for r in recetas_raw:
            receta = Receta(
                id=0,
                nombre=self.normalizar(r["nombre"]),
                instrucciones=r.get("instrucciones", ""),
            )

            ingredientes_plato = []
            for ing in r.get("ingredientes", []):
                nombre = self.normalizar(ing["nombre"])
                cantidad = float(ing["cantidad"])
                unidad = ing["unidad"].lower()
                gramos = cantidad if unidad == "gr" else cantidad * 1000

                plato_ing = PlatoIngrediente(
                    ingrediente=Ingrediente(
                        id=0, nombre=nombre, tipo="", precio_unit_250g=0
                    ),
                    cantidad_gramos=gramos,
                )
                ingredientes_plato.append(plato_ing)

            plato = Plato(
                id=0,
                nombre=receta.nombre,
                receta=receta,
                ingredientes=ingredientes_plato,
            )
            platos.append(plato)

        return platos

    # ─── Buscar precio de un ingrediente ───
    def _buscar_precio(self, nombre: str, precios: dict):
        nombre_normalizado = self.normalizar(nombre)
        return precios.get(nombre_normalizado)

    # ─── Obtener cotización USD/ARS ───
    def _obtener_dolar(self) -> float:
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{self.fecha}/v1/currencies/usd.json"
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()
            return float(data["usd"]["ars"])
        except Exception as e:
            print(f"⚠️ No se pudo obtener cotización del dólar: {e}. Usando ARS/USD = 1")
            return 1.0

    # ─── Ejecutar cálculo de costos ───
    def ejecutar(self):
        carnes = self.excel_reader.leer()
        verduras = self.pdf_reader.leer()
        recetas_raw = self.md_reader.leer()

        precios = self._mapear_precios(carnes + verduras)
        platos = self._mapear_recetas(recetas_raw)

        resultado = []
        dolar_ars = self._obtener_dolar()

        for plato in platos:
            costo_total = 0.0
            ingredientes_sin_precio = []

            for ing in plato.ingredientes:
                precio_250g = self._buscar_precio(ing.ingrediente.nombre, precios)
                if precio_250g is None:
                    ingredientes_sin_precio.append(ing.ingrediente.nombre)
                else:
                    cantidad_250g = ing.cantidad.gramos / 250
                    costo_total += precio_250g * cantidad_250g

            costo_pesos = Dinero(costo_total, "ARS")
            costo_usd = Dinero(costo_total / dolar_ars, "USD")

            if ingredientes_sin_precio:
                print(
                    f"⚠️ Plato '{plato.nombre}' tiene ingredientes sin precio: {ingredientes_sin_precio} → "
                    f"costo calculado: ${costo_pesos.valor:.2f}"
                )

            resultado.append({
                "plato": plato.nombre,
                "costo_pesos": costo_pesos,
                "costo_usd": costo_usd,
                "instrucciones": plato.receta.instrucciones,
                "ingredientes": [ing.ingrediente.nombre for ing in plato.ingredientes],
            })

        return resultado