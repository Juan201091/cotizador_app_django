"""
Serializers para la API de sugerencias.
"""
from rest_framework import serializers

from sugerencias.models import SugerenciaPlato


class SugerenciaPlatoSerializer(serializers.ModelSerializer):
    """Serializer de sugerencias de platos."""

    class Meta:
        model = SugerenciaPlato
        fields = [
            "id",
            "nombre",
            "descripcion",
            "ingredientes",
            "autor",
            "estado",
            "creado",
            "actualizado",
        ]
        read_only_fields = ["id", "creado", "actualizado"]
