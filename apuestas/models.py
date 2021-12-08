from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Torneos(models.Model):
    nombre = models.CharField(max_length=200)
    fechas = models.IntegerField(default=0)
    activo = models.BooleanField(default=False)
    abierto = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.nombre
    
class Equipos(models.Model):
    nombre = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre

class Partidos(models.Model):
    torneo = models.ForeignKey(Torneos, on_delete=models.CASCADE)
    equipo_1 = models.ForeignKey(Equipos, related_name='+')
    equipo_2 = models.ForeignKey(Equipos, related_name='+')
    jugado = models.BooleanField(default=False)
    goles_1  = models.IntegerField(default=0)
    goles_2  = models.IntegerField(default=0)

    def __str__(self):
        return '{0} - {1}'.format(self.equipo_1.nombre, self.equipo_2.nombre)

class Tarjetas(models.Model):
    torneo = models.ForeignKey(Torneos, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    puntos = models.IntegerField(default = 0)

    def __str__(self):
        return '{0} / {1}'.format(self.user.username, self.torneo)
    


class Apuestas(models.Model):
    tarjeta = models.ForeignKey(Tarjetas, on_delete=models.CASCADE)
    partido = models.ForeignKey(Partidos, on_delete=models.CASCADE)
    goles_1  = models.IntegerField(default=0)
    goles_2  = models.IntegerField(default=0)
    puntos = models.IntegerField(default = 0)
    
    def __str__(self):
        return '{0}({1}) - {2}({3})'.format(self.partido.equipo_1.nombre, self.goles_1,  self.partido.equipo_2.nombre, self.goles_2)
