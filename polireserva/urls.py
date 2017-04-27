from django.conf.urls import url
from . import views

app_name = 'polireserva'

urlpatterns = [
    # /polireserva/
    url(r'^$', views.index, name='polindex'),

    #Tipo de recursos
    # /polireserva/administracion/
    url(r'^administracion/$', views.modulo_admin, name='modulo_admin'),
    #/polireserva/tdr/
    url(r'^tdr/$', views.tdrlist, name= 'tdrlist'),
    url(r'^tdr/(?P<id_tdr>[0-9]+)/$', views.tdrdetail, name= 'tdrdetail'),
    url(r'^tdr/new/$',views.tdrfill,name='tdrfill'),
    url(r'^tdr/(?P<id_tdr>[0-9]+)/new/$', views.recursofill, name='recursofill'),
    url(r'^tdr/(?P<id_tdr>[0-9]+)/(?P<id_r>[0-9]+)/delete/$', views.deleterecurso, name='deleterecurso'),
    url(r'^tdr/(?P<id_tdr>[0-9]+)/(?P<id_r>[0-9]+)/confirm/$', views.deleterecursonconfirm, name='confirmrecurso'),

    #Reservas
    url(r'^reservas/$', views.reservalist, name='reservalist'),
    url(r'^reservas/new/$', views.newreserva, name='newreserva'),
    url(r'^reservas/(?P<id_R>[0-9]+)/$', views.reservadetail, name='reservadetail'),

]