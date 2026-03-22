import logging
import requests
from django.core.cache import cache

logger = logging.getLogger(__name__)


class CotizadorService:
    BASE_URL = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{fecha}/v1/currencies/usd.json"
    TIMEOUT = 5
    CACHE_TTL = 60 * 60 * 24
    FALLBACK = 1400

    @classmethod
    def obtener_dolar(cls, fecha: str) -> float:
        cache_key = f"dolar_{fecha}"
        cached = cache.get(cache_key)

        if cached:
            logger.info("Cotización obtenida desde cache para %s", fecha)
            return cached

        url = cls.BASE_URL.format(fecha=fecha)

        for intento in range(2):  # retry simple
            try:
                response = requests.get(url, timeout=cls.TIMEOUT)
                response.raise_for_status()

                data = response.json()
                valor = float(data["usd"]["ars"])

                cache.set(cache_key, valor, cls.CACHE_TTL)

                return valor

            except Exception as e:
                logger.warning(
                    "Error obteniendo dólar (intento %s): %s", intento + 1, str(e)
                )

        logger.error("Usando fallback para cotización en %s", fecha)
        return cls.FALLBACK
