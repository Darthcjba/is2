from django import forms
from .models import TdRecurso
from .models import Recurso
from .models import Reservas


class TdRecursoForm(forms.ModelForm):

    class Meta:
        model = TdRecurso
        fields = ('id_tdr', 'description')


class TdRecursoFillForm(forms.ModelForm):
    description = forms.CharField(max_length=25,label="Nombre del tipo de Recurso", widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'descripciontdr'}))

    class Meta:
        model = TdRecurso
        fields = ('description',)




class RecursoForm(forms.ModelForm):

    class Meta:
        model = Recurso
        fields = ('name_r', 'status', 'date_c', 'date_m', 'description',)

class RecursoFillForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('Disponible', 'Disponible'),
        ('EnUso', 'En Uso'),
        ('NoDisponible', 'No Disponible'),
        ('Mantenimiento', 'Mantenimiento')
    )

    name_r= forms.CharField(max_length=25,label="Nombre del Recurso")
    status=forms.ChoiceField(choices=STATUS_CHOICES, label="Estado")
    date_c=forms.DateField(label="Fecha de submision")
    date_m=forms.DateField(label="Fecha de alteracion")
    description = forms.CharField(label="Descripcion del item" , max_length=50)

    class Meta:
        model = Recurso
        fields = ('name_r', 'status', 'date_c', 'date_m', 'description',)





class ReservasForm(forms.ModelForm):

    class Meta:
        model = Reservas
        fields = ('id_R', 'tdr', 'user', 'recursos', 'status', 'obs', 'date_i', 'date_f')


