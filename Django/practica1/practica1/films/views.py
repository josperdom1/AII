from django.db.models.aggregates import Avg
from django.shortcuts import render
from django.shortcuts import render
from django.db import models
from .models import User, Occupation, Category, Film, Rate
import datetime as dt
import collections
import operator

# Create your views here.
from films.forms import user_id_form, film_year_form


def populate(request):
    populate_categories()
    populate_occupations()
    populate_users()
    populate_films()
    populate_ratings()
    print("success")
    return render(request, 'films/index.html')


def date_parser(date_str):
    try:
        return dt.datetime.strptime(date_str, "%d-%b-%Y")
    except:
        return None


def populate_occupations():
    Occupation.objects.all().delete()
    with open("/home/andres/AII/Django/practica1/ml-100k/u.occupation", "r") as occupations_file:
        occupations = [line.rstrip() for line in occupations_file.readlines()]
    occupation_array = [Occupation(name=o) for o in occupations]
    Occupation.objects.bulk_create(occupation_array)


def populate_categories():
    Category.objects.all().delete()
    with open("/home/andres/AII/Django/practica1/ml-100k/u.genre", "r") as categories_file:
        categories = [line.rstrip().split("|") for line in categories_file.readlines()]
    category_array = [Category(c[1], c[0]) for c in categories[:-1]]  # -1 because there is a blank line at the end
    Category.objects.bulk_create(category_array)


def populate_users():
    User.objects.all().delete()
    with open("/home/andres/AII/Django/practica1/ml-100k/u.user", "r") as users_file:
        users = [line.rstrip().split("|") for line in users_file]
    users_array = [User(uid=u[0], age=u[1], sex=u[2], postal_code=u[4], occupation=Occupation.objects.get(name=u[3]))
                   for u in users]
    User.objects.bulk_create(users_array)


def populate_films():
    Film.objects.all().delete()
    with open("/home/andres/AII/Django/practica1/ml-100k/u.item", "rb") as films_file:
        films = [line.decode("latin1").rstrip().split("|") for line in films_file]
    films_array = [Film(fid=f[0], title=f[1], year=date_parser(f[2]), url=f[4]) for f in films]
    Film.objects.bulk_create(films_array)


def populate_ratings():
    Rate.objects.all().delete()
    with open("/home/andres/AII/Django/practica1/ml-100k/u.data", "r") as ratings_file:
        ratings = [line.rstrip().split("\t") for line in ratings_file]
    ratings_array = [Rate(user=User.objects.get(uid=r[0]), film=Film.objects.get(fid=r[1]), number=r[2]) for r in
                     ratings]
    Rate.objects.bulk_create(ratings_array)


def index(request):
    return render(request, 'films/index.html')


def form_user(request):
    context = {}
    if request.method == 'POST':
        form = user_id_form(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['userId']
            rates = Rate.objects.filter(user=user_id)
            context.__setitem__('rates', rates)
    else:
        form = user_id_form()

    context.__setitem__('form', form)

    return render(request, 'films/form.html', context)


def form_film(request):
    context = {}
    if request.method == 'POST':
        form = film_year_form(request.POST)
        if form.is_valid():
            year_form = form.cleaned_data['year']
            print(year_form.year)
            films = Film.objects.filter(year__year=year_form.year)
            context.__setitem__('films', films)
    else:
        form = film_year_form()

    context.__setitem__('form', form)

    return render(request, 'films/films_form.html', context)


def show_top_films(request):
    films = Film.objects.annotate(avg_rating=Avg('rate__number')).order_by('-avg_rating')[:5]
    return render(request, 'films/top_films.html', {'films': films})


def show_user_by_occupation(request):
    users = User.objects.raw('SELECT * FROM FILMS_USER GROUP BY OCCUPATION_ID')

    return render(request, 'films/show_users.html', {'users': users})
