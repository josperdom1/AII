from django.shortcuts import render

# Create your views here.
from films.forms import user_id_form


def populate(request):
    tumetodo()
    return render(request, 'films/success.html')


def index(request):
    return render(request, 'films/index.html')


def form(request):
    if request.method == 'POST':
        form = user_id_form(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['userId']
            print(user_id)

    form = user_id_form()
    return render(request, 'films/form.html', {'form': form})
