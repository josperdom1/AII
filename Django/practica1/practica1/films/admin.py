from django.contrib import admin
from films.models import *

# Register your models here.
admin.site.register(Film)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Occupation)
admin.site.register(Rate)
