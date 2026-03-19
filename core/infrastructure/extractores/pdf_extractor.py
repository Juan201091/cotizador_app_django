import pdfplumber
import re
from core.aplication.ports.ports import LeerPDFPort

class LeerPDFImpl(LeerPDFPort):
    EXTENSION = ".pdf"

    def limpiar_precio(self, valor):
        valor = valor.replace(".", "").replace(",", ".").strip()
        return float(valor)

    def leer(self, archivo=None):
        if archivo and not str(archivo.name).lower().endswith(self.EXTENSION):
            raise ValueError(f"Archivo inválido, se esperaba un '{self.EXTENSION}'")

        archivo = archivo or "data/verduleria.pdf"
        resultados = []

        with pdfplumber.open(archivo) as pdf:
            for page in pdf.pages:
                texto = page.extract_text()
                if not texto:
                    print("[SIN TEXTO DETECTADO]")
                    continue
                for linea in texto.split("\n"):
                    linea = linea.strip()
                    if not linea or "http" in linea.lower():
                        continue
                    if any(x in linea.lower() for x in ["built with", "actualizado", "precios", "lista", "consulte"]):
                        continue
                    match = re.search(r"(.+?)\s+\$([\d\.,]+)", linea)
                    if match:
                        nombre = match.group(1).strip()
                        precio_raw = match.group(2)
                        precio = self.limpiar_precio(precio_raw)
                        resultados.append({
                            "nombre": nombre,
                            "precio": precio,
                            "tipo": "Verdura"
                        })
        return resultados


# import pdfplumber
# import re
# from core.aplication.ports.ports import LeerPDFPort


# class LeerPDFImpl(LeerPDFPort):
#     EXTENSION = ".pdf"

#     def __init__(self, archivo=None):
#         """
#         archivo: puede ser un path str o un UploadedFile de Django
#         """
#         if archivo and not str(archivo.name).lower().endswith(self.EXTENSION):
#             raise ValueError(f"Archivo inválido, se esperaba '{self.EXTENSION}'")
#         self.archivo = archivo

#     # ==============================
#     # Limpiar precio
#     # ==============================
#     def limpiar_precio(self, valor):
#         valor = valor.replace(".", "").replace(",", ".").strip()
#         try:
#             return float(valor)
#         except:
#             return None

#     # ==============================
#     # Leer PDF
#     # ==============================
#     def leer(self, archivo=None):
#         """
#         archivo: opcional. Si se pasa, se usa este archivo en lugar de self.archivo
#         """
#         archivo_a_usar = archivo or self.archivo
#         if not archivo_a_usar:
#             raise ValueError("No se proporcionó archivo para leer")

#         resultados = []

#         with pdfplumber.open(archivo_a_usar) as pdf:
#             for page in pdf.pages:
#                 texto = page.extract_text()
#                 if not texto:
#                     print("[SIN TEXTO DETECTADO]")
#                     continue

#                 for linea in texto.split("\n"):
#                     linea = linea.strip()
#                     if not linea or "http" in linea.lower():
#                         continue
#                     if any(
#                         x in linea.lower()
#                         for x in [
#                             "built with",
#                             "actualizado",
#                             "precios",
#                             "lista",
#                             "consulte",
#                         ]
#                     ):
#                         continue

#                     # 🔥 Detectar producto + precio
#                     match = re.search(r"(.+?)\s+\$([\d\.,]+)", linea)
#                     if match:
#                         nombre = match.group(1).strip()
#                         precio_raw = match.group(2)
#                         precio = self.limpiar_precio(precio_raw)
#                         if precio is not None:
#                             resultados.append(
#                                 {"nombre": nombre, "precio": precio, "tipo": "Verdura"}
#                             )

#         return resultados
