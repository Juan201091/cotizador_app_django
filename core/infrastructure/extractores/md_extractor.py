import re
from core.aplication.ports.ports import LeerXLSPort


class LeerMDImpl(LeerXLSPort):
    def parsear_numero(self, valor):
        # Convierte "1,5" en 1.5
        return float(valor.replace(",", ".").strip())

    def normalizar_unidad(self, unidad):
        return "gr" if unidad.lower() == "g" else "kg"

    def limpiar_linea(self, linea):
        # Quita bullets, numeración y letras tipo "a." al inicio
        return re.sub(r"^\s*([-*]|\d+\.|[a-zA-Z]\.)\s*", "", linea).strip()

    def leer(self, path: str = "data/Recetas.md"):
        recetas = []

        with open(path, "r", encoding="utf-8") as file:
            lineas = file.readlines()

        receta_actual = None
        modo = None

        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue

            # 🟣 NUEVA RECETA
            if linea.startswith("# "):
                if receta_actual:
                    recetas.append(receta_actual)

                receta_actual = {
                    "nombre": linea.replace("#", "").strip(),
                    "ingredientes": [],
                    "instrucciones": "",
                }
                modo = None
                continue

            # 🔵 SECCIONES
            # Flexible: detecta encabezados de ingredientes aunque sean solo "Lista"
            if any(x in linea.lower() for x in ["ingredientes", "lista"]):
                modo = "ingredientes"
                continue

            if "instrucciones" in linea.lower() or "preparación" in linea.lower():
                modo = "instrucciones"
                continue

            if not receta_actual:
                continue

            # 🧼 limpiar antes de parsear
            linea = self.limpiar_linea(linea)

            # 🟢 INGREDIENTES
            if modo == "ingredientes":
                match1 = re.search(
                    r"(\d+(?:[\.,]\d+)?)\s*(kg|g)\s+de\s+(.+)", linea, re.IGNORECASE
                )

                match2 = re.search(
                    r"(.+?)\s*:\s*(\d+(?:[\.,]\d+)?)\s*(kg|g)", linea, re.IGNORECASE
                )

                if match1:
                    cantidad_raw = match1.group(1)
                    unidad = self.normalizar_unidad(match1.group(2))
                    nombre = match1.group(3).strip()

                elif match2:
                    nombre = match2.group(1).strip()
                    cantidad_raw = match2.group(2)
                    unidad = self.normalizar_unidad(match2.group(3))

                else:
                    continue

                cantidad = self.parsear_numero(cantidad_raw)

                receta_actual["ingredientes"].append(
                    {"nombre": nombre, "cantidad": cantidad, "unidad": unidad}
                )

            # 🟠 INSTRUCCIONES
            elif modo == "instrucciones":
                receta_actual["instrucciones"] += linea + " "

        # Agregar la última receta
        if receta_actual:
            recetas.append(receta_actual)

        return recetas
