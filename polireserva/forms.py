from django import forms
from .models import TdRecurso
from .models import Recurso
from .models import Reservas


class TdRecursoForm(forms.ModelForm):

    class Meta:
        model = TdRecurso
        fields = ('id_tdr', 'description')


class TdRecursoFillForm(forms.ModelForm):
    id_tdr = forms.IntegerField(label= "ID")
    description = forms.CharField(max_length=25,label="Nombre del tipo de Recurso")

    class Meta:
        model = TdRecurso
        fields = ('id_tdr', 'description')




class RecursoForm(forms.ModelForm):

    class Meta:
        model = Recurso
        fields = ('id_r', 'name_r', 'status', 'date_c', 'date_m', 'description', )




class ReservasForm(forms.ModelForm):

    class Meta:
        model = Reservas
        fields = ('id_R', 'tdr', 'user', 'recursos', 'status', 'obs', 'date_i', 'date_f')


