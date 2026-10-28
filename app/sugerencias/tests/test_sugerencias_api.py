"""
Tests para la API de sugerencias.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from sugerencias.models import SugerenciaPlato


SUGERENCIAS_URL = reverse("sugerencias:sugerenciaplato-list")


def detalle_url(sugerencia_id):
    return reverse("sugerencias:sugerenciaplato-detail", args=[sugerencia_id])


def crear_sugerencia(**params):
    defaults = {
        "nombre": "Milanesa con puré",
        "ingredientes": "Nalga\nPapa",
    }
    defaults.update(params)
    return SugerenciaPlato.objects.create(**defaults)


class SugerenciasApiTests(TestCase):
    """Tests del CRUD de sugerencias."""

    def setUp(self):
        self.client = APIClient()

    def test_listar_sugerencias(self):
        crear_sugerencia()
        crear_sugerencia(nombre="Guiso de lentejas")

        res = self.client.get(SUGERENCIAS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_crear_sugerencia(self):
        payload = {
            "nombre": "Empanadas de carne",
            "ingredientes": "Carne picada\nCebolla",
            "autor": "Juan",
        }

        res = self.client.post(SUGERENCIAS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        sugerencia = SugerenciaPlato.objects.get(id=res.data["id"])
        self.assertEqual(sugerencia.nombre, payload["nombre"])
        self.assertEqual(sugerencia.estado, SugerenciaPlato.Estado.PENDIENTE)

    def test_crear_sugerencia_sin_nombre_falla(self):
        res = self.client.post(SUGERENCIAS_URL, {"ingredientes": "Papa"})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_actualizar_estado(self):
        sugerencia = crear_sugerencia()

        res = self.client.patch(
            detalle_url(sugerencia.id), {"estado": "aprobada"}
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        sugerencia.refresh_from_db()
        self.assertEqual(sugerencia.estado, SugerenciaPlato.Estado.APROBADA)

    def test_estado_invalido_falla(self):
        sugerencia = crear_sugerencia()

        res = self.client.patch(
            detalle_url(sugerencia.id), {"estado": "cualquiera"}
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_borrar_sugerencia(self):
        sugerencia = crear_sugerencia()

        res = self.client.delete(detalle_url(sugerencia.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            SugerenciaPlato.objects.filter(id=sugerencia.id).exists()
        )
