from django.contrib import admin

from .models import Torneos, Equipos, Partidos, Tarjetas, Apuestas
# Register your models here.

admin.site.register(Torneos)
admin.site.register(Equipos)
admin.site.register(Partidos)
admin.site.register(Tarjetas)
admin.site.register(Apuestas)
