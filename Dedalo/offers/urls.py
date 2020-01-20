from django.urls import path
from django.conf.urls import url

from offers.views import *

urlpatterns = [
    url(r'^index/', index, name="index"),
    url(r'^populate/', populate, name="populate"),
    url(r'^extractcsv/', extract_csv, name="extract_csv"),
    url(r'^popularoffers/', popular_offers , name="popular_offers"),
    url(r'^myoffers/', my_offers, name="my_offers"),
    # url(r'^top_books/', top_books, name="top_books"),
    # url(r'^recom/', recom_books, name="recom"),
]