from django.contrib import admin

from sugerencias.models import SugerenciaPlato


@admin.register(SugerenciaPlato)
class SugerenciaPlatoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "autor", "estado", "creado"]
    list_filter = ["estado"]
    search_fields = ["nombre", "autor"]
