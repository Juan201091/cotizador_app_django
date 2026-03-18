import pandas as pd
import re
from core.aplication.ports.ports import LeerXLSPort


class LeerXLSImpl(LeerXLSPort):
    # ==============================
    # Normalizar texto
    # ==============================
    def normalizar_texto(self, valor):
        if pd.isna(valor):
            return ""

        valor = str(valor)
        valor = valor.strip()
        valor = re.sub(r"\s+", " ", valor)
        return valor

    # ==============================
    # Limpiar precio (robusto)
    # ==============================
    def limpiar_precio(self, valor):
        if pd.isna(valor):
            return None

        valor = str(valor)
        valor = valor.replace("$", "").strip()

        # Soporta formatos: 6.800 / 6,800 / 6.800,50
        if "," in valor:
            valor = valor.replace(".", "").replace(",", ".")
        else:
            valor = valor.replace(".", "")

        try:
            return float(valor)
        except:
            return None

    # ==============================
    # Construir item
    # ==============================
    def construir_item(self, nombre, precio, tipo):
        return {"nombre": nombre, "precio": precio, "tipo": tipo}

    # ==============================
    # Leer Excel
    # ==============================
    def leer(self, path: str = "data/CarnesyPescados.xlsx"):
        df = pd.read_excel(path, header=None)

        resultados = []

        # ==============================
        # 1. Detectar fila con "Corte"
        # ==============================
        header_row = None

        for i, row in df.iterrows():
            if "Corte" in row.values:
                header_row = i
                break

        if header_row is None:
            raise ValueError("No se encontró encabezado 'Corte'")

        # 🔥 NO saltamos la fila (clave para no perder pescado)
        df_data = df.iloc[header_row:].reset_index(drop=True)

        # Columnas (según tu Excel actual)
        col_nombre_carne = 2
        col_precio_carne = 3

        col_nombre_pescado = 5
        col_precio_pescado = 6

        tipo_actual = "Vacuna"

        # ==============================
        # 2. Iterar filas
        # ==============================
        for idx, row in df_data.iterrows():
            # ===== CARNE =====
            nombre = row[col_nombre_carne]
            precio_raw = row[col_precio_carne]

            if pd.notna(nombre):
                nombre_str = self.normalizar_texto(nombre).lower()
                precio = self.limpiar_precio(precio_raw)

                # ❌ Ignorar headers (PERO NO cortar ejecución)
                if nombre_str in ["corte", "precio (ars/kg)"]:
                    pass

                # 🔄 Cambios de tipo
                elif nombre_str == "carne de cerdo":
                    tipo_actual = "Cerdo"

                elif nombre_str == "pollo":
                    tipo_actual = "Pollo"

                # ✅ Guardar dato válido
                elif precio is not None and nombre_str != "":
                    resultados.append(
                        self.construir_item(nombre_str.title(), precio, tipo_actual)
                    )
                else:
                    print(f"[CARNE IGNORADA] fila {idx}: '{nombre}' - '{precio_raw}'")

            # ===== PESCADO (SIEMPRE se evalúa) =====
            nombre_p = row[col_nombre_pescado]
            precio_p_raw = row[col_precio_pescado]

            if pd.notna(nombre_p):
                nombre_p_str = self.normalizar_texto(nombre_p).lower()
                precio_p = self.limpiar_precio(precio_p_raw)

                # ❌ Ignorar headers
                if nombre_p_str in ["tipo", "precio (ars/kg)"]:
                    pass

                # ✅ Guardar dato válido
                elif precio_p is not None and nombre_p_str != "":
                    resultados.append(
                        self.construir_item(nombre_p_str.title(), precio_p, "Pescado")
                    )
                else:
                    print(
                        f"[PESCADO IGNORADO] fila {idx}: '{nombre_p}' - '{precio_p_raw}'"
                    )

        # ==============================
        # 3. Ordenar resultados
        # ==============================
        orden_tipos = {"Vacuna": 0, "Cerdo": 1, "Pollo": 2, "Pescado": 3}

        resultados.sort(key=lambda x: orden_tipos.get(x["tipo"], 99))

        return resultados
