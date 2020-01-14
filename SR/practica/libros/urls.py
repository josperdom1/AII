from django.urls import path
from django.conf.urls import url

from libros.views import *

urlpatterns = [
    url(r'^index/', index, name="index"),
    url(r'^populate/', populate, name="populate"),
    url(r'^search_books/', form_a, name="search_books"),
    url(r'^top_books/', top_books, name="top_books"),
    url(r'^recom/', recom_books, name="recom"),
]