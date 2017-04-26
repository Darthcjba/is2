from django.conf.urls import url
from . import views

app_name = 'polireserva'

urlpatterns = [
    # /polireserva/
    url(r'^$', views.index, name='polindex'),

    #Tipo de recursos
    url(r'^tdr/$', views.tdrlist, name= 'tdrlist'),
    url(r'^tdr/(?P<id_tdr>[0-9]+)/$', views.tdrdetail, name= 'tdrdetail'),
    url(r'^tdr/new/$',views.tdrfill,name='tdrfill'),

    #Reservas
    url(r'^reservas/$', views.reservalist, name='reservalist'),
    url(r'^reservas/new/$', views.newreserva, name='newreserva'),
    url(r'^reservas/(?P<id_R>[0-9]+)/$', views.reservadetail, name='reservadetail'),

]