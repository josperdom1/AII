from django.db import models

class Libro(models.Model):
    #  Fields
    bookId = models.IntegerField(primary_key=True)
    titulo = models.TextField(max_length=100)
    autor = models.TextField(max_length=100)
    genero = models.TextField(max_length=100)
    idioma = models.TextField(max_length=100)
    one = models.IntegerField()
    two = models.IntegerField()
    three = models.IntegerField()
    four = models.IntegerField()
    five = models.IntegerField()



class Puntuacion(models.Model):

    #  Relationships
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)

    #  Fields
    puntuacion = models.IntegerField()



class Usuario(models.Model):

    #  Fields
    idUsuario = models.IntegerField(primary_key=True)
    libro = models.ManyToManyField(Libro, through='Puntuacion')



