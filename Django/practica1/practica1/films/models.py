from django.core.validators import URLValidator
from django.db import models


# Create your models here.
class User(models.Model):
    uid = models.IntegerField(primary_key=True)
    age = models.PositiveSmallIntegerField()
    sex = models.CharField(choices=["M", "F"])
    postal_code = models.CharField()

    occupation = models.ForeignKey('Occupation', on_delete=models.SET_NULL)


class Occupation(models.Model):
    name = models.CharField()


class Category(models.Model):
    cid = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=500)


class Film(models.Model):
    fid = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    year = models.DateField()
    url = models.URLField()
    rating = models.ManyToManyField('Rate', through=User)

    categories = models.ManyToManyField(Category)


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    number = models.SmallIntegerField()

    categories = models.ManyToManyField(Category)


