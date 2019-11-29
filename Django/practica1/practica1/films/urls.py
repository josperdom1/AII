from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from films.views import *

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^search_users/', form_user, name="search_users"),
    url(r'^search_films/', form_film, name="search_films"),
    url(r'^populate/', populate, name="populate"),
    # url(r'^list_films_by_category/', list_films_by_category, name="list_films_by_category"),
    # url(r'^list_directors/', list_directors, name="list_directors"),
]