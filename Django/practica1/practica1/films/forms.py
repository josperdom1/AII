from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


class user_id_form(forms.Form):
    userId = forms.IntegerField()


class film_year_form(forms.Form):
    year = forms.DateField(widget=forms.widgets.DateInput(format="%m/%d/%Y"))
