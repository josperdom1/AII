from django.shortcuts import render
from django.db import models
from django.db.models import F, Q, Exists, Value, IntegerField, Sum
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

    return render(request, 'recomendation/index.html')


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
    Etiqueta.objects.bulk_create(list_to_create)


def populate_users():
    Usuario.objects.all().delete()
    Usuario.objects.bulk_create([Usuario(idUsuario=i) for i in range(2101)])


def populate_user_artists():
    UsuarioArtista.objects.all().delete()
    with open(data_path + "user_artists.dat", "r", encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)
        list_to_create = []
        for row in csv_reader:
            try:
                ua = UsuarioArtista(usuario=Usuario.objects.get(idUsuario=row[0]),
                                    artista=Artista.objects.get(idArtista=row[1]),
                                    tiempoEscucha=row[2])
                list_to_create.append(ua)
            except:
                pass

    UsuarioArtista.objects.bulk_create(list_to_create)


def populate_user_taggedartists():
    UsuarioEtiquetaArtista.objects.all().delete()
    with open(data_path + "user_taggedartists.dat", "r", encoding="ISO-8859-1") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        next(csv_reader)
        list_to_create = []
        for row in csv_reader:
            try:
                uea = UsuarioEtiquetaArtista(usuario=Usuario.objects.get(idUsuario=row[0]),
                                             artista=Artista.objects.get(idArtista=row[1]),
                                             tag=Etiqueta.objects.get(idTag=row[2]),
                                             fecha=dt.date(int(row[5]), int(row[4]), int(row[3])))
                list_to_create.append(uea)
            except:
                pass

    UsuarioEtiquetaArtista.objects.bulk_create(list_to_create)


def index(request):
    return render(request, 'recomendation/index.html')


def form_a(request):
    context = {}
    if request.method == 'POST':
        form = user_id_form(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['userId']
            try:
                list = []
                arts = Artista.objects.filter(usuario__idUsuario=user_id)

                for a in arts:
                    item = []
                    time = UsuarioArtista.objects.filter(usuario_id=user_id, artista_id=a.idArtista).first().tiempoEscucha
                    item.append(a)
                    item.append(time)
                    list.append(item)
            except:
                pass

            context.__setitem__('artists', list)
    else:
        form = user_id_form()

    context.__setitem__('form', form)

    return render(request, 'recomendation/form_a.html', context)


def top_artist(request):
    artists = Artista.objects.annotate(time=Sum('usuarioartista__tiempoEscucha')).order_by('-time')[:3]
    return render(request, 'recomendation/top_artists.html', {'artists': artists})
