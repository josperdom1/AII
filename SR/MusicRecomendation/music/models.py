from django.db import models
from django.urls import reverse


class Artista(models.Model):

    #  Fields
    url = models.URLField()
    pictureUrl = models.URLField()
    nombre = models.TextField(max_length=100)
    idArtista = models.IntegerField(primary_key=True)


class UsuarioEtiquetaArtista(models.Model):

    #  Relationships
    idArtista = models.ForeignKey("Artista", on_delete=models.CASCADE)
    idTag = models.ForeignKey("Etiqueta", on_delete=models.CASCADE)
    idUsuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)

    #  Fields
    fecha = models.DateField()
    idUsuarioEtiquetaArtista = models.IntegerField(primary_key=True)




class Usuario(models.Model):

    #  Fields
    idUsuario = models.IntegerField(primary_key=True)
    artistas = models.ManyToManyField(Artista, through='UsuarioArtista')


class UsuarioArtista(models.Model):

    #  Relationships
    idArtista = models.ForeignKey("Artista", on_delete=models.CASCADE)
    idUsuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)

    #  Fields
    tiempoEscucha = models.IntegerField()



class Etiqueta(models.Model):
    #  Fields
    tagValue = models.TextField(max_length=100)
    idTag = models.IntegerField(primary_key=True)

