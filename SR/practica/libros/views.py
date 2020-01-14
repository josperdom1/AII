from django.shortcuts import render
from django.db import models
from django.db.models import F, Q, Exists, Value, IntegerField, Sum
from .models import *
import csv
import datetime as dt
from libros.forms import *
from collections import Counter
import itertools

data_path = "./goodreads-dataset/"


def populate(request):
    populate_books()
    populate_users()
    populate_ratings()

    return render(request, 'libros/index.html')


def populate_books():
    Libro.objects.all().delete()
    with open(data_path + "bookfeatures.csv", "r", encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        next(csv_reader)
        list_to_create = [Libro(bookId=row[0], titulo=row[1], autor=row[2], genero=row[3], idioma=row[4], one=row[5], two=row[6], three=row[7], four=row[8], five=row[9]) for row in csv_reader]
    Libro.objects.bulk_create(list_to_create)


def populate_users():
    Usuario.objects.all().delete()
    with open(data_path + "ratings.csv", "r", encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        next(csv_reader)
        list_to_create = [Usuario(idUsuario=row[1]) for row in csv_reader]
    Usuario.objects.bulk_create(list(set(list_to_create)))


def populate_ratings():
    Puntuacion.objects.all().delete()
    with open(data_path + "ratings.csv", "r", encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        next(csv_reader)
        list_to_create = [Puntuacion(puntuacion=row[0], usuario=Usuario.objects.get(idUsuario=row[1]), libro=Libro.objects.get(bookId=row[2])) for row in csv_reader]
    Puntuacion.objects.bulk_create(list_to_create)

def index(request):
    return render(request, 'libros/index.html')


def sim_distance(u1, u2):
    # Get the list of mutually rated items
    qset1 = Libro.objects.filter(usuario=u1)
    qset2 = Libro.objects.filter(usuario=u2)

    books1 = list(qset1)
    books2 = list(qset2)
    si = {}
    for item in books1:
        if item in books2: si[item] = 1


    # if they have no ratings in common, return 0
    if len(si) == 0: return 0

    # Add up the squares of all the differences
    sum_of_squares = sum([pow( Puntuacion.objects.get(usuario=u1 ,libro=item).puntuacion - Puntuacion.objects.get(usuario=u2 ,libro=item).puntuacion, 2)
                          for item in books1 if item in books2])

    return 1 / (1 + sum_of_squares)


def topMatches (userId, similarity=sim_distance):

    users = Usuario.objects.exclude(idUsuario=userId)
    print(users)
    user = Usuario.objects.get(idUsuario=userId)

    scores =[[other, similarity(user, other)]
                  for other in users]
    print(scores)
    res = Sort(scores)
    return res[0]

def form_a(request):
    context = {}
    if request.method == 'POST':
        form = genero_form(request.POST)
        if form.is_valid():
            genero = form.cleaned_data['genero']
            books = Libro.objects.filter(genero=genero)
            context.__setitem__('books', books)
    else:
        form = genero_form()

    context.__setitem__('form', form)

    return render(request, 'libros/form_a.html', context)

def max_books():
    books = Libro.objects.all()
    books_rate = []
    for b in books:
        element = []
        try:

            rate = (b.one + b.two*2 + b.three*3 + b.four*4 + b.five*5)/(b.one + b.two + b.three + b.four + b.five)
        except:
            rate = 0

        element.append(b)
        element.append(rate)
        books_rate.append(element)

    return Sort(books_rate)


def top_books(request):

    return render(request, 'libros/top_books.html', {'books': max_books()[:3]})


def recom(request):
    context = {}
    if request.method == 'POST':
        form = user_id_form(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['userId']
            usuario = topMatches(user_id)
            print(usuario)
            context.__setitem__('usuario', usuario[0])
    else:
        form = user_id_form()

    context.__setitem__('form', form)

    return render(request, 'libros/recom.html', context)

def recom_books(request):
    context = {}
    if request.method == 'POST':
        form = user_id_form(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['userId']
            libros = Libro.objects.filter(usuario__idUsuario=user_id)
            nice_libros = [i[0] for i in Sort(max_books())[:6]]
            res = [libro for libro in nice_libros if libro not in libros]

            context.__setitem__('books', res)
    else:
        form = user_id_form()

    context.__setitem__('form', form)

    return render(request, 'libros/form_a.html', context)


def Sort(sub_li):
    sub_li.sort(key=lambda x: x[1], reverse=True)
    return sub_li
