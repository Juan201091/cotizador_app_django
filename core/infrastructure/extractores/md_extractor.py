import re
from core.aplication.ports.ports import LeerMDPort


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

        with open(archivo, "r", encoding="utf-8") if isinstance(archivo, str) else archivo.open("r", encoding="utf-8") as file:
            lineas = file.readlines()

        receta_actual = None
        modo = None

        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
            if linea.startswith("# "):
                if receta_actual:
                    recetas.append(receta_actual)
                receta_actual = {"nombre": linea.replace("#", "").strip(),
                                 "ingredientes": [], "instrucciones": ""}
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
                    continue
                cantidad = self.parsear_numero(cantidad_raw)
                receta_actual["ingredientes"].append({"nombre": nombre, "cantidad": cantidad, "unidad": unidad})
            elif modo == "instrucciones":
                receta_actual["instrucciones"] += linea + " "
        if receta_actual:
            recetas.append(receta_actual)
        return recetas

# import re
# from core.aplication.ports.ports import LeerMDPort


# class LeerMDImpl(LeerMDPort):
#     EXTENSION = ".md"

#     def __init__(self, archivo=None):
#         """
#         archivo: puede ser un path str o un UploadedFile de Django
#         """
#         if archivo and not str(archivo.name).lower().endswith(self.EXTENSION):
#             raise ValueError(f"Archivo inválido, se esperaba '{self.EXTENSION}'")
#         self.archivo = archivo

#     # ==============================
#     # Parsear número (1,5 -> 1.5)
#     # ==============================
#     def parsear_numero(self, valor):
#         try:
#             return float(valor.replace(",", ".").strip())
#         except:
#             return None

#     # ==============================
#     # Normalizar unidad
#     # ==============================
#     def normalizar_unidad(self, unidad):
#         return "gr" if unidad.lower() == "g" else "kg"

#     # ==============================
#     # Limpiar línea
#     # ==============================
#     def limpiar_linea(self, linea):
#         return re.sub(r"^\s*([-*]|\d+\.|[a-zA-Z]\.)\s*", "", linea).strip()

#     # ==============================
#     # Leer Markdown
#     # ==============================
#     def leer(self, archivo=None):
#         if archivo and not str(archivo.name).lower().endswith(self.EXTENSION):
#             raise ValueError(f"Archivo inválido, se esperaba un '{self.EXTENSION}'")

#         archivo = archivo or "data/Recetas.md"
#         recetas = []

#         if isinstance(archivo, str):
#             with open(archivo, "r", encoding="utf-8") as file:
#                 lineas = file.readlines()
#         else:
#             contenido = archivo.read().decode("utf-8")
#             lineas = contenido.splitlines()

#         receta_actual = None
#         modo = None

#         for linea in lineas:
#             linea = linea.strip()
#             if not linea:
#                 continue
#             if linea.startswith("# "):
#                 if receta_actual:
#                     recetas.append(receta_actual)
#                 receta_actual = {"nombre": linea.replace("#", "").strip(),
#                                 "ingredientes": [], "instrucciones": ""}
#                 modo = None
#                 continue
#             if any(x in linea.lower() for x in ["ingredientes", "lista"]):
#                 modo = "ingredientes"
#                 continue
#             if "instrucciones" in linea.lower() or "preparación" in linea.lower():
#                 modo = "instrucciones"
#                 continue
#             if not receta_actual:
#                 continue
#             linea = self.limpiar_linea(linea)
#             if modo == "ingredientes":
#                 match1 = re.search(r"(\d+(?:[\.,]\d+)?)\s*(kg|g)\s+de\s+(.+)", linea, re.IGNORECASE)
#                 match2 = re.search(r"(.+?)\s*:\s*(\d+(?:[\.,]\d+)?)\s*(kg|g)", linea, re.IGNORECASE)
#                 if match1:
#                     cantidad_raw = match1.group(1)
#                     unidad = self.normalizar_unidad(match1.group(2))
#                     nombre = match1.group(3).strip()
#                 elif match2:
#                     nombre = match2.group(1).strip()
#                     cantidad_raw = match2.group(2)
#                     unidad = self.normalizar_unidad(match2.group(3))
#                 else:
#                     continue
#                 cantidad = self.parsear_numero(cantidad_raw)
#                 receta_actual["ingredientes"].append({"nombre": nombre, "cantidad": cantidad, "unidad": unidad})
#             elif modo == "instrucciones":
#                 receta_actual["instrucciones"] += linea + " "
#         if receta_actual:
#             recetas.append(receta_actual)
#         return recetas