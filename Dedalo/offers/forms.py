from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


class user_id_form(forms.Form):
    userId = forms.IntegerField()

class text_form(forms.Form):
    query = forms.CharField( max_length=100)