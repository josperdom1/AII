from django import forms


class user_id_form(forms.Form):
    userId = forms.IntegerField()


class film_year_form(forms.Form):
    year = forms.IntegerField()
