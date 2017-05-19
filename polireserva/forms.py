from django import forms
from .models import *
from django.contrib.auth.models import User
from datetimewidget.widgets import DateTimeWidget, DateWidget
from django.utils import timezone


ROLES = (
    ('administrador','administrador'),
    ('usuario','usuario'),
    ('recepcionista','recepcionista'),
    ('mantenimiento','mantenimiento'),
    ('invitado','invitado'),
    )

class RolesForm(forms.Form):
    roles=forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=ROLES,
    )




class TdRecursoForm(forms.ModelForm):
    class Meta:
        model = TdRecurso
        fields = ('id_tdr', 'description')


class TdRecursoFillForm(forms.ModelForm):
    description = forms.CharField(max_length=25, label="Nombre del tipo de Recurso",
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'descripciontdr'}))

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

    dateTimeOptions = {
        'format': 'yyyy-mm-dd',
        'weekStart':1,
        'clearBtn':False
    }

    name_r = forms.CharField(max_length=25, label="Nombre del Recurso",
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Estado",
                               widget=forms.Select(attrs={'class': 'form-control'}))
    date_c = forms.DateField(label="Fecha de submision", widget=DateWidget(usel10n= False,attrs={'id': "date_c", 'class': 'form-control'}, bootstrap_version=3, options=dateTimeOptions))
    date_m = forms.DateField(label="Fecha de modificacion", widget=DateWidget(usel10n=False,attrs={'id': "date_m", 'class': 'form-control'}, bootstrap_version=3, options=dateTimeOptions))
    description = forms.CharField(label="Descripcion del item", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Recurso
        fields = ('name_r', 'status', 'date_c', 'date_m', 'description',)


class ReservasForm(forms.ModelForm):
    dateTimeOptions = {
        'format': 'mm/dd/yyyy hh:ii',
        'weekStart': 1,
        'clearBtn': False
    }

    id_R = forms.IntegerField(label="ID", max_value=1000, widget=forms.HiddenInput, required=False)
    tdr = forms.ModelChoiceField(label="Tipo de recurso", queryset=TdRecurso.objects.all().order_by('description'), required=True,
                                 widget=forms.Select(attrs={'class': 'form-control', 'name': 'tdrselect'}))
    recursos = forms.ModelMultipleChoiceField(label="Recursos", queryset=Recurso.objects.all(), required=True,
                                              widget=forms.SelectMultiple(
                                                  attrs={'class': 'form-control', 'name': 'rselect'}))
    status = forms.ChoiceField(label="Tipo de recurso", choices=Reservas.STATUS_CHOICES, required=True, initial='',
                               widget=forms.Select(attrs={'class': 'form-control', 'name': 'statusselect'}))
    obs = forms.CharField(max_length=25, label="Observacion",
                          widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'reservaobs'}))
    date_i = forms.DateTimeField(label="Desde", widget=DateTimeWidget(usel10n=False, attrs={'class': 'form-control'}, bootstrap_version=3, options=dateTimeOptions))
    date_f = forms.DateTimeField(label="Hasta", widget=DateTimeWidget(usel10n=False, attrs={'class': 'form-control'}, bootstrap_version=3, options=dateTimeOptions))

    #evita que la fecha de inicio sea fijada en el pasado
    def clean_date_i(self):
        date_i = self.cleaned_data['date_i']
        if date_i<timezone.now():
            raise forms.ValidationError("La fecha de inicio de la reserva no puede ser una fecha pasada!")
        return date_i
    #evita que la fecha de fin sea fijada en el pasado
    def clean_date_f(self):
        date_f = self.cleaned_data['date_f']
        if date_f < timezone.now():
            raise forms.ValidationError("La fecha de fin de la reserva no puede ser una fecha pasada!")
        return date_f

    class Meta:
        model = Reservas
        fields = ('tdr', 'recursos', 'status', 'obs', 'date_i', 'date_f')



class MantenimientoForm(forms.ModelForm):

    class Meta:
        model = Mantenimiento
        fields = ( 'user', 'recurso', 'kindM', 'reason', 'report', 'date_c',)


class MantenimientoNewForm(forms.ModelForm):
    dateTimeOptions = {
        'format': 'yyyy-mm-dd',
        'weekStart': 1,
        'clearBtn': False
    }

    recurso = forms.ModelChoiceField(label="Recursos", queryset=Recurso.objects.filter(status='Disponible'), required=True,
                                              widget=forms.Select(attrs={'class': 'form-control', 'name': 'rselect'}))
    date_c = forms.DateField(label="Fecha de submision",widget=DateWidget(usel10n=False, attrs={'id': "date_c", 'class': 'form-control'},bootstrap_version=3, options=dateTimeOptions))
    kindM= forms.ChoiceField(label="Fecha",choices=Mantenimiento.KIND_CHOICES,required=True,initial='')
    reason = forms.CharField(label="Razon del mantenimiento", max_length=200)

    class Meta:
        model=Mantenimiento
        fields = {'recurso','date_c','kindM','reason'}


class MantenimientoFinForm(forms.ModelForm):

    report = forms.CharField(label="Reporte de mantenimiento", max_length=100)

    class Meta:
        model=Mantenimiento
        fields = { 'report'}