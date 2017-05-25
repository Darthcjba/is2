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
    # /polireserva/dashboard/ --Modulo de Dashboard
    url(r'^dashboard/$', views.modulo_dashboard, name='modulo_dashboard'),
    #/polireserva/tdr/ --Lista Tipos de Recursos
    url(r'^administracion/recursos/$', views.tdrlist, name= 'tdrlist'),
    # /polireserva/tdr/<id_tdr>/ --Detalles Tipo de Recurso
    url(r'^tdr/(?P<id_tdr>[0-9]+)/$', views.tdrdetail, name= 'tdrdetail'),
    # /polireserva/tdr/new/ --Crear Tipo de Recurso
    url(r'^tdr/new/$',views.newtdr,name='tdrfill'),
    # /polireserva/tdr/<id_tdr>/new/ --Nuevo Recurso
    url(r'^tdr/(?P<id_tdr>[0-9]+)/new/$', views.newrecurso, name='recursofill'),
    #/polireserva/tdr/<id_tdr>/<id_r>/delete/ --Eliminar recursos
    url(r'^tdr/(?P<id_tdr>[0-9]+)/(?P<id_r>[0-9]+)/delete/$', views.deleterecurso, name='deleterecurso'),
    #/polireserva/tdr/<id_tdr>/<id_r>/confirm/ --Confirma Eliminar recursos
    url(r'^tdr/(?P<id_tdr>[0-9]+)/(?P<id_r>[0-9]+)/confirm/$', views.deleterecursonconfirm, name='confirmrecurso'),
    # /polireserva/tdr/<id_tdr>/delete/ --Eliminar TDR
    url(r'^tdr/(?P<id_tdr>[0-9]+)/delete/$', views.deletetdr, name='deletetdr'),
    # /polireserva/tdr/<id_tdr>/confirm/ --Confirma Eliminar TDR
    url(r'^tdr/(?P<id_tdr>[0-9]+)/confirm/$', views.deletetdrconfirm, name='confirmtdr'),
    #polireserva/usuarios/ --Listar usuarios
    url(r'^administracion/usuarios/$', views.userlist, name= 'userlist'),
    #listar roles de un usuario
    url(r'^usuarios/(?P<username_id>[0-9]+)/$', views.rolelist, name= 'roleslist'),

    #agregar roles a un usuario
    url(r'^usuarios/(?P<username_id>[0-9]+)/addroles$', views.roleassing, name= 'rolesassing'),

    #asignar rol
    url(r'^usuarios/(?P<username_id>[0-9]+)/addroles/(?P<role_id>[0-9]+)/$', views.roleassignation, name='rolesassignation'),


    #polireservas/reservas/list/ --Listar reservas
    url(r'^administracion/reservas/$', views.reservalist, name='reservalist'),
    # polireservas/reservas/new/ --Nueva reserva
    url(r'^reservas/new/$', views.newreserva, name='newreserva'),
    # polireservas/reservas/<id_R>/ --Detalles reserva
    url(r'^reservas/(?P<id_R>[0-9]+)/$', views.reservadetail, name='reservadetail'),
    # polireservas/reservas/<id_R>/edit--Modificar reserva
    url(r'^reservas/(?P<id_R>[0-9]+)/edit/$', views.updatereserva, name='updatereserva'),
    #polireservas/reservas/misreservas/ --Listar mis reservas
    url(r'^reservas/misreservas/$', views.misreservas, name='misreservas'),
    # /polireserva/reservas/<id_R>/delete/ --Eliminar reserva
    url(r'^reservas/(?P<id_R>[0-9]+)/delete/$', views.deletereserva, name='deletereserva'),
    # /polireserva/reservas/<id_R>/delete/confirm --Eliminar reserva confirmado
    url(r'^reservas/(?P<id_R>[0-9]+)/delete/confirm/$', views.deletereservaconfirm, name='deletereservaconfirm'),

    # polireservas/mantenimiento --listar los mantenimientos
    url(r'^mantenimiento/$',views.mantenimientolist,name='mantenimientolist'),
    # polireservas/mantenimiento/new --agregar recurso a mantenimiento
    url(r'^mantenimiento/new/$',views.mantenimientonew,name='mantenimientonew'),
    # polireservas/mantenimiento/<id_M>/fin --finalizar mantenimiento
    url(r'^mantenimiento/(?P<id_M>[0-9]+)/fin/$',views.mantenimientofin,name='mantenimientofin'),
    # polireservas/mantenimiento/<id_M>/detail --detalle del mantenimiento
    url(r'^mantenimiento/(?P<id_M>[0-9]+)/detail/$', views.amantenimiento, name='amantenimiento'),
    # polireservas/mantenimiento/<id_M>/confirm
    url(r'^mantenimiento/(?P<id_M>[0-9]+)/confirm/$', views.enviarman, name='enviarman'),

    # polireservas/recepcion/list --listar las reservas del dia, y las reservas en uso
    url(r'^recepcion/$', views.recepcionlist, name='recepcionlist')


]