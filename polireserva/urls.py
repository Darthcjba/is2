from django.conf.urls import url
from . import views

app_name = 'polireserva'

urlpatterns = [
    # /polireserva/
    url(r'^$', views.index, name='polindex'),
    # /polireserva/administracion/
    url(r'^administracion/$', views.modulo_admin, name='modulo_admin'),
    #/polireserva/tdr/
    url(r'^tdr/$', views.tdrlist, name= 'tdrlist'),
    #/polireserva/tdr/<id_tdr>/
    url(r'^tdr/(?P<id_tdr>[0-9]+)/$', views.tdrdetail, name= 'tdrdetail'),
    # /polireserva/tdr/<id_tdr>/newr
    url(r'^tdr/(?P<id_tdr>[0-9]+)/new/$', views.recursofill, name='recursofill'),
    #/polireserva/tdr/newtdr/
    url(r'^tdr/new/$',views.tdrfill,name='tdrfill')

]