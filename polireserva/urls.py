from django.conf.urls import url
from . import views

app_name = 'polireserva'

urlpatterns = [
    # /polireserva/ --Menu Principal
    url(r'^$', views.index, name='polindex'),
    # /polireserva/administracion/ --Modulo de Administracion
    url(r'^administracion/$', views.modulo_admin, name='modulo_admin'),
    # /polireserva/reservas/ --Modulo de Reservas
    url(r'^reservas/$', views.modulo_reservas, name='modulo_reservas'),
    # /polireserva/recepcion/ --Modulo de Recepcion
    url(r'^recepcion/$', views.modulo_recepcion, name='modulo_recepcion'),
    # /polireserva/mantenimiento/ --Modulo de Mantenimiento
    url(r'^mantenimiento/$', views.modulo_mantenimiento, name='modulo_mantenimiento'),
    # /polireserva/dashboard/ --Modulo de Dashboard
    url(r'^dashboard/$', views.modulo_dashboard, name='modulo_dashboard'),
    #/polireserva/tdr/list/ --Lista Tipos de Recursos
    url(r'^tdr/list/$', views.tdrlist, name= 'tdrlist'),
    # /polireserva/tdr/<id_tdr>/ --Detalles Tipo de Recurso
    url(r'^tdr/(?P<id_tdr>[0-9]+)/$', views.tdrdetail, name= 'tdrdetail'),
    # /polireserva/tdr/new/ --Crear Tipo de Recurso
    url(r'^tdr/new/$',views.tdrfill,name='tdrfill'),
    # /polireserva/tdr/<id_tdr>/new/ --Nuevo Recurso
    url(r'^tdr/(?P<id_tdr>[0-9]+)/new/$', views.recursofill, name='recursofill'),
    #/polireserva/tdr/<id_tdr>/<id_r>/delete/ --Eliminar recursos
    url(r'^tdr/(?P<id_tdr>[0-9]+)/(?P<id_r>[0-9]+)/delete/$', views.deleterecurso, name='deleterecurso'),
    #/polireserva/tdr/<id_tdr>/<id_r>/confirm/ --Confirma Eliminar recursos
    url(r'^tdr/(?P<id_tdr>[0-9]+)/(?P<id_r>[0-9]+)/confirm/$', views.deleterecursonconfirm, name='confirmrecurso'),
    # /polireserva/tdr/<id_tdr>/delete/ --Eliminar TDR
    url(r'^tdr/(?P<id_tdr>[0-9]+)/delete/$', views.deletetdr, name='deletetdr'),
    # /polireserva/tdr/<id_tdr>/confirm/ --Confirma Eliminar TDR
    url(r'^tdr/(?P<id_tdr>[0-9]+)/confirm/$', views.deletetdrconfirm, name='confirmtdr'),
    #polireserva/usuarios/ --Listar usuarios
    url(r'^usuarios/$', views.userlist, name= 'userlist'),
    #polireservas/reservas/list/ --Listar reservas
    url(r'^reservas/list/$', views.reservalist, name='reservalist'),
    # polireservas/reservas/new/ --Nueva reserva
    url(r'^reservas/new/$', views.newreserva, name='newreserva'),
    # polireservas/reservas/<id_R>/ --Detalles reserva
    url(r'^reservas/(?P<id_R>[0-9]+)/$', views.reservadetail, name='reservadetail'),

]