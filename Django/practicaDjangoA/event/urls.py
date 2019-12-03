from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from event.views import *

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^show_gruoped_events/', show_grouped_events, name="show_grouped_events"),
    url(r'^show_municipio/', show_municipio, name="show_municipio"),
    url(r'^form_month/', form_month, name="form_month"),
    url(r'^form_language/', form_language, name="form_language"),
    url(r'^populate/', populate, name="populate"),
    # url(r'^search_films/', form_film, name="search_films"),
    # url(r'^populate/', populate, name="populate"),
]