from django.http import HttpResponse
from django.shortcuts import render
from .models import Torneos, Equipos, Partidos, Tarjetas, Apuestas
from .forms import LoginMiniForm, LogoutMiniForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count, Min, Sum, Avg
from django.forms import modelformset_factory
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist

def get_torneo_activo():
    ts = Torneos.objects.filter(activo = True)
    ta = -1
    for t in ts:
        if t.activo == True:
            ta = t.id
    if ta == -1:
        raise("No hay torneo activo")
    return Torneos.objects.get(id = ta)


def index(request):
    username, form, user = login_managment(request)
    ta = get_torneo_activo()
    #torneos = Torneos.objects.filter(nombre__contains='Mundial')
    partidos = Partidos.objects.filter(torneo = ta.id)
    tarjetas = Tarjetas.objects.filter(torneo = ta.id).filter(user__username = username)
    apuestas = Apuestas.objects.filter(tarjeta__torneo = ta.id).filter(tarjeta__user__username = username)
    ranking = Tarjetas.objects.filter(torneo = ta.id).order_by('-puntos')
    context = {'torneo': ta, 'partidos': partidos, 'apuestas': apuestas,  'tarjetas': tarjetas, 
                'ranking': ranking, 'login_mini_form': form, 'username': request.user.username, 'user': user}
    return render(request, 'apuestas/browser.html', context)
    
# Create your views here.



# Do login managment and returns a tuple with ( username or None, Form)  
def login_managment(request):
    if request.user.is_authenticated():  
        form = LogoutMiniForm()
        if request.method == 'POST':
            form = LogoutMiniForm(request.POST)
            if form.is_valid():
                logout(request)
                form = LoginMiniForm()
    else:   #user not authenticated
        if request.method == 'POST':
            form = LoginMiniForm(request.POST)
            if form.is_valid():
                #autenticate
                #user = authenticate(request, username = form.cleaned_data['username'], password = form.cleaned_data['password'])
                user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
                if user is not None:
                    login(request, user)
                    form = LogoutMiniForm()
                else:
                    form = LoginMiniForm(request.POST)
        else:
            form = LoginMiniForm()
    if request.user.is_authenticated():
        username = request.user.username
    else:
        username = None
    return username, form, request.user

def sign(a):
    if a>0:
        return 1
    elif a<0:
        return -1
    else:
        return 0


def actualizar():
    ta = get_torneo_activo()
    apuestas = Apuestas.objects.filter(tarjeta__torneo = ta.id)
    for a in apuestas:
        r = a.puntos
        if a.partido.jugado:
            a.puntos = 0
            if a.goles_1 == a.partido.goles_1:
                a.puntos = 2
            if a.goles_2 == a.partido.goles_2:
                a.puntos = a.puntos + 2
            if sign(a.goles_1 - a.goles_2) == sign(a.partido.goles_1 - a.partido.goles_2):
                a.puntos = a.puntos + 3
            if r != a.puntos:
                a.save()
    
    tarjetas = Tarjetas.objects.filter(torneo = ta.id).annotate(p = Sum('apuestas__puntos'))
    for t in tarjetas:
        t.puntos = t.p
        t.save()

    return 0

class TorneosForm(ModelForm):
    class Meta:
        model = Torneos
        fields = ['nombre']

        

def administrar_torneo(request):

    if request.method == 'POST':
        partidosformset = modelformset_factory(Partidos, exclude = ('torneo', ))
        partidosformset_bound = partidosformset(request.POST)
        #Crucemos los dedos:
        partidosformset_bound.save()
        actualizar()
        
    ta = get_torneo_activo()
    #obtenemos los partidos del torneo:
    partidos = Partidos.objects.filter(torneo = ta.id)
    #verificamos si faltan partidos a agregar:
    cp = 0
    for p in partidos:
        cp=cp+1
    
    if cp < ta.fechas:
        #obtenemos un equipo:
        ea = Equipos.objects.all()[0]
        eb = Equipos.objects.all()[1]
        for i in range(cp, ta.fechas):
            p = Partidos(torneo = ta, equipo_1 = ea, equipo_2 = eb)
            p.save()

    #obtenemos los partidos del torneo:
    partidos = Partidos.objects.filter(torneo = ta.id)

    
    PartidosFormset = modelformset_factory(Partidos, exclude = ('torneo', ), extra=0)
    
    context = {'torneo': ta, 'partidos' : PartidosFormset(queryset=partidos) }
    return render(request, 'apuestas/admin_torneo.html', context)

def editar_tarjeta(request):
    aux = ''

    #obtenemos el torneo activo
    ta = get_torneo_activo()

    
    #si no hay tarjeta, la creo:
    t = Tarjetas.objects.filter(torneo = ta, user = request.user).first()
    if not t:
        t = Tarjetas(torneo = ta, user = request.user)
        t.save()

    #obtenemos las apuestas de la tarjeta:
    apuestas = Apuestas.objects.filter(tarjeta = t.id)

    if request.method == 'POST':
        ApuestasFormset = modelformset_factory(Apuestas, exclude = ('tarjeta', 'puntos' ), extra=0)
        apuestasformset_bound = ApuestasFormset(request.POST, initial = apuestas)
        if  apuestasformset_bound.is_valid():            
            for f in apuestasformset_bound.forms:
                #obtengo los datos:
                data = f.cleaned_data
                #verifico si el partido esta en la lista:
                p = apuestas.filter(partido = data['partido'].id).first()
                if p == None:
                    raise Exception("Se ha cambiado un partido")
                #si no esta jugado, lo cambiamos:    
                if data['partido'].jugado == False:
                    p.goles_1 = data['goles_1']
                    p.goles_2 = data['goles_2']
                    p.save()
                    
                #aux = '{0} / {1} - {2}'.format(aux, data['partido'], data['partido'].jugado)
                
        #Crucemos los dedos:
        #apuestasformset_bound.save()
        #no llamo a actualizar porque las apuestas son sobre partidos no jugados aun....
        

    #verificamos si faltan apuestas a agregar:
    if apuestas.count() < ta.fechas:
        partidos = Partidos.objects.filter(torneo = ta)
        #este codigo se puede resolver con una consulta SQL, la cual ahora no voy a realizar:
        for p in partidos:
            if not apuestas.filter(partido = p).first():
                #si no esta la apuestas la agrego:
                a = Apuestas(tarjeta = t, partido = p)
                a.save()
        

    #ya normalizado, obtenemos las apuestas de la tarjeta:
    apuestas = Apuestas.objects.filter(tarjeta = t.id)

    
    ApuestasFormset = modelformset_factory(Apuestas, exclude = ('tarjeta', 'puntos' ), extra=0)
    
    context = {'torneo': ta, 'apuestas' : ApuestasFormset(queryset=apuestas), 'aux': aux}
    return render(request, 'apuestas/mi_tarjeta.html', context)

    