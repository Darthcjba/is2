from django import forms
from .models import Usuario
from .models import TdRecurso
from .models import Recurso
from .models import Reserva
from .models import Mantenimiento
from .models import RecursoReserva

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




class ReservaForm(forms.ModelForm):

    class Meta:
        model = Reserva
        fields = ('id_R', 'tdr', 'user', 'status', 'obs', 'date_i', 'date_f')


class RecursoReservaForm(forms.ModelForm):

    class Meta:
        model = RecursoReserva
        fields = ('id_RR', 'id_reserva', 'id_recurso')


class MantenimientoForm(forms.ModelForm):

    class Meta:
        model = Mantenimiento
        fields = ('id_M', 'user', 'recurso', 'kindM', 'reason', 'report', 'date_c')

