# # views.py
# import datetime
# from django.shortcuts import render
# from core.aplication.services.receta_service import RecetaService
# from core.infrastructure.extractores.xls_extractor import LeerXLSImpl
# from core.infrastructure.extractores.pdf_extractor import LeerPDFImpl
# from core.infrastructure.extractores.md_extractor import LeerMDImpl

# def index_view(request):
#     hoy = datetime.date.today().isoformat()
#     min_fecha = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()

#     # Instanciamos readers con None (archivos ya hardcodeados o en assets)
#     excel_reader = LeerXLSImpl()
#     pdf_reader = LeerPDFImpl()
#     md_reader = LeerMDImpl()

#     # Ejecutamos el servicio para obtener todos los platos
#     service = RecetaService(
#         excel_reader=excel_reader,
#         pdf_reader=pdf_reader,
#         md_reader=md_reader,
#         fecha=hoy,
#     )
#     todos_los_platos = service.ejecutar()  # esto devuelve lista de diccionarios

#     # Extraemos solo los nombres para el <select>
#     nombres_platos = [p["plato"] for p in todos_los_platos]

#     return render(request, "cotizador.html", {
#         "hoy": hoy,
#         "min_fecha": min_fecha,
#         "platos": nombres_platos,
#         "datos_platos": todos_los_platos,  # opcional si quieres filtrar en backend
#     })

# def cotizador_view(request):
#     plato_elegido = request.POST.get("plato")
#     fecha_str = request.POST.get("fecha")

#     # Ejecutamos service de nuevo para obtener todos los platos
#     service = RecetaService(
#         excel_reader=LeerXLSImpl(),
#         pdf_reader=LeerPDFImpl(),
#         md_reader=LeerMDImpl(),
#         fecha=fecha_str,
#     )
#     todos_los_platos = service.ejecutar()

#     # Filtramos solo el plato elegido
#     resultado = [p for p in todos_los_platos if p["plato"] == plato_elegido]

#     return render(request, "partials/cards.html", {"resultado": resultado, "hoy": fecha_str})


# import datetime
# from django.shortcuts import render
# from core.aplication.services.receta_service import RecetaService
# from core.infrastructure.extractores.xls_extractor import LeerXLSImpl
# from core.infrastructure.extractores.pdf_extractor import LeerPDFImpl
# from core.infrastructure.extractores.md_extractor import LeerMDImpl
# from core.aplication.services.cotizador_service import CotizadorService
# from django.core.cache import cache

# def index_view(request):
#     hoy = datetime.date.today().isoformat()

#     # Intentamos levantar los platos del cache
#     todos_los_platos = cache.get('platos_procesados')

#     if not todos_los_platos:
#         print("Cache vacío. Procesando archivos...")
#         service = RecetaService(
#             excel_reader=LeerXLSImpl(),
#             pdf_reader=LeerPDFImpl(),
#             md_reader=LeerMDImpl(),
#             fecha=hoy,
#         )
#         todos_los_platos = service.ejecutar()
#         # Guardamos "para siempre" (None) o por mucho tiempo (ej: 86400 seg = 1 día)
#         cache.set('platos_procesados', todos_los_platos, None)

#     nombres_platos = [p["plato"] for p in todos_los_platos]

#     return render(request, "cotizador.html", {
#         "hoy": hoy,
#         "platos": nombres_platos,
#     })

# def cotizador_view(request):
#     plato_elegido = request.POST.get("plato")
#     print(plato_elegido)
#     for p in cache.get('platos_procesados', []):
#         if plato_elegido == p["plato"]:
#             pesos = p["costo_pesos"]
#             #aca llmar al cotizador con fecha el cotizador me retorna el dolar
#             dolar_ars = # asignacion de dolar obtenido del cotizador via api
#              #y epudo contruir le obejeto o suar el qu tengo aca con retunr  y lsito
#     # Acá ya no procesamos nada, simplemente pedimos al cache
#     if cache.get('platos_procesados')[plato]:
#         print("Cache encontrado. Usando datos en memoria...")
#         print(cache.get('platos_procesados'))  # Imprime el primer plato para verificar que está en cache
#     todos_los_platos = cache.get('platos_procesados')

#     # Filtramos la lista que ya tenemos en memoria
#     resultado = [p for p in todos_los_platos if p["plato"] == plato_elegido] if todos_los_platos else []

#     return render(request, "partials/cards.html", {"resultado": resultado})


import datetime
from django.shortcuts import render
from core.infrastructure.extractores.xls_extractor import LeerXLSImpl
from core.infrastructure.extractores.pdf_extractor import LeerPDFImpl
from core.infrastructure.extractores.md_extractor import LeerMDImpl
from django.core.cache import cache
from core.aplication.services.cotizador_service import CotizadorService
from core.aplication.services.receta_service import RecetaService


def index_view(request):
    hoy = datetime.date.today().isoformat()
    min_fecha = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()

    # Intentamos levantar los platos del cache
    todos_los_platos = cache.get("platos_procesados")

    if not todos_los_platos:
        print("Cache vacío. Procesando archivos...")
        service = RecetaService(
            excel_reader=LeerXLSImpl(),
            pdf_reader=LeerPDFImpl(),
            md_reader=LeerMDImpl(),
            fecha=hoy,
        )
        todos_los_platos = service.ejecutar()
        # Guardamos en cache "para siempre" o por mucho tiempo
        cache.set("platos_procesados", todos_los_platos, None)

    nombres_platos = [p["plato"] for p in todos_los_platos]

    return render(
        request,
        "cotizador.html",
        {
            "hoy": hoy,
            "min_fecha": min_fecha,
            "platos": nombres_platos,
        },
    )


def cotizador_view(request):
    plato_elegido = request.POST.get("plato")
    fecha_str = request.POST.get("fecha") or datetime.date.today().isoformat()

    if not plato_elegido:
        # No se seleccionó plato
        return render(request, "partials/cards.html", {"resultado": []})

    # Obtenemos todos los platos del cache
    todos_los_platos = cache.get("platos_procesados", [])

    # Buscamos el plato elegido
    plato_base = next(
        (p for p in todos_los_platos if p["plato"] == plato_elegido), None
    )

    if not plato_base:
        return render(request, "partials/cards.html", {"resultado": []})

    # Calculamos costo en USD usando el servicio
    resultado = [CotizadorService.calcular_costo_por_fecha(plato_base, fecha_str)]

    return render(request, "partials/cards.html", {"resultado": resultado})
