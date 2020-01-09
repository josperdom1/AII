from rest_framework import serializers

from . import models


class ArtistaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Artista
        fields = [
            "Url",
            "PictureUrl",
            "Nombre",
            "IdArtista",
        ]

class UsuarioEtiquetaArtistaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UsuarioEtiquetaArtista
        fields = [
            "Fecha",
        ]

class UsuarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Usuario
        fields = [
            "IdUsuario",
        ]

class UsuarioArtistaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UsuarioArtista
        fields = [
            "TiempoEscucha",
        ]

class EtiquetaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Etiqueta
        fields = [
            "TagValue",
            "IdTag",
        ]
