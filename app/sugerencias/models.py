"""
Modelos para las sugerencias de platos.
"""
from django.db import models


class SugerenciaPlato(models.Model):
    """Plato propuesto para agregar al recetario."""

    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        APROBADA = "aprobada", "Aprobada"
        RECHAZADA = "rechazada", "Rechazada"

    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True)
    ingredientes = models.TextField(help_text="Un ingrediente por línea")
    autor = models.CharField(max_length=80, blank=True)
    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-creado"]

    def __str__(self):
        return self.nombre
