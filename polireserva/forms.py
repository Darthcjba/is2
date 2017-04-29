from django import forms
from .models import *
from django.contrib.auth.models import User
from datetimewidget.widgets import DateTimeWidget, DateWidget


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
    id_R = forms.IntegerField(label="ID", max_value=1000, widget=forms.HiddenInput, required=False)
    tdr = forms.ModelChoiceField(label="Tipo de recurso", queryset=TdRecurso.objects.all(), required=True,
                                 widget=forms.Select(attrs={'class': 'form-control', 'name': 'tdrselect'}))
    recursos = forms.ModelMultipleChoiceField(label="Recursos", queryset=Recurso.objects.all(), required=True,
                                              widget=forms.SelectMultiple(
                                                  attrs={'class': 'form-control', 'name': 'rselect'}))
    status = forms.ChoiceField(label="Tipo de recurso", choices=Reservas.STATUS_CHOICES, required=True, initial='',
                               widget=forms.Select(attrs={'class': 'form-control', 'name': 'statusselect'}))
    obs = forms.CharField(max_length=25, label="Observacion",
                          widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'reservaobs'}))
    date_i = forms.DateTimeField(label="Fecha", widget=DateTimeWidget(attrs={'class': 'form-control'}))
    date_f = forms.DateTimeField(label="Fecha", widget=DateTimeWidget(attrs={'class': 'form-control'}))

    class Meta:
        model = Reservas
        fields = ('tdr', 'recursos', 'status', 'obs', 'date_i', 'date_f')
        dateTimeOptions = {
            'format': 'dd/mm/yyyy HH:ii',
            'autoclose': True,
            'showMeridian': True
        }

        widgets = {
            'recursos': forms.Select(),
            # Use localization and bootstrap 3
            'date_i': DateTimeWidget(attrs={'id': "date_i", 'class': 'form-control'}, usel10n=True,
                                     bootstrap_version=3),
            'date_f': DateTimeWidget(attrs={'id': "date_f", 'class': 'form-control'}, usel10n=True, bootstrap_version=3)
        }

