from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from films.views import *

from practica1.films.views import index

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^users_by_occupation/', show_user_by_occupation, name="user_by_occupation"),
    url(r'^top_rated_films/', show_top_films, name="top_rated_films"),
    url(r'^search_users/', form_user, name="search_users"),
    url(r'^search_films/', form_film, name="search_films"),
    url(r'^populate/', populate, name="populate"),
    # url(r'^list_films_by_category/', list_films_by_category, name="list_films_by_category"),
    # url(r'^list_directors/', list_directors, name="list_directors"),
]