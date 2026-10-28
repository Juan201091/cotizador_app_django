import unicodedata # libería para normalizar texto (eliminar acentos, etc) ej "Carne de res" -> "carne de res"
from typing import List
from core.domain.models.models import (
    Receta,
    Ingrediente,
    PlatoIngrediente,
    Plato,
)
import logging
logger = logging.getLogger(__name__)

#Orquestador de la carga de datos y mapeo a modelos de dominio

class RecetaService:
    def __init__(self, excel_reader, pdf_reader, md_reader):
        self.excel_reader = excel_reader
        self.pdf_reader = pdf_reader
        self.md_reader = md_reader

    def normalizar(self, texto: str) -> str:
        if not isinstance(texto, str):
            return None

        texto = texto.lower()

        resultado = ""
        texto_normalizado = unicodedata.normalize("NFD", texto)

        for c in texto_normalizado:
            if unicodedata.category(c) != "Mn":
                resultado += c

        return resultado.strip()

    def _mapear_precios(self, data: List[dict]) -> dict:
        precios = {}

        for item in data:
            try:
                nombre = self.normalizar(item["nombre"])
                if not nombre:
                    logger.warning("Nombre inválido en precios: %s", item)
                    continue

                precio_kg = float(item["precio"])
                precio_250g = precio_kg / 4

                precios[nombre] = precio_250g

            except Exception:
                logger.warning("Error procesando precio: %s", item)
                continue

        logger.info("Precios mapeados: %s items", len(precios))
        return precios
    
    
    
    def _mapear_recetas(self, recetas: List[dict]) -> List[Plato]:
        platos = []

        for r in recetas:
            try:
                nombre_receta = self.normalizar(r["nombre"])
                if not nombre_receta:
                    logger.warning("Receta sin nombre válido: %s", r)
                    continue

                receta = Receta(
                    id=0,
                    nombre=nombre_receta,
                    instrucciones=r.get("instrucciones", "")
                )

                ingredientes = []

                for ing in r.get("ingredientes", []):
                    try:
                        nombre = self.normalizar(ing["nombre"])
                        if not nombre:
                            logger.warning("Ingrediente inválido: %s", ing)
                            continue

                        cantidad = float(ing["cantidad"])
                        unidad = ing["unidad"].lower()

                        if unidad == "gr":
                            gramos = cantidad
                        elif unidad == "kg":
                            gramos = cantidad * 1000
                        else:
                            logger.warning("Unidad desconocida: %s", ing)
                            continue

                        ingredientes.append(
                            PlatoIngrediente(
                                ingrediente=Ingrediente(0, nombre, "", 0),
                                cantidad_gramos=gramos
                            )
                        )

                    except Exception:
                        logger.warning("Error procesando ingrediente: %s", ing)
                        continue

                platos.append(
                    Plato(
                        id=0,
                        nombre=receta.nombre,
                        receta=receta,
                        ingredientes=ingredientes
                    )
                )

            except Exception:
                logger.error("Error procesando receta completa: %s", r)
                continue

        logger.info("Platos mapeados: %s", len(platos))
        return platos

    def ejecutar(self):
        try:
            carnes = self.excel_reader.leer()
        except Exception:
            logger.exception("Error leyendo Excel")
            carnes = []

        try:
            verduras = self.pdf_reader.leer()
        except Exception:
            logger.exception("Error leyendo PDF")
            verduras = []

        try:
            recetas_raw = self.md_reader.leer()
        except Exception:
            logger.exception("Error leyendo MD")
            recetas_raw = []

        precios = self._mapear_precios(carnes + verduras)
        platos = self._mapear_recetas(recetas_raw)

        return (platos, precios)