from django.shortcuts import render

# Create your views here.
def populate(request):
    tumetodo()
    return render(request, 'films/success.html')