import re
from core.aplication.ports.ports import LeerMDPort
import logging
logger = logging.getLogger(__name__)

class LeerMDImpl(LeerMDPort):
    EXTENSION = ".md"

    def parsear_numero(self, valor):
        return float(valor.replace(",", ".").strip())

    def normalizar_unidad(self, unidad):
        return "gr" if unidad.lower() == "g" else "kg"

    def limpiar_linea(self, linea):
        return re.sub(r"^\s*([-*]|\d+\.|[a-zA-Z]\.)\s*", "", linea).strip()

    def leer(self, archivo=None):
        if archivo and not str(archivo.name).lower().endswith(self.EXTENSION):
            raise ValueError(f"Archivo inválido, se esperaba un '{self.EXTENSION}'")

        archivo = archivo or "data/Recetas.md"
        recetas = []

        try:
            with open(archivo, "r", encoding="utf-8") if isinstance(archivo, str) else archivo.open("r", encoding="utf-8") as file:
                lineas = file.readlines()
        except Exception:
            logger.exception("Error leyendo archivo MD")
            return []

        receta_actual = None
        modo = None

        for idx, linea in enumerate(lineas):
            try:
                linea = linea.strip()
                if not linea:
                    continue

                if linea.startswith("# "):
                    if receta_actual:
                        recetas.append(receta_actual)

                    receta_actual = {
                        "nombre": linea.replace("#", "").strip(),
                        "ingredientes": [],
                        "instrucciones": ""
                    }
                    modo = None
                    continue

                if any(x in linea.lower() for x in ["ingredientes", "lista"]):
                    modo = "ingredientes"
                    continue

                if "instrucciones" in linea.lower() or "preparación" in linea.lower():
                    modo = "instrucciones"
                    continue

                if not receta_actual:
                    continue

                linea = self.limpiar_linea(linea)

                if modo == "ingredientes":
                    match1 = re.search(r"(\d+(?:[\.,]\d+)?)\s*(kg|g)\s+de\s+(.+)", linea, re.IGNORECASE)
                    match2 = re.search(r"(.+?)\s*:\s*(\d+(?:[\.,]\d+)?)\s*(kg|g)", linea, re.IGNORECASE)

                    if match1:
                        cantidad_raw = match1.group(1)
                        unidad = self.normalizar_unidad(match1.group(2))
                        nombre = match1.group(3).strip()

                    elif match2:
                        nombre = match2.group(1).strip()
                        cantidad_raw = match2.group(2)
                        unidad = self.normalizar_unidad(match2.group(3))

                    else:
                        logger.warning("Ingrediente no reconocido: %s", linea)
                        continue

                    try:
                        cantidad = self.parsear_numero(cantidad_raw)
                    except Exception:
                        logger.warning("Error parseando número: %s", cantidad_raw)
                        continue

                    receta_actual["ingredientes"].append({
                        "nombre": nombre,
                        "cantidad": cantidad,
                        "unidad": unidad
                    })

                elif modo == "instrucciones":
                    receta_actual["instrucciones"] += linea + " "

            except Exception:
                logger.exception("Error procesando línea %s: %s", idx, linea)
                continue

        if receta_actual:
            recetas.append(receta_actual)

        logger.info("Recetas parseadas: %s", len(recetas))

        return recetas