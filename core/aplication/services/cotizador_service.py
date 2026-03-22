import logging
import requests

logger = logging.getLogger(__name__)


class CotizadorService:
    @staticmethod
    def obtener_dolar(fecha: str) -> float:
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{fecha}/v1/currencies/usd.json"

        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()
            return float(data["usd"]["ars"])

        except Exception:
            logger.exception("Error obteniendo dólar")
            # En caso de error, se puede optar por un valor fijo o lanzar una excepción o consultar otra fuente
            return 1400