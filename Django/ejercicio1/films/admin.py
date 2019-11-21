from django.contrib import admin

from .models import Film, Category, StandardUser, Director

admin.site.register(Film)
admin.site.register(Category)
admin.site.register(StandardUser)
admin.site.register(Director)