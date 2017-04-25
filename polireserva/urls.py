from django.conf.urls import url
from . import views

urlpatterns = [
    # /polireserva/
    url(r'^$', views.index, name='polindex'),
    #/polireserva/tdr/
    url(r'^tdr/$', views.tdrlist, name= 'tdrlist'),
    #/polireserva/tdr/154/
    url(r'^tdr/(?P<id_tdr>[0-9]+)/$', views.tdrdetail, name= 'tdrdetail'),
]