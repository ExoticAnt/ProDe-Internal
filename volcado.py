from apuestas.models import Torneos, Equipos, Partidos, Tarjetas, Apuestas
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Min, Sum, Avg
from django.contrib.auth.models import User


pd = [("Rusia","Arabia Saudita"),
("Egipto","Uruguay"),
("Marruecos","Iran"),
("Portugal","España"),
("Francia","Australia"),
("Argentina","Islandia"),
("Peru","Dinamarca"),
("Croacia","Nigeria"),
("Costa Rica","Serbia"),
("Alemania","Mexico"),
("Brasil","Suiza"),
("Suecia","Corea del Sur"),
("Belgica","Panama"),
("Tunez","Inglaterra"),
("Colombia","Japon"),
("Polonia","Senegal"),
("Rusia","Egipto"),
("Portugal","Marruecos"),
("Uruguay","Arabia Saudita",2,0),
("Iran","España",0,4),
("Dinamarca","Australia",1,2),
("Francia","Peru",2,1),
("Argentina","Croacia",2,1),
("Brasil","Costa Rica",2,0),
("Nigeria","Islandia",2,1),
("Serbia","Suiza",0,1),
("Belgica","Tunez",2,0),
("Corea del Sur","Mexico",1,3),
("Alemania","Suecia",2,0),
("Inglaterra","Panama",2,0),
("Japon","Senegal",2,3),
("Polonia","Colombia",1,1),
("Uruguay","Rusia",2,1),
("Arabia Saudita","Egipto",0,2),
("Iran","Portugal",1,3),
("España","Marruecos",3,0),
("Dinamarca","Francia",0,2),
("Australia","Peru",0,1),
("Nigeria","Argentina",1,3),
("Islandia","Croacia",0,2),
("Corea del Sur","Alemania",1,3),
("Mexico","Suecia",2,2),
("Serbia","Brasil",0,3),
("Suiza","Costa Rica",0,2),
("Japon","Polonia",1,1),
("Senegal","Colombia",0,2),
("Inglaterra","Belgica",1,2),
("Panama","Tunez",0,2)]

uu = 'nvega@kioshi.com.ar'

aps = [
(1, 0),
(0, 2),
(0, 1),
(1, 2),
(2, 0),
(1, 0),
(2, 0),
(1, 0),
(1, 0),
(2, 0),
(2, 0),
(1, 0),
(2, 0),
(0, 2),
(1, 0),
(1, 0),
(0, 1),
(1, 0),
(1, 0),
(0, 2),
(0, 1),
(1, 0),
(2, 0),
(3, 0),
(2, 1),
(0, 1),
(2, 0),
(0, 2),
(3, 0),
(2, 0),
(1, 0),
(1, 3),
(2, 0),
(1, 2),
(0, 2),
(3, 0),
(1, 2),
(0, 1),
(0, 1),
(1, 2),
(0, 4),
(1, 0),
(1, 3),
(2, 1),
(1, 0),
(0, 2),
(3, 1),
(1, 0)
]

def get_torneo_activo():
    ts = Torneos.objects.filter(activo = True)
    ta = -1
    for t in ts:
        if t.activo == True:
            ta = t.id
    if ta == -1:
        raise("No hay torneo activo")
    return Torneos.objects.get(id = ta)
    

def run():
    u = User.objects.create_user(username=uu, password='kioshi')
    ta = get_torneo_activo()

    t = Tarjetas(torneo = ta, user = u)

    t.save()
    
    for i in range(0, len(aps)):
        p = Partidos.objects.get(equipo_1__nombre = pd[i][0], equipo_2__nombre = pd[i][1], torneo__id = ta.id)
        apuesta = Apuestas(tarjeta = t, partido = p, goles_1 = aps[i][0], goles_2 = aps[i][1])
        apuesta.save()



