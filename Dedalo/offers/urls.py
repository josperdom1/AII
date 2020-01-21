from django.urls import path
from django.conf.urls import url

from offers.views import *

urlpatterns = [
    url(r'^index/', index, name="index"),
    url(r'^populate/', populate, name="populate"),
    url(r'^extractcsv/', extract_csv, name="extract_csv"),
    url(r'^popularoffers/', popular_offers , name="popular_offers"),
    url(r'^myoffers/', my_offers, name="my_offers"),
    url(r'^search/', search_offers, name="search_offers"),
    url(r'^recom/', recom, name="recom_offers"),
    # url(r'^recom/', recom_books, name="recom"),
]