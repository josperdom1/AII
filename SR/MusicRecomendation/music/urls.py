from django.urls import path, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register("Artista", api.ArtistaViewSet)
router.register("UsuarioEtiquetaArtista", api.UsuarioEtiquetaArtistaViewSet)
router.register("Usuario", api.UsuarioViewSet)
router.register("UsuarioArtista", api.UsuarioArtistaViewSet)
router.register("Etiqueta", api.EtiquetaViewSet)

urlpatterns = (
)
