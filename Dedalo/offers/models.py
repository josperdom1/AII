from django.db import models


class Offer(models.Model):

    #  Relationships
    degrees = models.ManyToManyField('Degree')

    #  Fields
    offerId = models.IntegerField(primary_key=True)
    university = models.TextField(blank=True, null=True)
    enterprise = models.TextField(blank=True, null=True)
    months = models.IntegerField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    immediate = models.BooleanField(blank=True, null=True)


class User_offer(models.Model):

    #  Relationships
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    #  Fields
    userOfferId = models.IntegerField(primary_key=True)
    like = models.BooleanField()


class User(models.Model):

    #  Relationships
    degrees = models.ManyToManyField('Degree')

    #  Fields
    userId = models.IntegerField(primary_key=True)


class Degree(models.Model):

    #  Fields
    degreeId = models.IntegerField(primary_key=True)
    name = models.TextField(max_length=100) # , unique=True





