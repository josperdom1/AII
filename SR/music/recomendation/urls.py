from django.urls import path
from django.conf.urls import url

from recomendation.views import *

urlpatterns = [
    url(r'^index/', index, name="index"),
    url(r'^populate/', populate, name="populate"),
    url(r'^search_artist/', form_a, name="search_artist"),
]