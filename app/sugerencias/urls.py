"""
URLs para la API de sugerencias.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from sugerencias import views


router = DefaultRouter()
router.register("", views.SugerenciaPlatoViewSet)

app_name = "sugerencias"

urlpatterns = [
    path("", include(router.urls)),
]
