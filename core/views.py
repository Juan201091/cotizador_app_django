import datetime
from django.shortcuts import render
from django.core.cache import cache
from core.composition_root.composition_services import get_recetas_use_case, get_calcular_costo_use_case
import logging

logger = logging.getLogger(__name__)


def index_view(request):
    hoy = datetime.date.today().isoformat()
    min_fecha = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()

    try:
        data = cache.get("platos_base")

        if not data:
            logger.info("Cache sin datos - iniciado carga desde fuentes de datos")

            use_case = get_recetas_use_case()
            platos, precios = use_case.ejecutar()

            data = (platos, precios)
            cache.set("platos_base", data, 60 * 60)

        else:
            logger.info("Cache con datos - usando datos en memoria")

        platos, _ = data
        logger.info("Cantidad de platos disponibles: %s", len(platos))

        return render(
            request,
            "cotizador.html",
            {"platos": [p.nombre for p in platos], "hoy": hoy, "min_fecha": min_fecha},
        )

    except Exception:
        logger.exception("Error al cargar los datos")
        return render(
            request,
            "cotizador.html",
            {
                "platos": [],
                "hoy": hoy,
                "min_fecha": min_fecha,
                "error": "No se pudieron cargar los datos",
            },
        )


def cotizador_view(request):
    plato_nombre = request.POST.get("plato")
    fecha = request.POST.get("fecha")

    if not plato_nombre:
        return render(request, "partials/cards.html", {"resultado": []})

    data = cache.get("platos_base")

    if not data:
        return render(request, "partials/cards.html", {"resultado": []})

    platos, precios = data

    use_case = get_calcular_costo_use_case()

    resultado = use_case.execute(
        platos,
        precios,
        fecha,
        plato_nombre
    )

    return render(request, "partials/cards.html", {"resultado": resultado})
