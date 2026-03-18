import pdfplumber
import re
from core.aplication.ports.ports import LeerXLSPort


class LeerPDFImpl(LeerXLSPort):

    def limpiar_precio(self, valor):
        valor = valor.replace(".", "").replace(",", "").strip()
        return float(valor)

    def leer(self, path: str = "data/verduleria.pdf"):
        resultados = []

        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages):

                texto = page.extract_text()


                if not texto:
                    print("[SIN TEXTO DETECTADO]")
                    continue

                lineas = texto.split("\n")

                for linea in lineas:
                    linea = linea.strip()

                    # ❌ ignorar ruido
                    if not linea or "http" in linea.lower():
                        continue

                    if any(x in linea.lower() for x in [
                        "built with", "actualizado", "precios", "lista", "consulte"
                    ]):
                        continue

                    # 🔥 detectar producto + precio
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