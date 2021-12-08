from django.conf.urls import include, url

from . import views

urlpatterns = [
    url('^mi_tarjeta/?$', views.editar_tarjeta, name='mi_tarjeta'),
    url('^torneo/?$', views.administrar_torneo, name='torneo'),
    url('', views.index, name='index'),
]