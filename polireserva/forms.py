from django import forms
from .models import Usuario
from .models import TdRecurso
from .models import Recurso
from .models import Reservas
from .models import Mantenimiento

class UsuarioForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('ladder', 'cin', 'user')

class TdRecursoForm(forms.ModelForm):

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


class MantenimientoForm(forms.ModelForm):

    class Meta:
        model = Mantenimiento
        fields = ('id_M', 'user', 'recurso', 'kindM', 'reason', 'report', 'date_c')

