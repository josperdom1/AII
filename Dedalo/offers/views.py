# coding: utf-8
from django.shortcuts import render
from django.db import models
from django.db.models import *
from .models import *
import csv
import datetime as dt
from offers.forms import *
from collections import Counter
import itertools
from robobrowser import RoboBrowser
import time, random
from djqscsv import write_csv
from django.http.response import HttpResponse
from djqscsv.djqscsv import render_to_csv_response
from djqscsv import render_to_csv_response


def populate(request):
    # populate_offers()
    # populate_users()
    # populate_user_offer()
    return render(request, 'offers/index.html')


def populate_offers():
    Offer.objects.all().delete()

    username = "dedalo1234"
    password = "dedalo4321"

    browser = RoboBrowser(history=True, parser="lxml")
    browser.open("https://icaro.ual.es/acceso/")

    form = browser.get_form(id='form1')
    form["ctl00$contenido$txtLogin"].value = username
    form["ctl00$contenido$txtPassword"].value = password
    form["ctl00$contenido$btnAcceder"].value = "Acceder"
    browser.submit_form(form, submit=form['ctl00$contenido$btnAcceder'])

    offers = []

    for offerId in range(252000, 252600):

        job_offer_url = f"https://icaro.ual.es/Empresas/Ofertas/Presentacion.aspx?codOferta={offerId}"
        browser.open(job_offer_url)

        # main blocks
        enterprise_info = browser.find("dl", "presentacion_datos_2")
        offer_info = browser.find_all("dl", "presentacion_datos")

        if offer_info:
            general_info = offer_info[0]
            if len(offer_info) > 1:
                requisites_info = offer_info[1]

            # EMPRESA
            if enterprise_info is not None:
                try:
                    enterprise = enterprise_info.find("dt", string="Empresa").find_next("dd").string
                except:
                    enterprise = None
            else:
                enterprise = None

            # INFORMACIÓN GENERAL
            try:
                university = general_info.find("dt", string="Universidad").find_next("dd").string
            except:
                university = None

            try:
                months = int(general_info.find("dt", string="Duración").find_next("dd").string.replace(" meses",
                                                                                                       ""))  # Nota: añadir el caso para cuando ponga años
            except:
                months = None

            try:
                salary = int(
                    general_info.find("dt", string=["Dotación", "Dotación/Mes"]).find_next("dd").string.replace(
                        " euros", ""))
            except:
                salary = None

            try:
                country = general_info.find("dt", string="País").find_next("dd").string
            except:
                country = None

            try:
                province = general_info.find("dt", string="Provincia").find_next("dd").string
            except:
                province = None

            try:
                city = general_info.find("dt", string="Localidad").find_next("dd").string
            except:
                city = None

            try:
                description = general_info.find("dt", string=["Tareas a Realizar", "Detalle Actividades Diarias",
                                                              "Proyecto Formativo"]).find_next("dd").string
            except:
                description = None

            offers.append(
                Offer(offerId=offerId, university=university, enterprise=enterprise, months=months, salary=salary,
                      country=country, province=province, city=city, description=description))

            time.sleep(random.uniform(0.2, 0.8))  # Para evitar posibles baneos

    Offer.objects.bulk_create(offers)


def extract_csv(request):
    qs = Offer.objects.all()
    return render_to_csv_response(qs)


def populate_users():
    User.objects.all().delete()
    User.objects.bulk_create([User() for i in range(288)])


def populate_user_offer():
    User_offer.objects.all().delete()

    all_users = User.objects.all()
    all_offers = Offer.objects.all()

    user_offers_list = []

    for user in all_users:
        for offer in random.choices(all_offers, k=random.randint(10, 150)):
            user_offers_list.append(User_offer(offer=offer, user=user, like=bool(random.getrandbits(1))))

    User_offer.objects.bulk_create(user_offers_list)


# def populate_offers():
# Offer.objects.all().delete()
# with open(data_path + "bookfeatures.csv", "r", encoding="ISO-8859-1") as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=";")
#     next(csv_reader)
#     list_to_create = [Offer(bookId=row[0], titulo=row[1], autor=row[2], genero=row[3], idioma=row[4], one=row[5], two=row[6], three=row[7], four=row[8], five=row[9]) for row in csv_reader]
# Offer.objects.bulk_create(list_to_create)
#
#
# def populate_users():
#     Usuario.objects.all().delete()
#     with open(data_path + "ratings.csv", "r", encoding="ISO-8859-1") as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=";")
#         next(csv_reader)
#         list_to_create = [Usuario(idUsuario=row[1]) for row in csv_reader]
#     Usuario.objects.bulk_create(list(set(list_to_create)))
#
#
# def populate_ratings():
#     Puntuacion.objects.all().delete()
#     with open(data_path + "ratings.csv", "r", encoding="ISO-8859-1") as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=";")
#         next(csv_reader)
#         list_to_create = [Puntuacion(puntuacion=row[0], usuario=Usuario.objects.get(idUsuario=row[1]), libro=Libro.objects.get(bookId=row[2])) for row in csv_reader]
#     Puntuacion.objects.bulk_create(list_to_create)

def index(request):
    return render(request, 'offers/index.html')


# def sim_distance(u1, u2):
#     # Get the list of mutually rated items
#     qset1 = Libro.objects.filter(usuario=u1)
#     qset2 = Libro.objects.filter(usuario=u2)

#     books1 = list(qset1)
#     books2 = list(qset2)
#     si = {}
#     for item in books1:
#         if item in books2: si[item] = 1


#     # if they have no ratings in common, return 0
#     if len(si) == 0: return 0

#     # Add up the squares of all the differences
#     sum_of_squares = sum([pow( Puntuacion.objects.get(usuario=u1 ,libro=item).puntuacion - Puntuacion.objects.get(usuario=u2 ,libro=item).puntuacion, 2)
#                           for item in books1 if item in books2])

#     return 1 / (1 + sum_of_squares)


# def topMatches (userId, similarity=sim_distance):

#     users = Usuario.objects.exclude(idUsuario=userId)
#     print(users)
#     user = Usuario.objects.get(idUsuario=userId)

#     scores =[[other, similarity(user, other)]
#                   for other in users]
#     print(scores)
#     res = Sort(scores)
#     return res[0]

def my_offers(request):
    context = {}
    if request.method == 'POST':
        form = user_id_form(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['userId']
            offers = Offer.objects.filter(user_offer__user_id=user_id, user_offer__like=True).order_by('-salary')
            context.__setitem__('offers', offers)
    else:
        form = user_id_form()

    context.__setitem__('form', form)

    return render(request, 'offers/form_a.html', context)


def popular_offers(request):
    offers = Offer.objects.annotate(number=Count('user_offer')).order_by('-number')[:10]
    return render(request, 'offers/top_offers.html', {'offers': offers})


# def max_books():
#     books = Libro.objects.all()
#     books_rate = []
#     for b in books:
#         element = []
#         try:

#             rate = (b.one + b.two*2 + b.three*3 + b.four*4 + b.five*5)/(b.one + b.two + b.three + b.four + b.five)
#         except:
#             rate = 0

#         element.append(b)
#         element.append(rate)
#         books_rate.append(element)

#     return Sort(books_rate)


# def recom(request):
#     context = {}
#     if request.method == 'POST':
#         form = user_id_form(request.POST)
#         if form.is_valid():
#             user_id = form.cleaned_data['userId']
#             usuario = topMatches(user_id)
#             print(usuario)
#             context.__setitem__('usuario', usuario[0])
#     else:
#         form = user_id_form()

#     context.__setitem__('form', form)

#     return render(request, 'offers/recom.html', context)

# def recom_books(request):
#     context = {}
#     if request.method == 'POST':
#         form = user_id_form(request.POST)
#         if form.is_valid():
#             user_id = form.cleaned_data['userId']
#             libros = Libro.objects.filter(usuario__idUsuario=user_id)
#             nice_libros = [i[0] for i in Sort(max_books())[:6]]
#             res = [libro for libro in nice_libros if libro not in libros]

#             context.__setitem__('books', res)
#     else:
#         form = user_id_form()

#     context.__setitem__('form', form)

#     return render(request, 'offers/form_a.html', context)


def Sort(sub_li):
    sub_li.sort(key=lambda x: x[1], reverse=True)
    return sub_li
