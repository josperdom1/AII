from django import forms


class language_form(forms.Form):
    language = forms.CharField(max_length=30)


class event_month_form(forms.Form):
    month = forms.DateField(widget=forms.widgets.DateInput(format="%d/%m/%Y"))
