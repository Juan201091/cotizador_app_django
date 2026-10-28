"""
Vistas para la API de sugerencias.
"""
from rest_framework import viewsets

from sugerencias.models import SugerenciaPlato
from sugerencias.serializers import SugerenciaPlatoSerializer


class SugerenciaPlatoViewSet(viewsets.ModelViewSet):
    """CRUD de sugerencias de platos."""

    queryset = SugerenciaPlato.objects.all()
    serializer_class = SugerenciaPlatoSerializer
