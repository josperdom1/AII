from django.shortcuts import render
from django.db import models
from .models import Artista, UsuarioEtiquetaArtista, Usuario, UsuarioArtista, Etiqueta
import csv
import datetime as dt
from recomendation.forms import *

data_path = "./hetrec2011-lastfm-2k/"


def populate(request):
    populate_artists()
    populate_tags()
    populate_users()
    populate_user_artists()
    populate_user_taggedartists()

    return render(request, 'recomendation/populate.html')


def populate_artists():
    Artista.objects.all().delete()
    with open(data_path + "artists.dat", "r", encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)
        list_to_create = [Artista(idArtista=row[0], nombre=row[1], url=row[2], pictureUrl=row[3]) for row in csv_reader]
    Artista.objects.bulk_create(list_to_create)


def populate_tags():
    Etiqueta.objects.all().delete()
    with open(data_path + "tags.dat", "r", encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)
        list_to_create = [Etiqueta(idTag=row[0], tagValue=row[1]) for row in csv_reader]
    print(list_to_create)
    Etiqueta.objects.bulk_create(list_to_create)


def populate_users():
    Usuario.objects.all().delete()
    Usuario.objects.bulk_create([Usuario(idUsuario=i) for i in range(2101)])


def populate_user_artists():
    UsuarioArtista.objects.all().delete()
    with open(data_path + "user_artists.dat", "r", encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)
        list_to_create = [
            UsuarioArtista(usuario=Usuario.objects.get(idUsuario=row[0]), artista=Artista.objects.get(idArtista=row[1]),
                           tiempoEscucha=row[2]) for row in csv_reader]
    UsuarioArtista.objects.bulk_create(list_to_create)


def populate_user_taggedartists():
    UsuarioEtiquetaArtista.objects.all().delete()
    with open(data_path + "user_taggedartists.dat", "r", encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)
        list_to_create = []
        for row in csv_reader:
            try:
                artista=Artista.objects.get(idArtista=row[1])
            except:
                artista=Artista.objects.get(idArtista=1)
            uea = UsuarioEtiquetaArtista(usuario=Usuario.objects.get(idUsuario=row[0]),
                                    artista=artista,
                                    tag=Etiqueta.objects.get(idTag=row[2]),
                                    fecha=dt.date(int(row[5]), int(row[4]), int(row[3])))
            list_to_create.append(uea)
    UsuarioEtiquetaArtista.objects.bulk_create(list_to_create)


def index(request):
    return render(request, 'recomendation/index.html')


def form_a(request):
    context = {}
    if request.method == 'POST':
        form = user_id_form(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['userId']
            artists = Artist.objects.filter(Usuario__idUsuario=user_id)
            context.__setitem__('artists', artists)
    else:
        form = user_id_form()

    context.__setitem__('form', form)

    return render(request, 'recomendation/form_a.html', context)


def form_b():
    return true
