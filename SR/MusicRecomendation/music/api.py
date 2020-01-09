from rest_framework import viewsets, permissions

from . import serializers
from . import models


class ArtistaViewSet(viewsets.ModelViewSet):
    """ViewSet for the Artista class"""

    queryset = models.Artista.objects.all()
    serializer_class = serializers.ArtistaSerializer
    permission_classes = [permissions.IsAuthenticated]


class UsuarioEtiquetaArtistaViewSet(viewsets.ModelViewSet):
    """ViewSet for the UsuarioEtiquetaArtista class"""

    queryset = models.UsuarioEtiquetaArtista.objects.all()
    serializer_class = serializers.UsuarioEtiquetaArtistaSerializer
    permission_classes = [permissions.IsAuthenticated]


class UsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet for the Usuario class"""

    queryset = models.Usuario.objects.all()
    serializer_class = serializers.UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]


class UsuarioArtistaViewSet(viewsets.ModelViewSet):
    """ViewSet for the UsuarioArtista class"""

    queryset = models.UsuarioArtista.objects.all()
    serializer_class = serializers.UsuarioArtistaSerializer
    permission_classes = [permissions.IsAuthenticated]


class EtiquetaViewSet(viewsets.ModelViewSet):
    """ViewSet for the Etiqueta class"""

    queryset = models.Etiqueta.objects.all()
    serializer_class = serializers.EtiquetaSerializer
    permission_classes = [permissions.IsAuthenticated]
