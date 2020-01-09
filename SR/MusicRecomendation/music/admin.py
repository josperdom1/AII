from django.contrib import admin
from django import forms

from . import models


class ArtistaAdminForm(forms.ModelForm):

    class Meta:
        model = models.Artista
        fields = "__all__"


class ArtistaAdmin(admin.ModelAdmin):
    form = ArtistaAdminForm
    list_display = [
        "Url",
        "PictureUrl",
        "Nombre",
        "IdArtista",
    ]
    readonly_fields = [
        "Url",
        "PictureUrl",
        "Nombre",
        "IdArtista",
    ]


class UsuarioEtiquetaArtistaAdminForm(forms.ModelForm):

    class Meta:
        model = models.UsuarioEtiquetaArtista
        fields = "__all__"


class UsuarioEtiquetaArtistaAdmin(admin.ModelAdmin):
    form = UsuarioEtiquetaArtistaAdminForm
    list_display = [
        "Fecha",
    ]
    readonly_fields = [
        "Fecha",
    ]


class UsuarioAdminForm(forms.ModelForm):

    class Meta:
        model = models.Usuario
        fields = "__all__"


class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioAdminForm
    list_display = [
        "IdUsuario",
    ]
    readonly_fields = [
        "IdUsuario",
    ]


class UsuarioArtistaAdminForm(forms.ModelForm):

    class Meta:
        model = models.UsuarioArtista
        fields = "__all__"


class UsuarioArtistaAdmin(admin.ModelAdmin):
    form = UsuarioArtistaAdminForm
    list_display = [
        "TiempoEscucha",
    ]
    readonly_fields = [
        "TiempoEscucha",
    ]


class EtiquetaAdminForm(forms.ModelForm):

    class Meta:
        model = models.Etiqueta
        fields = "__all__"


class EtiquetaAdmin(admin.ModelAdmin):
    form = EtiquetaAdminForm
    list_display = [
        "TagValue",
        "IdTag",
    ]
    readonly_fields = [
        "TagValue",
        "IdTag",
    ]


admin.site.register(models.Artista, ArtistaAdmin)
admin.site.register(models.UsuarioEtiquetaArtista, UsuarioEtiquetaArtistaAdmin)
admin.site.register(models.Usuario, UsuarioAdmin)
admin.site.register(models.UsuarioArtista, UsuarioArtistaAdmin)
admin.site.register(models.Etiqueta, EtiquetaAdmin)
