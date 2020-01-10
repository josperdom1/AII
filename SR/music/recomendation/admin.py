from django.contrib import admin

# the module name is app_name.models
from .models import Artista, UsuarioEtiquetaArtista, Usuario, UsuarioArtista, Etiqueta
# Register your models to admin site, then you can add, edit, delete and search your models in Django admin site.
admin.site.register(Artista)
admin.site.register(UsuarioEtiquetaArtista)
admin.site.register(Usuario)
admin.site.register(UsuarioArtista)
admin.site.register(Etiqueta)