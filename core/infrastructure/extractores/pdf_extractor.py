import pdfplumber
import re
import logging
from core.aplication.ports.ports import LeerPDFPort

logger = logging.getLogger(__name__)

class LeerPDFImpl(LeerPDFPort):
    EXTENSION = ".pdf"

    def limpiar_precio(self, valor):
        try:
            valor = valor.replace(".", "").replace(",", ".").strip()
            return float(valor)
        except Exception:
            logger.warning(f"Precio inválido: {valor}")
            return None  # decidís ignorarlo

    def leer(self, archivo=None):
        if archivo and hasattr(archivo, "name"):
            if not archivo.name.lower().endswith(self.EXTENSION):
                raise ValueError(f"Archivo inválido, se esperaba un '{self.EXTENSION}'")

        archivo = archivo or "data/verduleria.pdf"
        resultados = []

        try:
            with pdfplumber.open(archivo) as pdf:
                for page in pdf.pages:
                    texto = page.extract_text()

                    if not texto:
                        logger.warning("Página sin texto detectado")
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

                            if precio is None:
                                continue  # ignora línea inválida

                            resultados.append({
                                "nombre": nombre,
                                "precio": precio,
                                "tipo": "Verdura"
                            })

        except Exception as e:
            logger.exception("Error leyendo PDF")
            raise Exception(f"Error leyendo PDF: {str(e)}")

        return resultados