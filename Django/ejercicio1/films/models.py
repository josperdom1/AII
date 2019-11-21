import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.TextField(max_length=500)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name):
        return cls(name=name)


class StandardUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=500)
    surname = models.TextField(max_length=500)
    birth_date = models.DateField(null=True, blank=True)

    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.name + " " + self.surname


class Director(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=500, blank=True)
    surname = models.TextField(max_length=500)
    biography = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name + " " + self.surname


class Film(models.Model):
    title = models.CharField(max_length=100, unique=True)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1900),
                                                        MaxValueValidator(datetime.datetime.now().year)],
                                            verbose_name="Year")
    summary = models.TextField(verbose_name='Summary')

    categories = models.ManyToManyField(Category)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
