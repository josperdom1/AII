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
import time
import random
from djqscsv import write_csv
from django.http.response import HttpResponse
from djqscsv.djqscsv import render_to_csv_response
from djqscsv import render_to_csv_response
from whoosh.fields import Schema, TEXT, NUMERIC, BOOLEAN, ID
import os.path
from whoosh.index import create_in, open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser, MultifieldParser


def populate(request):
    populate_offers()
    populate_users()
    populate_user_offer()
    return render(request, 'offers/index.html')


def search(q):
    qparser = MultifieldParser(["description", "enterprise", "university", "province", "city"], get_whoosh_schema())

    user_q = qparser.parse(q)

    with get_whoosh_index().searcher() as s:
        results = s.search(user_q)
        return [Offer.objects.get(pk=result.get('offerId')) for result in results]


def get_whoosh_schema():
    return Schema(offerId=ID(stored=True), university=TEXT(stored=True),
                  enterprise=TEXT(stored=True), months=NUMERIC(stored=True),
                  salary=NUMERIC(stored=True), country=TEXT(stored=True),
                  province=TEXT(stored=True), city=TEXT(stored=True),
                  description=TEXT(stored=True), immediate=BOOLEAN(stored=True))

def get_whoosh_index():
    if not os.path.exists("whoosh_index"):
        os.mkdir("whoosh_index")
        return create_in("whoosh_index", schema=get_whoosh_schema())
    else:
        return open_dir("whoosh_index")
    

def create_whoosh_index(offers):
    writer = get_whoosh_index().writer()

    for o in offers:
        writer.add_document(offerId=str(o.offerId), university=o.university,
                        enterprise=o.enterprise, months=o.months,
                        salary=o.salary, country=o.country,
                        province=o.province, city=o.city,
                        description=o.description, immediate=o.immediate)
    writer.commit()


def populate_offers():
    Offer.objects.all().delete()
    # Degree.objects.all().delete()

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

    for offerId in range(267700, 268000):

        print(f"==== {offerId} ====")

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
            try: university = general_info.find("dt", string="Universidad").find_next("dd").string
            except: university = None

            try: months = int(general_info.find("dt", string="Duración").find_next("dd").string.replace(" meses", ""))  # Nota: añadir el caso para cuando ponga años
            except: months = None

            try: salary = int(general_info.find("dt", string=["Dotación", "Dotación/Mes"]).find_next("dd").string.replace(" euros", ""))
            except: salary = None

            try: country = general_info.find("dt", string="País").find_next("dd").string
            except: country = None

            try: province = general_info.find("dt", string="Provincia").find_next("dd").string
            except: province = None

            try: city = general_info.find("dt", string="Localidad").find_next("dd").string
            except: city = None

            try: description = general_info.find("dt", string=["Tareas a Realizar", "Detalle Actividades Diarias",
                                                              "Proyecto Formativo"]).find_next("dd").string
            except: description = None
            
            # REQUISITOS
            degrees = []
            if requisites_info:
                try:
                    estudies = requisites_info.find("dt", string="Estudios").find_next("dd")
                    estudies_list = estudies.find_all("li")

                    if estudies_list:
                        degree_set = set(degree.string for degree in estudies_list) # To avoid repeated elements
                        print(f"DEGREE SET: {degree_set}")
                        for degree in degree_set:
                            degrees.append(Degree.objects.get_or_create(name=degree.string)[0])
                            print(degrees)
                    else:
                        degrees.append(Degree.objects.get_or_create(name=degree.string)[0])
                        print(degrees)
                except:
                    pass

                try: immediate = requisites_info.find("dt", string="Incorporación Inmediata").find_next("dd").string == "SI"
                except: immediate = None

            
            # #REQUISITOS
            # if requisites_info is not None:
            #     titles = requisites_info.find_all("dt")

            #     for title in titles:
            #         title_str = title.string
            #         index = titles.index(title)

            #         studies = []

            #         if title_str == "Estudios":

            #             list_st = requisites_info.find_all("dd")[index]
            #             list_st_ul = list_st.find("ul")

            #             if list_st_ul is None:
            #                 offer.append(list_st.get_text())

            #             else:
            #                 studies_degrees = list_st_ul.find_all("li")
            #                 for degree in studies_degrees:
            #                     dg = degree
            #                     studies.append(dg.get_text())

            #                 offer.append(studies)

            #         if title_str == "Incorporación Inmediata":

            #             inmediate = requisites_info.find_all("dd")[index].string

            #             if inmediate == "SI":
            #                 inmediate_value = True

            #             if inmediate == "NO":
            #                 inmediate_value = False
                        
            #             offer.append(inmediate_value)

            offer = Offer(offerId=offerId, university=university, enterprise=enterprise, months=months, salary=salary,
                      country=country, province=province, city=city, description=description, immediate=immediate)
            
            offer.save()

            offers.append(offer)

            # if degrees_tuple:
            #     degrees = []
            #     for degree_tuple in degrees_tuple:
            #         degrees.append(degree_tuple[0])
            #         if degree_tuple[1]:
            #             degree_tuple[0].save()
            #             print(degree_tuple[0])

                # degrees = [d[0] for d in degrees_tuple]

                # for d in degrees:
                #     print(d)
                #     d.save()
                #     print(d)
                
                # offer.degrees.set(degrees)
            
            try:
                offer.degrees.set(degrees)
            except:
                pass

            #time.sleep(random.uniform(0.2, 0.8))  # Para evitar posibles baneos

    #Offer.objects.bulk_create(offers)
    create_whoosh_index(offers)


def get_keywords(offer_list, num_words):
    all_descriptions = ""
    for offer in offer_list:
        if offer.description:
            all_descriptions += f" {offer.description}"
    
    with get_whoosh_index().searcher() as s:
        return [x[0] for x in s.key_terms_from_text("description", all_descriptions, num_words)]


def populate_users():
    User.objects.all().delete()
    User.objects.bulk_create([User() for i in range(288)])

    all_degrees = Degree.objects.all()
    for user in User.objects.all():
        for degree in random.choices(all_degrees, k=random.randint(1, 2)):
            user.degrees.add(degree)


def populate_user_offer():
    User_offer.objects.all().delete()

    all_users = User.objects.all()
    all_offers = Offer.objects.all()

    user_offers_list = []

    for user in all_users:
        for offer in random.choices(all_offers, k=random.randint(10, 150)):
            user_offers_list.append(User_offer(offer=offer, user=user, like=bool(random.getrandbits(1))))

    User_offer.objects.bulk_create(user_offers_list)


## ---------------------------------------------------------------------------------------------------------------------


def index(request):
    return render(request, 'offers/index.html')


def extract_csv(request):
    qs = Offer.objects.all()
    return render_to_csv_response(qs)


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


def search_offers(request):
    context = {}
    if request.method == 'POST':
        form = text_form(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            offers = search(query)
            context.__setitem__('offers', offers)
    else:
        form = text_form()

    context.__setitem__('form', form)

    return render(request, 'offers/form_a.html', context)


def popular_offers(request):
    offers = Offer.objects.annotate(number=Count('user_offer')).order_by('-number')[:10]
    return render(request, 'offers/top_offers.html', {'offers': offers})


def recom(request):
    context = {}
    if request.method == 'POST':
        form = user_id_form(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['userId']
            offers = recom_offers(user_id)
            context.__setitem__('offers', offers)
    else:
        form = user_id_form()

    context.__setitem__('form', form)

    return render(request, 'offers/form_a.html', context)


def Sort(sub_li):
    sub_li.sort(key=lambda x: x[1], reverse=True)
    return sub_li



def offer_similarity(my_keywords, off2):
    si = []
    list = []
    list.append(off2)

    #Get the list of similar keywords
    for w in get_keywords(list, 20):
        if w in my_keywords:
            si.append(w)

    #Number of keywords in common
    return len(si)


def recom_offers(user_id):
    my_offers = Offer.objects.filter(user_offer__user_id=user_id, user_offer__like=True).order_by('-salary')
    no_rated_offers = Offer.objects.exclude(user_offer__user_id=user_id).order_by('-salary')
    my_keywords = get_keywords(my_offers, 50)

    res = []
    #List with non rated offers and its similarity based on keywords coincidence
    for o in no_rated_offers:
        res.append([o, offer_similarity(my_keywords, o)])

    #Normalization
    max = Sort(res)[0][1]
    for e in res:
        e[1] = e[1]/max

    #We order by similarity and return only offers
    return [x[0] for x in Sort(res)]
