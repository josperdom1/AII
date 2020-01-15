from django.db import models


class Offer(models.Model):

    #  Relationships
    degrees = models.ManyToManyField('Degree')

    #  Fields
    offerId = models.IntegerField(primary_key=True)
    university = models.TextField(default='University')
    enterprise = models.TextField(default='Enterprise')
    months = models.IntegerField(default=0)
    salary = models.IntegerField(default=0)
    country = models.TextField(default='Country')
    province = models.TextField(default='Province')
    city = models.TextField(default='City')
    description = models.TextField(default='Description')
    immediate = models.BooleanField(default=True)


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
    name = models.TextField(max_length=100)





