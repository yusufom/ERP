from django.contrib import admin

from .models import todo, dashboard

admin.site.register(todo)
admin.site.register(dashboard)