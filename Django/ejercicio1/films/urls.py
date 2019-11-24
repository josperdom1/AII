from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^list_standard_users/', list_standard_users, name="list_standard_users"),
    url(r'^list_films_by_category/', list_films_by_category, name="list_films_by_category"),
    url(r'^list_directors/', list_directors, name="list_directors"),
]
