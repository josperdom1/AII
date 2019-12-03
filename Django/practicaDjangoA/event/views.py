from django.db.models.aggregates import Avg
from django.shortcuts import render
from django.shortcuts import render
from django.db import models
from .models import Event, Language, Municipio
import datetime as dt
from django.shortcuts import render
from .models import Event, Language, Municipio

# Create your views here.
from event.forms import event_month_form, language_form


def populate_languages():
    Language.objects.all().delete()
    with open("lenguas.csv", "r") as languages_file:
        language_lines = [line.rstrip() for line in languages_file.readlines()]
    languages = [Language(name=l) for l in language_lines]
    Language.objects.bulk_create(languages)


def populate_municipios():
    Municipio.objects.all().delete()
    with open("municipio.csv", "r") as municipios_file:
        municipio_lines = [line.rstrip().replace("\ufeff", "") for line in municipios_file.readlines()]
    print(municipio_lines)
    municipios = [Municipio(name=m) for m in municipio_lines]
    Municipio.objects.bulk_create(municipios)


def populate(request):
    populate_languages()
    populate_municipios()

    return render(request, 'event/index.html')


def date_parser(date_str):
    try:
        return dt.datetime.strptime(date_str, "%d-%b-%Y")
    except:
        return None


def index(request):
    return render(request, 'event/index.html')


def form_language(request):
    context = {}
    if request.method == 'POST':
        form = language_form(request.POST)
        if form.is_valid():
            language = form.cleaned_data['language']
            municipios = Municipio.objects.filter(language__name=language)
            context.__setitem__('municipios', municipios)
    else:
        form = language_form()

    context.__setitem__('form', form)

    return render(request, 'event/form_search_by_language.html', context)


def form_month(request):
    context = {}
    if request.method == 'POST':
        form = event_month_form(request.POST)
        if form.is_valid():
            month_form = form.cleaned_data['month']
            print(month_form.month)
            events = Event.objects.filter(start_date__month=month_form.month)
            context.__setitem__('events', events)
    else:
        form = event_month_form()

    context.__setitem__('form', form)

    return render(request, 'event/form_search_by_month.html', context)


def show_grouped_events(request):
    events = Event.objects.all().order_by('type')
    return render(request, 'event/show_all_events.html', {'events': events})


def show_municipio(request):
    municipios = Municipio.objects.annotate(events_number='event'.count() ).order_by('-events_number')[:2]

    return render(request, 'event/top_2_municipios.html', {'municipios': municipios})
