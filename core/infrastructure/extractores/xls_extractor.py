import pandas as pd
import re
from core.aplication.ports.ports import LeerXLSPort

import logging
logger = logging.getLogger(__name__)

class LeerXLSImpl(LeerXLSPort):
    def normalizar_texto(self, valor):
        if pd.isna(valor):
            return ""

        valor = str(valor)
        valor = valor.strip()
        valor = re.sub(r"\s+", " ", valor)
        return valor

    def limpiar_precio(self, valor):
        if pd.isna(valor):
            return None

        valor = str(valor)
        valor = valor.replace("$", "").strip()

        if "," in valor:
            valor = valor.replace(".", "").replace(",", ".")
        else:
            valor = valor.replace(".", "")

        try:
            return float(valor)
        except:
            return None

    def construir_item(self, nombre, precio, tipo):
        return {"nombre": nombre, "precio": precio, "tipo": tipo}

    def leer(self, path: str = "data/CarnesyPescados.xlsx"):
        try:
            df = pd.read_excel(path, header=None)
        except Exception:
            logger.exception("Error leyendo Excel: %s", path)
            return []

        resultados = []

        # ==============================
        # 1. Detectar header
        # ==============================
        header_row = None

        for i, row in df.iterrows():
            if "Corte" in row.values:
                header_row = i
                break

        if header_row is None:
            logger.error("No se encontró encabezado 'Corte'")
            return []

        df_data = df.iloc[header_row:].reset_index(drop=True)

        col_nombre_carne = 2
        col_precio_carne = 3

        col_nombre_pescado = 5
        col_precio_pescado = 6

        tipo_actual = "Vacuna"

        for idx, row in df_data.iterrows():
            try:
                # ===== CARNES =====
                nombre = row[col_nombre_carne]
                precio_raw = row[col_precio_carne]

                if pd.notna(nombre):
                    nombre_str = self.normalizar_texto(nombre).lower()
                    precio = self.limpiar_precio(precio_raw)

                    if nombre_str in ["corte", "precio (ars/kg)"]:
                        pass

                    elif nombre_str == "carne de cerdo":
                        tipo_actual = "Cerdo"

                    elif nombre_str == "pollo":
                        tipo_actual = "Pollo"

                    elif precio is not None and nombre_str != "":
                        resultados.append(
                            self.construir_item(nombre_str.title(), precio, tipo_actual)
                        )
                    else:
                        logger.warning(
                            "[CARNE IGNORADA] fila %s: '%s' - '%s'",
                            idx, nombre, precio_raw
                        )

                # ===== PESCADO Siempre Se Busca =====
                nombre_p = row[col_nombre_pescado]
                precio_p_raw = row[col_precio_pescado]

                if pd.notna(nombre_p):
                    nombre_p_str = self.normalizar_texto(nombre_p).lower()
                    precio_p = self.limpiar_precio(precio_p_raw)

                    if nombre_p_str in ["tipo", "precio (ars/kg)"]:
                        pass

                    elif precio_p is not None and nombre_p_str != "":
                        resultados.append(
                            self.construir_item(nombre_p_str.title(), precio_p, "Pescado")
                        )
                    else:
                        logger.warning(
                            "[PESCADO IGNORADO] fila %s: '%s' - '%s'",
                            idx, nombre_p, precio_p_raw
                        )

            except Exception:
                logger.exception("Error procesando fila %s", idx)
                continue

        #  Ordenar por tipo: Vacuna, Cerdo, Pollo, Pescado
        
        orden_tipos = {"Vacuna": 0, "Cerdo": 1, "Pollo": 2, "Pescado": 3}

        resultados.sort(key=lambda x: orden_tipos.get(x["tipo"], 99))

        logger.info("Items leídos desde Excel: %s", len(resultados))

        return resultados