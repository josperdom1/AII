from django.shortcuts import render, redirect
from .models import *


def index(request):
    return render(request, 'films/index.html')


def list_standard_users(request):
    # Django ORM
    users = StandardUser.objects.all()
    context = {'users': users}
    return render(request, 'films/list_standard_users.html', context)


def list_films_by_category(request):
    films = Film.objects.raw('SELECT * FROM films_film')
    context = {'films': films}
    return render(request, 'films/list_films_by_category.html', context)


def list_directors(request):

    directors = []
    for director in Director.objects.all():
        director_films = Film.objects.filter(director=director)
        directors.append({'director': director, 'films': director_films})

    context = {'directors': directors}
    return render(request, 'films/list_directors.html', context)
