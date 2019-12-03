from django.db import models
from django.urls import reverse


class Language(models.Model):

    #  Fields
    name = models.CharField(max_length=30)


class Municipio(models.Model):

    #  Fields
    name = models.CharField(max_length=30)


class Event(models.Model):
    #  Relationships
    language = models.ManyToManyField(Language)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

    #  Fields
    name = models.CharField(max_length=30)
    start_date = models.DateField()
    location = models.CharField(max_length=30)
    type = models.TextField(max_length=100)
